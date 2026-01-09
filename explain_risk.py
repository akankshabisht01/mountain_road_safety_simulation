"""
Explain what 14.5% risk means in realistic terms
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.simulation_engine import simulate_vehicle_journey
import pandas as pd

base_path = Path(__file__).parent

# Load data
road_data = pd.read_csv(base_path / 'bhikyasen road data.csv')
road_characteristics = pd.read_csv(base_path / 'data' / 'road_characteristics.csv')
vehicle_params = pd.read_csv(base_path / 'data' / 'vehicle_params.csv')
environment_conditions = pd.read_csv(base_path / 'data' / 'environment_conditions.csv')

# Get CAR and Winter conditions (matching user's settings)
vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Car'].iloc[0]
environment = environment_conditions[environment_conditions['Condition'] == 'Winter'].iloc[0]

print("="*70)
print("🚗 YOUR CURRENT SETTINGS:")
print("="*70)
print(f"Vehicle: Car")
print(f"Max Safe Speed for Car: {vehicle['Max_Safe_Speed_Hills_kmh']} km/h")
print(f"Your Speed: 75 km/h")
print(f"⚠️ YOU ARE OVERSPEEDING BY: {75 - vehicle['Max_Safe_Speed_Hills_kmh']} km/h!")
print(f"Weather: Winter")
print(f"Night Driving: YES")
print(f"Overspeeding Checkbox: NO (but you ARE overspeeding!)")
print()

# Simulate WITHOUT overspeeding checkbox (what you're seeing now)
print("="*70)
print("❌ CURRENT (Overspeeding checkbox NOT checked):")
print("="*70)
results_no_flag = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=75,
    driver_behavior={'is_night': True, 'is_overspeeding': False, 'poor_visibility': False, 'driver_experience': 'Medium'}
)
avg_risk_no_flag = results_no_flag['Final_Risk'].mean() * 100
max_risk_no_flag = results_no_flag['Final_Risk'].max() * 100
critical_no_flag = len(results_no_flag[results_no_flag['Final_Risk'] >= 0.8])

print(f"Average Risk: {avg_risk_no_flag:.1f}%")
print(f"Max Risk: {max_risk_no_flag:.1f}%")
print(f"Critical Segments: {critical_no_flag}")
print()

# Simulate WITH overspeeding checkbox (what it SHOULD be)
print("="*70)
print("✅ CORRECT (Overspeeding checkbox CHECKED):")
print("="*70)
results_with_flag = simulate_vehicle_journey(
    road_data, road_characteristics, vehicle, environment, 
    speed=75,
    driver_behavior={'is_night': True, 'is_overspeeding': True, 'poor_visibility': False, 'driver_experience': 'Medium'}
)
avg_risk_with_flag = results_with_flag['Final_Risk'].mean() * 100
max_risk_with_flag = results_with_flag['Final_Risk'].max() * 100
critical_with_flag = len(results_with_flag[results_with_flag['Final_Risk'] >= 0.8])

print(f"Average Risk: {avg_risk_with_flag:.1f}%")
print(f"Max Risk: {max_risk_with_flag:.1f}%")
print(f"Critical Segments: {critical_with_flag}")
print(f"Risk Increase: +{avg_risk_with_flag - avg_risk_no_flag:.1f}%")
print()

print("="*70)
print("📊 WHAT DOES THIS MEAN IN REAL TERMS?")
print("="*70)
print(f"• If 100 cars drive this road in your conditions...")
print(f"  WITHOUT overspeeding penalty: ~{int(avg_risk_no_flag)} cars face serious danger")
print(f"  WITH overspeeding penalty: ~{int(avg_risk_with_flag)} cars face serious danger")
print()
print(f"• Your REAL risk: {avg_risk_with_flag:.1f}% average")
print(f"  - This means: MODERATE to HIGH danger level")
print(f"  - {critical_with_flag} segments are CRITICAL (>80% risk)")
print(f"  - Maximum danger point reaches: {max_risk_with_flag:.1f}%")
print()

print("="*70)
print("⚠️ THE PROBLEM:")
print("="*70)
print("The 'Overspeeding' checkbox is MANUAL - it doesn't auto-detect!")
print(f"You're going 75 km/h but safe speed is {vehicle['Max_Safe_Speed_Hills_kmh']} km/h")
print("You MUST check the 'Overspeeding' box to get accurate risk!")
print()
print("Let me fix this to AUTO-DETECT overspeeding...")
print("="*70)
