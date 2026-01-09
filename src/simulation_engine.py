"""
Mountain Road Safety Simulator - Core Simulation Engine
Implements vehicle physics, stability analysis, brake failure prediction, and hazard detection
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import math


class VehicleSimulator:
    """Simulates vehicle behavior on mountain roads"""
    
    def __init__(self, vehicle_params: pd.Series):
        self.vehicle_type = vehicle_params['Vehicle_Type']
        self.weight = vehicle_params['Weight_kg']
        self.length = vehicle_params['Length_m']
        self.width = vehicle_params['Width_m']
        self.brake_capacity = vehicle_params['Brake_Capacity']
        self.max_safe_speed = vehicle_params['Max_Safe_Speed_Hills_kmh']
        self.brake_heat_factor = vehicle_params['Brake_Heat_Factor']
        self.center_of_gravity = vehicle_params['Center_Of_Gravity_m']
        
        # Initialize tracking variables
        self.brake_temperature = 20  # Starting at ambient temperature (°C)
        self.cumulative_brake_usage = 0
        
    def calculate_stability_risk(self, 
                                  slope: float, 
                                  road_width: float, 
                                  curve_sharpness: str,
                                  speed: float,
                                  road_friction: float = 0.85) -> Dict:
        """
        Calculate vehicle stability risk on a road segment
        
        Args:
            slope: Slope magnitude in percentage
            road_width: Road width in meters
            curve_sharpness: Category (Gentle, Moderate, Sharp, Very_Sharp)
            speed: Vehicle speed in km/h
            road_friction: Road surface friction coefficient
            
        Returns:
            Dictionary with stability metrics and risk score
        """
        # Convert slope percentage to angle in radians
        slope_angle = math.atan(slope / 100)
        
        # Curve sharpness factors
        curve_factors = {
            'Gentle': 0.1,
            'Moderate': 0.3,
            'Sharp': 0.6,
            'Very_Sharp': 0.9
        }
        curve_factor = curve_factors.get(curve_sharpness, 0.5)
        
        # Calculate lateral stability risk (curve + speed)
        speed_ratio = speed / self.max_safe_speed
        lateral_risk = curve_factor * speed_ratio * 1.0
        
        # Calculate longitudinal stability (slope + weight)
        slope_risk = min(abs(slope) / 35, 1.0)  # Normalize to max 35% slope for earlier risk
        weight_factor = self.weight / 12000  # Normalized to bus weight
        longitudinal_risk = slope_risk * weight_factor * 1.2
        
        # Road width vs vehicle width clearance
        clearance = road_width - self.width
        clearance_risk = max(0, 1 - (clearance / 3.0))  # Risk increases if less than 3m clearance
        
        # Center of gravity tipping risk on curves
        tipping_risk = (self.center_of_gravity / 2.5) * curve_factor * speed_ratio
        
        # Friction-based stability
        friction_risk = (1 - road_friction) * 0.5
        
        # Overall stability risk (0-1 scale)
        stability_risk = min(
            (lateral_risk * 0.3 + 
             longitudinal_risk * 0.25 + 
             clearance_risk * 0.2 + 
             tipping_risk * 0.15 +
             friction_risk * 0.1),
            1.0
        )
        
        return {
            'stability_risk': stability_risk,
            'lateral_risk': lateral_risk,
            'longitudinal_risk': longitudinal_risk,
            'clearance_risk': clearance_risk,
            'tipping_risk': tipping_risk,
            'speed_ratio': speed_ratio,
            'safe_speed_recommendation': self.max_safe_speed * (1 - curve_factor)
        }
    
    def calculate_brake_failure_risk(self, 
                                       slope: float, 
                                       segment_distance: float,
                                       speed: float,
                                       is_downhill: bool) -> Dict:
        """
        Calculate brake failure risk based on brake heating model
        
        Args:
            slope: Slope percentage (negative for downhill)
            segment_distance: Segment length in km
            speed: Vehicle speed in km/h
            is_downhill: Whether vehicle is descending
            
        Returns:
            Dictionary with brake temperature and failure risk
        """
        if not is_downhill or slope >= 0:
            # Uphill or flat - brakes cool down
            cooling_rate = 5  # °C per segment
            self.brake_temperature = max(20, self.brake_temperature - cooling_rate)
            self.cumulative_brake_usage = max(0, self.cumulative_brake_usage - 0.1)
            
            return {
                'brake_temperature': self.brake_temperature,
                'brake_failure_risk': 0.0,
                'brake_usage': 0.0,
                'status': 'Cooling'
            }
        
        # Downhill - brakes heat up
        slope_magnitude = abs(slope)
        
        # Calculate brake energy dissipation
        # E = m * g * h = m * g * d * sin(theta)
        distance_m = segment_distance * 1000
        slope_radians = math.atan(slope_magnitude / 100)
        height_loss = distance_m * math.sin(slope_radians)
        
        # Energy dissipated through brakes (Joules)
        energy_dissipated = self.weight * 9.81 * height_loss
        
        # Convert to temperature increase (simplified heat model)
        # Assuming brake mass ~50kg, specific heat ~500 J/(kg·°C)
        brake_mass = 50
        specific_heat = 500
        temp_increase = (energy_dissipated * self.brake_heat_factor) / (brake_mass * specific_heat * 1000)
        
        # Speed factor - higher speed needs more braking
        speed_factor = (speed / self.max_safe_speed) * 2.0
        temp_increase *= speed_factor
        
        # Update brake temperature
        self.brake_temperature += temp_increase
        
        # Natural cooling during travel
        ambient_cooling = 2  # °C per segment
        self.brake_temperature -= ambient_cooling
        self.brake_temperature = max(20, self.brake_temperature)
        
        # Cumulative brake usage
        brake_usage = (slope_magnitude / 30) * (segment_distance / 0.11)
        self.cumulative_brake_usage += brake_usage
        
        # Calculate failure risk
        # Critical temperature: 300°C (brakes start to fade)
        # Dangerous temperature: 400°C (brake failure)
        temp_risk = 0
        if self.brake_temperature > 200:
            temp_risk = (self.brake_temperature - 200) / 200
        
        # Cumulative usage risk
        usage_risk = min(self.cumulative_brake_usage / 10, 1.0)
        
        # Combined brake failure risk
        brake_failure_risk = min((temp_risk * 0.7 + usage_risk * 0.3), 1.0)
        
        # Status determination
        if self.brake_temperature > 350:
            status = 'CRITICAL - Brake Failure Imminent'
        elif self.brake_temperature > 250:
            status = 'WARNING - Brakes Overheating'
        elif self.brake_temperature > 150:
            status = 'Caution - Elevated Temperature'
        else:
            status = 'Normal'
        
        return {
            'brake_temperature': round(self.brake_temperature, 1),
            'brake_failure_risk': brake_failure_risk,
            'brake_usage': brake_usage,
            'cumulative_usage': self.cumulative_brake_usage,
            'status': status,
            'energy_dissipated_mj': round(energy_dissipated / 1e6, 2)
        }
    
    def calculate_cliff_fall_risk(self,
                                   cliff_present: bool,
                                   guardrail: bool,
                                   road_width: float,
                                   visibility: float,
                                   speed: float,
                                   stability_risk: float) -> Dict:
        """
        Calculate risk of vehicle falling off cliff
        
        Args:
            cliff_present: Whether cliff exists on roadside
            guardrail: Whether guardrail is present
            road_width: Road width in meters
            visibility: Visibility distance in meters
            speed: Vehicle speed in km/h
            stability_risk: Pre-calculated stability risk
            
        Returns:
            Dictionary with cliff fall risk and contributing factors
        """
        if not cliff_present:
            return {
                'cliff_fall_risk': 0.0,
                'factors': 'No cliff present',
                'severity': 'None'
            }
        
        # Base risk from cliff presence - increased from 0.4 to 0.6
        base_risk = 0.6
        
        # Guardrail protection factor
        if guardrail:
            protection_factor = 0.25  # 75% risk reduction with guardrail
        else:
            protection_factor = 1.2  # 20% increase without protection
        
        # Road width factor - narrower roads are much more dangerous
        width_risk = max(0, 1 - (road_width / 7))  # Safer if wider than 7m
        
        # Visibility factor - poor visibility drastically increases risk
        visibility_risk = max(0, 1 - (visibility / 80))  # Safer with >80m visibility
        
        # Speed factor - higher speeds much more dangerous near cliffs
        speed_risk = min(speed / 60, 1.3)  # Normalized to 60 km/h with overage
        
        # Stability contribution - vehicle instability near cliffs is critical
        stability_contribution = stability_risk * 0.8
        
        # Combined cliff fall risk with increased weights
        cliff_fall_risk = base_risk * protection_factor * (
            width_risk * 0.30 +
            visibility_risk * 0.25 +
            speed_risk * 0.25 +
            stability_contribution * 0.20
        )
        
        cliff_fall_risk = min(cliff_fall_risk, 1.0)
        
        # Determine severity
        if cliff_fall_risk > 0.7:
            severity = 'EXTREME - Immediate danger'
        elif cliff_fall_risk > 0.5:
            severity = 'HIGH - Very dangerous'
        elif cliff_fall_risk > 0.3:
            severity = 'MEDIUM - Caution required'
        else:
            severity = 'LOW - Manageable risk'
        
        factors = []
        if not guardrail:
            factors.append('No guardrail')
        if width_risk > 0.5:
            factors.append('Narrow road')
        if visibility_risk > 0.5:
            factors.append('Poor visibility')
        if speed_risk > 0.6:
            factors.append('Excessive speed')
        
        return {
            'cliff_fall_risk': cliff_fall_risk,
            'factors': ', '.join(factors) if factors else 'Multiple risk factors',
            'severity': severity,
            'guardrail_present': guardrail
        }


class EnvironmentalHazards:
    """Analyzes environmental hazards like landslides"""
    
    @staticmethod
    def calculate_landslide_risk(slope: float,
                                  rainfall: float,
                                  soil_type: str,
                                  base_risk: float,
                                  vegetation: str = 'Medium') -> Dict:
        """
        Calculate landslide probability for a road segment
        
        Args:
            slope: Slope magnitude in percentage
            rainfall: Rainfall amount in mm
            soil_type: Type of soil (Rocky, Loose, Mixed)
            base_risk: Base environmental risk factor
            vegetation: Vegetation cover level
            
        Returns:
            Dictionary with landslide risk and recommendations
        """
        # Slope factor (steeper = more risk)
        slope_factor = min(abs(slope) / 40, 1.0)  # Normalize to 40% slope
        
        # Soil susceptibility
        soil_factors = {
            'Rocky': 0.3,
            'Loose': 0.9,
            'Mixed': 0.6
        }
        soil_factor = soil_factors.get(soil_type, 0.6)
        
        # Rainfall impact
        if rainfall < 25:
            rain_factor = 0.1
        elif rainfall < 75:
            rain_factor = 0.4
        elif rainfall < 150:
            rain_factor = 0.7
        else:
            rain_factor = 1.0
        
        # Vegetation protection
        vegetation_factors = {
            'Low': 1.0,
            'Medium': 0.7,
            'High': 0.4
        }
        veg_factor = vegetation_factors.get(vegetation, 0.7)
        
        # Combined landslide risk
        landslide_risk = base_risk * (
            slope_factor * 0.35 +
            soil_factor * 0.30 +
            rain_factor * 0.25 +
            veg_factor * 0.10
        )
        
        landslide_risk = min(landslide_risk, 1.0)
        
        # Risk categorization
        if landslide_risk > 0.7:
            category = 'CRITICAL'
            action = 'Road closure recommended'
        elif landslide_risk > 0.5:
            category = 'HIGH'
            action = 'Restrict heavy vehicles, monitor continuously'
        elif landslide_risk > 0.3:
            category = 'MEDIUM'
            action = 'Increase monitoring, warning signs'
        else:
            category = 'LOW'
            action = 'Normal monitoring'
        
        return {
            'landslide_risk': landslide_risk,
            'risk_category': category,
            'recommended_action': action,
            'slope_contribution': slope_factor,
            'rainfall_contribution': rain_factor,
            'soil_contribution': soil_factor
        }
    
    @staticmethod
    def adjust_for_driver_behavior(base_risk: float,
                                     is_night: bool = False,
                                     is_overspeeding: bool = False,
                                     poor_visibility: bool = False,
                                     driver_experience: str = 'Medium') -> Dict:
        """
        Adjust risk based on driver behavior and conditions
        
        Args:
            base_risk: Calculated base risk score
            is_night: Whether driving at night
            is_overspeeding: Whether driver is overspeeding
            poor_visibility: Poor visibility conditions
            driver_experience: Driver experience level
            
        Returns:
            Dictionary with adjusted risk and factors
        """
        risk_multiplier = 1.0
        factors = []
        
        if is_night:
            risk_multiplier += 0.35
            factors.append('Night driving (+35%)')
        
        if is_overspeeding:
            risk_multiplier += 0.50
            factors.append('Overspeeding (+50%)')
        
        if poor_visibility:
            risk_multiplier += 0.40
            factors.append('Poor visibility (+40%)')
        
        # Driver experience factor
        experience_factors = {
            'Novice': 1.4,
            'Medium': 1.0,
            'Expert': 0.75
        }
        exp_factor = experience_factors.get(driver_experience, 1.0)
        risk_multiplier *= exp_factor
        
        if exp_factor > 1.0:
            factors.append(f'Novice driver (+{int((exp_factor-1)*100)}%)')
        elif exp_factor < 1.0:
            factors.append(f'Expert driver ({int((1-exp_factor)*100)}% reduction)')
        
        adjusted_risk = min(base_risk * risk_multiplier, 1.0)
        
        return {
            'adjusted_risk': adjusted_risk,
            'risk_increase': adjusted_risk - base_risk,
            'risk_multiplier': risk_multiplier,
            'contributing_factors': factors
        }


def simulate_vehicle_journey(road_data: pd.DataFrame,
                               road_characteristics: pd.DataFrame,
                               vehicle_params: pd.Series,
                               environment: pd.Series,
                               speed: float = None,
                               driver_behavior: Dict = None) -> pd.DataFrame:
    """
    Simulate complete vehicle journey through all road segments
    
    Args:
        road_data: DataFrame with elevation and slope data
        road_characteristics: DataFrame with road features
        vehicle_params: Vehicle parameters series
        environment: Environmental conditions series
        speed: Override speed (km/h), defaults to vehicle's safe speed
        driver_behavior: Dictionary with driver behavior settings
        
    Returns:
        DataFrame with detailed risk analysis for each segment
    """
    vehicle = VehicleSimulator(vehicle_params)
    
    if speed is None:
        speed = vehicle.max_safe_speed * 0.9  # Default to 90% of max safe speed
    
    if driver_behavior is None:
        driver_behavior = {
            'is_night': False,
            'is_overspeeding': False,
            'poor_visibility': False,
            'driver_experience': 'Medium'
        }
    
    results = []
    
    # Merge road data with characteristics
    combined = road_data.merge(road_characteristics, on='Segment', how='left')
    
    for idx, segment in combined.iterrows():
        segment_id = segment['Segment']
        slope_pct = segment['Slope_Magnitude(%)']
        slope_direction = segment['Slop(%)']
        
        # Parse slope direction
        is_downhill = '-' in str(slope_direction)
        
        # Get segment characteristics with safe defaults
        road_width = float(segment.get('Road_Width_m', 7.0))
        curve_sharpness = str(segment.get('Curve_Sharpness', 'Moderate'))
        cliff_present = str(segment.get('Cliff_Present', 'No')).strip().lower() == 'yes'
        guardrail = str(segment.get('Guardrail_Present', 'Yes')).strip().lower() == 'yes'
        visibility = float(segment.get('Visibility_m', 80))
        
        # Calculate segment distance (difference from previous segment)
        current_distance = float(segment.get('Distance(KM)', 0.11 * (idx + 1)))
        if idx > 0:
            prev_distance = float(combined.loc[idx-1, 'Distance(KM)'])
            segment_distance = current_distance - prev_distance
        else:
            segment_distance = 0.11  # Default first segment length
        
        # Ensure positive distance
        if segment_distance <= 0:
            segment_distance = 0.11
        
        # Calculate stability risk
        stability = vehicle.calculate_stability_risk(
            slope_pct, road_width, curve_sharpness, speed, environment['Road_Friction']
        )
        
        # Calculate brake failure risk
        brake = vehicle.calculate_brake_failure_risk(
            slope_pct if is_downhill else -slope_pct,
            segment_distance,
            speed,
            is_downhill
        )
        
        # Calculate cliff fall risk
        cliff = vehicle.calculate_cliff_fall_risk(
            cliff_present, guardrail, road_width, visibility, speed, stability['stability_risk']
        )
        
        # Calculate landslide risk
        landslide = EnvironmentalHazards.calculate_landslide_risk(
            slope_pct,
            environment['Rainfall_mm'],
            environment['Soil_Type'],
            environment['Landslide_Risk_Base']
        )
        
        # Combine all risks
        base_combined_risk = (
            stability['stability_risk'] * 0.25 +
            brake['brake_failure_risk'] * 0.30 +
            cliff['cliff_fall_risk'] * 0.25 +
            landslide['landslide_risk'] * 0.20
        )
        
        # Adjust for driver behavior
        driver_adjusted = EnvironmentalHazards.adjust_for_driver_behavior(
            base_combined_risk, **driver_behavior
        )
        
        results.append({
            'Segment': segment_id,
            'Distance_km': segment['Distance(KM)'],
            'Elevation_m': segment['Elevation(M)'],
            'Slope_pct': slope_pct,
            'Is_Downhill': is_downhill,
            'Stability_Risk': stability['stability_risk'],
            'Brake_Failure_Risk': brake['brake_failure_risk'],
            'Brake_Temperature_C': brake['brake_temperature'],
            'Cliff_Fall_Risk': cliff['cliff_fall_risk'],
            'Landslide_Risk': landslide['landslide_risk'],
            'Combined_Risk': base_combined_risk,
            'Final_Risk': driver_adjusted['adjusted_risk'],
            'Safe_Speed_Recommendation': stability['safe_speed_recommendation'],
            'Risk_Category': segment['Risk'],
            'Brake_Status': brake['status'],
            'Cliff_Severity': cliff['severity'],
            'Landslide_Category': landslide['risk_category']
        })
    
    return pd.DataFrame(results)
