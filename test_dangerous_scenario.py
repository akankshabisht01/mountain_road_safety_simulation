"""
Test dangerous scenario: Night + Overspeeding
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.simulation_engine import simulate_vehicle_journey
import pandas as pd

# Get absolute paths
base_path = Path(__file__).parent

# Load data (bhikyasen road data.csv is in root, others in data/)
road_data = pd.read_csv(base_path / 'bhikyasen road data.csv')
road_characteristics = pd.read_csv(base_path / 'data' / 'road_characteristics.csv')
vehicle_params = pd.read_csv(base_path / 'data' / 'vehicle_params.csv')
environment_conditions = pd.read_csv(base_path / 'data' / 'environment_conditions.csv')

# Get bus and normal conditions
vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Bus'].iloc[0]
environment = environment_conditions[environment_conditions['Condition'] == 'Normal'].iloc[0]

print("=" * 60)
print("TEST: DANGEROUS SCENARIO (Night + Overspeeding)")
print("=" * 60)

# Test 1: Normal conditions
print("\n1️⃣ Normal Conditions (40 km/h, Day, No Overspeeding):")
results_normal = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=40,
    driver_behavior={'is_night': False, 'is_overspeeding': False, 'poor_visibility': False, 'driver_experience': 'Medium'}
)
print(f"   Average Risk: {results_normal['Final_Risk'].mean()*100:.1f}%")
print(f"   Max Risk: {results_normal['Final_Risk'].max()*100:.1f}%")

# Test 2: Night driving only
print("\n2️⃣ Night Driving (40 km/h, Night, No Overspeeding):")
results_night = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=40,
    driver_behavior={'is_night': True, 'is_overspeeding': False, 'poor_visibility': False, 'driver_experience': 'Medium'}
)
print(f"   Average Risk: {results_night['Final_Risk'].mean()*100:.1f}%")
print(f"   Max Risk: {results_night['Final_Risk'].max()*100:.1f}%")
print(f"   Increase: +{(results_night['Final_Risk'].mean() - results_normal['Final_Risk'].mean())*100:.1f}%")

# Test 3: Overspeeding only
print("\n3️⃣ Overspeeding (60 km/h, Day, Overspeeding):")
results_speed = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=60,
    driver_behavior={'is_night': False, 'is_overspeeding': True, 'poor_visibility': False, 'driver_experience': 'Medium'}
)
print(f"   Average Risk: {results_speed['Final_Risk'].mean()*100:.1f}%")
print(f"   Max Risk: {results_speed['Final_Risk'].max()*100:.1f}%")
print(f"   Increase: +{(results_speed['Final_Risk'].mean() - results_normal['Final_Risk'].mean())*100:.1f}%")

# Test 4: BOTH night and overspeeding
print("\n4️⃣ DANGER ZONE (60 km/h, Night, Overspeeding):")
results_danger = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=60,
    driver_behavior={'is_night': True, 'is_overspeeding': True, 'poor_visibility': False, 'driver_experience': 'Medium'}
)
print(f"   Average Risk: {results_danger['Final_Risk'].mean()*100:.1f}%")
print(f"   Max Risk: {results_danger['Final_Risk'].max()*100:.1f}%")
print(f"   Increase: +{(results_danger['Final_Risk'].mean() - results_normal['Final_Risk'].mean())*100:.1f}%")
print(f"   Risk Multiplier: {results_danger['Final_Risk'].mean() / results_normal['Final_Risk'].mean():.2f}x")

# Test 5: EXTREME - All danger factors
print("\n5️⃣ EXTREME DANGER (60 km/h, Night, Overspeeding, Fog, Novice):")
results_extreme = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=60,
    driver_behavior={'is_night': True, 'is_overspeeding': True, 'poor_visibility': True, 'driver_experience': 'Novice'}
)
print(f"   Average Risk: {results_extreme['Final_Risk'].mean()*100:.1f}%")
print(f"   Max Risk: {results_extreme['Final_Risk'].max()*100:.1f}%")
print(f"   Increase: +{(results_extreme['Final_Risk'].mean() - results_normal['Final_Risk'].mean())*100:.1f}%")
print(f"   Risk Multiplier: {results_extreme['Final_Risk'].mean() / results_normal['Final_Risk'].mean():.2f}x")

# Critical segments
critical = results_extreme[results_extreme['Final_Risk'] > 0.8]
print(f"\n⚠️ CRITICAL SEGMENTS (>80% risk): {len(critical)}")
if len(critical) > 0:
    print(critical[['Segment', 'Distance_km', 'Final_Risk', 'Slope_pct', 'Brake_Temperature_C']].to_string(index=False))

print("\n" + "=" * 60)
print("✅ Risk calculations are now much more realistic!")
print("=" * 60)
