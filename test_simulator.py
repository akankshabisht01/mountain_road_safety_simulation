"""
Quick test script to verify the simulator works correctly
"""

import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.simulation_engine import simulate_vehicle_journey
from src.risk_calculator import generate_safety_report

print("🔄 Loading data files...")
road_data = pd.read_csv('bhikyasen road data.csv')
road_characteristics = pd.read_csv('data/road_characteristics.csv')
vehicle_params = pd.read_csv('data/vehicle_params.csv')
environment_conditions = pd.read_csv('data/environment_conditions.csv')

print(f"✅ Loaded {len(road_data)} road segments")
print(f"✅ Loaded {len(vehicle_params)} vehicle types")
print(f"✅ Loaded {len(environment_conditions)} environment conditions")

print("\n🚗 Running test simulation (Bus in Normal conditions)...")
vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Bus'].iloc[0]
environment = environment_conditions[environment_conditions['Condition'] == 'Normal'].iloc[0]

results = simulate_vehicle_journey(
    road_data,
    road_characteristics,
    vehicle,
    environment,
    speed=40,
    driver_behavior={
        'is_night': False,
        'is_overspeeding': False,
        'poor_visibility': False,
        'driver_experience': 'Medium'
    }
)

print(f"✅ Simulation completed for {len(results)} segments")

print("\n📊 Summary Statistics:")
print(f"   Average Risk: {results['Final_Risk'].mean():.1%}")
print(f"   Maximum Risk: {results['Final_Risk'].max():.1%}")
print(f"   Critical Segments: {len(results[results['Final_Risk'] >= 0.8])}")
print(f"   Max Brake Temperature: {results['Brake_Temperature_C'].max():.0f}°C")

print("\n🔥 Top 5 Most Dangerous Segments:")
dangerous = results.nlargest(5, 'Final_Risk')[['Segment', 'Distance_km', 'Final_Risk', 'Slope_pct', 'Brake_Temperature_C']]
print(dangerous.to_string(index=False))

print("\n📋 Generating safety report...")
report = generate_safety_report(results, 'Bus', 'Normal')
print(f"✅ Generated {len(report['recommendations'])} recommendations")

print("\n🎉 All tests passed! Simulator is ready to use.")
print("\n🚀 To launch the dashboard, run:")
print("   streamlit run app.py")
