"""
Mountain Road Safety Simulator - Risk Analysis & Recommendations Engine
Provides comprehensive risk assessment and actionable safety recommendations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class RiskFusionEngine:
    """Combines multiple risk factors into comprehensive safety scores"""
    
    def __init__(self):
        self.risk_weights = {
            'stability': 0.25,
            'brake_failure': 0.30,
            'cliff_fall': 0.25,
            'landslide': 0.20
        }
    
    def calculate_overall_risk(self, risk_scores: Dict[str, float]) -> Dict:
        """
        Combine individual risk scores into overall risk assessment
        
        Args:
            risk_scores: Dictionary with individual risk scores
            
        Returns:
            Dictionary with overall risk and classification
        """
        weighted_risk = (
            risk_scores.get('stability', 0) * self.risk_weights['stability'] +
            risk_scores.get('brake_failure', 0) * self.risk_weights['brake_failure'] +
            risk_scores.get('cliff_fall', 0) * self.risk_weights['cliff_fall'] +
            risk_scores.get('landslide', 0) * self.risk_weights['landslide']
        )
        
        # Risk classification
        if weighted_risk >= 0.8:
            classification = 'CRITICAL'
            color = '#8B0000'  # Dark Red
            action = 'IMMEDIATE ACTION REQUIRED'
        elif weighted_risk >= 0.6:
            classification = 'EXTREME'
            color = '#FF0000'  # Red
            action = 'HIGH PRIORITY INTERVENTION'
        elif weighted_risk >= 0.4:
            classification = 'HIGH'
            color = '#FF8C00'  # Orange
            action = 'SAFETY MEASURES NEEDED'
        elif weighted_risk >= 0.25:
            classification = 'MEDIUM'
            color = '#FFD700'  # Yellow
            action = 'MONITORING REQUIRED'
        else:
            classification = 'LOW'
            color = '#32CD32'  # Green
            action = 'ACCEPTABLE RISK'
        
        return {
            'overall_risk': weighted_risk,
            'risk_classification': classification,
            'color_code': color,
            'action_priority': action,
            'primary_risk_factor': max(risk_scores, key=risk_scores.get)
        }
    
    def identify_dangerous_zones(self, simulation_results: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Identify the most dangerous road segments
        
        Args:
            simulation_results: DataFrame with simulation results
            top_n: Number of top dangerous zones to return
            
        Returns:
            DataFrame with top dangerous segments
        """
        dangerous = simulation_results.nlargest(top_n, 'Final_Risk').copy()
        
        # Add danger reasons
        def identify_danger_reasons(row):
            reasons = []
            if row['Brake_Failure_Risk'] > 0.6:
                reasons.append(f"Brake failure risk ({row['Brake_Temperature_C']:.0f}°C)")
            if row['Cliff_Fall_Risk'] > 0.6:
                reasons.append("High cliff fall risk")
            if row['Landslide_Risk'] > 0.6:
                reasons.append(f"Landslide prone ({row['Landslide_Category']})")
            if row['Stability_Risk'] > 0.6:
                reasons.append("Vehicle stability issues")
            if row['Slope_pct'] > 25:
                reasons.append(f"Extreme slope ({row['Slope_pct']:.1f}%)")
            return '; '.join(reasons) if reasons else 'Multiple factors'
        
        dangerous['Danger_Reasons'] = dangerous.apply(identify_danger_reasons, axis=1)
        
        return dangerous[['Segment', 'Distance_km', 'Final_Risk', 'Slope_pct', 
                          'Brake_Temperature_C', 'Danger_Reasons']]
    
    def calculate_risk_statistics(self, simulation_results: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive risk statistics for the entire road
        
        Args:
            simulation_results: DataFrame with simulation results
            
        Returns:
            Dictionary with statistical metrics
        """
        return {
            'total_segments': len(simulation_results),
            'critical_segments': len(simulation_results[simulation_results['Final_Risk'] >= 0.8]),
            'extreme_segments': len(simulation_results[simulation_results['Final_Risk'] >= 0.6]),
            'high_risk_segments': len(simulation_results[simulation_results['Final_Risk'] >= 0.4]),
            'average_risk': simulation_results['Final_Risk'].mean(),
            'max_risk': simulation_results['Final_Risk'].max(),
            'max_risk_segment': simulation_results.loc[simulation_results['Final_Risk'].idxmax(), 'Segment'],
            'max_brake_temp': simulation_results['Brake_Temperature_C'].max(),
            'brake_critical_segments': len(simulation_results[simulation_results['Brake_Temperature_C'] > 250]),
            'cliff_zones': len(simulation_results[simulation_results['Cliff_Fall_Risk'] > 0.5]),
            'landslide_zones': len(simulation_results[simulation_results['Landslide_Risk'] > 0.5])
        }


class SafetyRecommendationEngine:
    """Generates actionable safety recommendations based on risk analysis"""
    
    @staticmethod
    def generate_segment_recommendations(segment_data: pd.Series) -> List[Dict]:
        """
        Generate specific recommendations for a road segment
        
        Args:
            segment_data: Series with segment risk data
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Brake failure recommendations
        if segment_data['Brake_Failure_Risk'] > 0.6:
            recommendations.append({
                'type': 'INFRASTRUCTURE',
                'priority': 'CRITICAL',
                'recommendation': 'Install emergency escape ramp',
                'reason': f"High brake failure risk (Temp: {segment_data['Brake_Temperature_C']:.0f}°C)",
                'estimated_cost': 'High (₹50-80 lakhs)',
                'implementation_time': '3-6 months'
            })
            recommendations.append({
                'type': 'SIGNAGE',
                'priority': 'HIGH',
                'recommendation': 'Install brake temperature warning signs',
                'reason': 'Warn drivers of extended downhill section',
                'estimated_cost': 'Low (₹50,000-1 lakh)',
                'implementation_time': '1-2 weeks'
            })
        elif segment_data['Brake_Failure_Risk'] > 0.4:
            recommendations.append({
                'type': 'SIGNAGE',
                'priority': 'MEDIUM',
                'recommendation': 'Install "Use Low Gear" advisory signs',
                'reason': 'Moderate brake stress on downhill',
                'estimated_cost': 'Low (₹30,000-50,000)',
                'implementation_time': '1 week'
            })
        
        # Cliff fall recommendations
        if segment_data['Cliff_Fall_Risk'] > 0.6:
            recommendations.append({
                'type': 'INFRASTRUCTURE',
                'priority': 'CRITICAL',
                'recommendation': 'Install/upgrade guardrails immediately',
                'reason': f"Extreme cliff fall risk - {segment_data['Cliff_Severity']}",
                'estimated_cost': 'High (₹20-30 lakhs per km)',
                'implementation_time': '2-4 months'
            })
            recommendations.append({
                'type': 'TRAFFIC_MANAGEMENT',
                'priority': 'HIGH',
                'recommendation': 'Implement speed limit of 20-25 km/h',
                'reason': 'Reduce risk in cliff zone',
                'estimated_cost': 'Low (₹20,000-30,000)',
                'implementation_time': 'Immediate'
            })
        
        # Landslide recommendations
        if segment_data['Landslide_Risk'] > 0.6:
            recommendations.append({
                'type': 'MONITORING',
                'priority': 'CRITICAL',
                'recommendation': 'Install real-time landslide monitoring system',
                'reason': f"High landslide risk - {segment_data['Landslide_Category']}",
                'estimated_cost': 'Medium (₹10-20 lakhs)',
                'implementation_time': '1-2 months'
            })
            recommendations.append({
                'type': 'INFRASTRUCTURE',
                'priority': 'HIGH',
                'recommendation': 'Construct retaining walls and drainage',
                'reason': 'Stabilize slope and prevent soil erosion',
                'estimated_cost': 'Very High (₹1-2 crores)',
                'implementation_time': '6-12 months'
            })
        
        # Stability/curve recommendations
        if segment_data['Stability_Risk'] > 0.5:
            recommendations.append({
                'type': 'INFRASTRUCTURE',
                'priority': 'HIGH',
                'recommendation': 'Widen road and improve banking on curves',
                'reason': 'Improve vehicle stability on sharp curves',
                'estimated_cost': 'High (₹40-60 lakhs per km)',
                'implementation_time': '4-6 months'
            })
            recommendations.append({
                'type': 'SIGNAGE',
                'priority': 'MEDIUM',
                'recommendation': 'Install curve warning signs with speed advisory',
                'reason': 'Alert drivers to dangerous curve ahead',
                'estimated_cost': 'Low (₹40,000-60,000)',
                'implementation_time': '1 week'
            })
        
        # Speed recommendations
        if segment_data['Safe_Speed_Recommendation'] < 30:
            recommendations.append({
                'type': 'TRAFFIC_MANAGEMENT',
                'priority': 'HIGH',
                'recommendation': f"Enforce strict speed limit: {int(segment_data['Safe_Speed_Recommendation'])} km/h",
                'reason': 'Extremely dangerous segment requires reduced speed',
                'estimated_cost': 'Low (₹50,000-1 lakh)',
                'implementation_time': 'Immediate'
            })
        
        return recommendations
    
    @staticmethod
    def generate_road_level_recommendations(simulation_results: pd.DataFrame, 
                                             risk_stats: Dict) -> List[Dict]:
        """
        Generate recommendations for the entire road
        
        Args:
            simulation_results: Complete simulation results
            risk_stats: Risk statistics dictionary
            
        Returns:
            List of road-level recommendations
        """
        recommendations = []
        
        # Overall critical zones
        if risk_stats['critical_segments'] > 5:
            recommendations.append({
                'scope': 'ROAD-WIDE',
                'priority': 'CRITICAL',
                'recommendation': 'Comprehensive road safety audit and immediate intervention',
                'reason': f"{risk_stats['critical_segments']} critical danger zones identified",
                'estimated_cost': 'Very High (₹5-10 crores)',
                'implementation_time': '12-24 months'
            })
        
        # Brake failure zones
        if risk_stats['brake_critical_segments'] > 3:
            recommendations.append({
                'scope': 'ROAD-WIDE',
                'priority': 'HIGH',
                'recommendation': 'Install 2-3 emergency escape ramps at strategic locations',
                'reason': f"Multiple brake overheating zones detected (Max: {risk_stats['max_brake_temp']:.0f}°C)",
                'estimated_cost': 'High (₹1.5-2.5 crores)',
                'implementation_time': '6-9 months'
            })
            recommendations.append({
                'scope': 'OPERATIONAL',
                'priority': 'MEDIUM',
                'recommendation': 'Mandatory brake check stations before steep descents',
                'reason': 'Prevent brake-related accidents',
                'estimated_cost': 'Medium (₹30-50 lakhs)',
                'implementation_time': '2-3 months'
            })
        
        # Cliff zones
        if risk_stats['cliff_zones'] > 10:
            recommendations.append({
                'scope': 'ROAD-WIDE',
                'priority': 'CRITICAL',
                'recommendation': 'Phased guardrail installation program for all cliff zones',
                'reason': f"{risk_stats['cliff_zones']} segments with high cliff fall risk",
                'estimated_cost': 'Very High (₹2-4 crores)',
                'implementation_time': '8-12 months'
            })
        
        # Landslide zones
        if risk_stats['landslide_zones'] > 5:
            recommendations.append({
                'scope': 'ROAD-WIDE',
                'priority': 'HIGH',
                'recommendation': 'Implement real-time weather-based road closure system',
                'reason': f"{risk_stats['landslide_zones']} landslide-prone segments",
                'estimated_cost': 'Medium (₹50-80 lakhs)',
                'implementation_time': '3-4 months'
            })
            recommendations.append({
                'scope': 'OPERATIONAL',
                'priority': 'HIGH',
                'recommendation': 'Restrict traffic during heavy rainfall (>50mm/day)',
                'reason': 'Prevent landslide-related accidents',
                'estimated_cost': 'Low (₹10-20 lakhs)',
                'implementation_time': 'Immediate'
            })
        
        # General safety
        recommendations.append({
            'scope': 'OPERATIONAL',
            'priority': 'HIGH',
            'recommendation': 'Deploy mobile safety patrol units during peak hours',
            'reason': 'Quick response to accidents and hazards',
            'estimated_cost': 'Medium (₹40-60 lakhs annually)',
            'implementation_time': '1 month'
        })
        
        recommendations.append({
            'scope': 'AWARENESS',
            'priority': 'MEDIUM',
            'recommendation': 'Conduct driver awareness campaigns for mountain driving',
            'reason': 'Educate drivers on safe mountain driving practices',
            'estimated_cost': 'Low (₹10-20 lakhs)',
            'implementation_time': 'Ongoing'
        })
        
        return recommendations
    
    @staticmethod
    def prioritize_interventions(all_recommendations: List[Dict], budget_limit: float = None) -> pd.DataFrame:
        """
        Prioritize recommendations based on priority and budget
        
        Args:
            all_recommendations: List of all recommendations
            budget_limit: Optional budget constraint in crores
            
        Returns:
            DataFrame with prioritized recommendations
        """
        priority_order = {'CRITICAL': 1, 'HIGH': 2, 'MEDIUM': 3, 'LOW': 4}
        
        for rec in all_recommendations:
            rec['priority_rank'] = priority_order.get(rec['priority'], 5)
        
        df = pd.DataFrame(all_recommendations)
        df = df.sort_values('priority_rank')
        
        return df


def generate_safety_report(simulation_results: pd.DataFrame,
                           vehicle_type: str,
                           environment_condition: str) -> Dict:
    """
    Generate comprehensive safety report for the road
    
    Args:
        simulation_results: Complete simulation results
        vehicle_type: Type of vehicle simulated
        environment_condition: Environmental condition name
        
    Returns:
        Dictionary with complete safety report
    """
    risk_engine = RiskFusionEngine()
    safety_engine = SafetyRecommendationEngine()
    
    # Calculate statistics
    stats = risk_engine.calculate_risk_statistics(simulation_results)
    
    # Identify dangerous zones
    dangerous_zones = risk_engine.identify_dangerous_zones(simulation_results, top_n=10)
    
    # Generate recommendations for top dangerous segments
    segment_recommendations = []
    for _, segment in dangerous_zones.head(5).iterrows():
        recs = safety_engine.generate_segment_recommendations(simulation_results.iloc[segment['Segment']-1])
        for rec in recs:
            rec['segment'] = segment['Segment']
            rec['distance_km'] = segment['Distance_km']
            segment_recommendations.append(rec)
    
    # Generate road-level recommendations
    road_recommendations = safety_engine.generate_road_level_recommendations(simulation_results, stats)
    
    # Combine all recommendations
    all_recommendations = segment_recommendations + road_recommendations
    prioritized = safety_engine.prioritize_interventions(all_recommendations)
    
    return {
        'vehicle_type': vehicle_type,
        'environment_condition': environment_condition,
        'statistics': stats,
        'dangerous_zones': dangerous_zones,
        'recommendations': prioritized,
        'executive_summary': {
            'total_risk_score': stats['average_risk'],
            'critical_action_items': len(prioritized[prioritized['priority'] == 'CRITICAL']),
            'most_dangerous_segment': stats['max_risk_segment'],
            'key_hazards': [
                f"Brake failure risk in {stats['brake_critical_segments']} segments",
                f"Cliff fall danger in {stats['cliff_zones']} zones",
                f"Landslide risk in {stats['landslide_zones']} areas"
            ]
        }
    }
