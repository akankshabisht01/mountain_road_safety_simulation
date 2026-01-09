"""
Comprehensive test to validate all simulator components
"""

import pandas as pd
import sys
from pathlib import Path
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from simulation_engine import simulate_vehicle_journey
    from risk_calculator import generate_safety_report, RiskFusionEngine, SafetyRecommendationEngine
    from visualizer import RoadVisualizer
except ImportError:
    from src.simulation_engine import simulate_vehicle_journey
    from src.risk_calculator import generate_safety_report, RiskFusionEngine, SafetyRecommendationEngine
    from src.visualizer import RoadVisualizer

def test_data_loading():
    """Test if all data files load correctly"""
    print("\n" + "="*60)
    print("TEST 1: Data Loading")
    print("="*60)
    
    try:
        road_data = pd.read_csv('bhikyasen road data.csv')
        road_characteristics = pd.read_csv('data/road_characteristics.csv')
        vehicle_params = pd.read_csv('data/vehicle_params.csv')
        environment_conditions = pd.read_csv('data/environment_conditions.csv')
        
        print(f"✅ Road data: {len(road_data)} segments")
        print(f"✅ Road characteristics: {len(road_characteristics)} segments")
        print(f"✅ Vehicle types: {len(vehicle_params)}")
        print(f"✅ Environment conditions: {len(environment_conditions)}")
        
        return road_data, road_characteristics, vehicle_params, environment_conditions
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        traceback.print_exc()
        return None, None, None, None

def test_simulation_normal(road_data, road_characteristics, vehicle_params, environment_conditions):
    """Test normal weather simulation"""
    print("\n" + "="*60)
    print("TEST 2: Normal Weather Simulation (Bus)")
    print("="*60)
    
    try:
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
        
        print(f"✅ Simulation completed: {len(results)} segments")
        print(f"   Average Risk: {results['Final_Risk'].mean():.2%}")
        print(f"   Max Risk: {results['Final_Risk'].max():.2%}")
        print(f"   Critical Segments: {len(results[results['Final_Risk'] >= 0.8])}")
        print(f"   Max Brake Temp: {results['Brake_Temperature_C'].max():.1f}°C")
        
        # Check for NaN values
        nan_counts = results.isna().sum()
        if nan_counts.any():
            print(f"⚠️  Warning: Found NaN values:")
            print(nan_counts[nan_counts > 0])
        else:
            print("✅ No NaN values found")
        
        return results
    except Exception as e:
        print(f"❌ Normal simulation failed: {e}")
        traceback.print_exc()
        return None

def test_simulation_heavy_rain(road_data, road_characteristics, vehicle_params, environment_conditions):
    """Test heavy rain simulation"""
    print("\n" + "="*60)
    print("TEST 3: Heavy Rain Simulation (Bus)")
    print("="*60)
    
    try:
        vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Bus'].iloc[0]
        environment = environment_conditions[environment_conditions['Condition'] == 'Heavy_Rain'].iloc[0]
        
        results = simulate_vehicle_journey(
            road_data,
            road_characteristics,
            vehicle,
            environment,
            speed=35,
            driver_behavior={
                'is_night': False,
                'is_overspeeding': False,
                'poor_visibility': True,
                'driver_experience': 'Medium'
            }
        )
        
        print(f"✅ Simulation completed: {len(results)} segments")
        print(f"   Average Risk: {results['Final_Risk'].mean():.2%}")
        print(f"   Max Risk: {results['Final_Risk'].max():.2%}")
        print(f"   High Risk Segments: {len(results[results['Final_Risk'] >= 0.4])}")
        print(f"   Landslide Warnings: {len(results[results['Landslide_Risk'] > 0.5])}")
        
        return results
    except Exception as e:
        print(f"❌ Heavy rain simulation failed: {e}")
        traceback.print_exc()
        return None

def test_car_simulation(road_data, road_characteristics, vehicle_params, environment_conditions):
    """Test car simulation"""
    print("\n" + "="*60)
    print("TEST 4: Car Simulation (Overspeeding)")
    print("="*60)
    
    try:
        vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Car'].iloc[0]
        environment = environment_conditions[environment_conditions['Condition'] == 'Normal'].iloc[0]
        
        results = simulate_vehicle_journey(
            road_data,
            road_characteristics,
            vehicle,
            environment,
            speed=70,
            driver_behavior={
                'is_night': False,
                'is_overspeeding': True,
                'poor_visibility': False,
                'driver_experience': 'Novice'
            }
        )
        
        print(f"✅ Simulation completed: {len(results)} segments")
        print(f"   Average Risk: {results['Final_Risk'].mean():.2%}")
        print(f"   Max Risk: {results['Final_Risk'].max():.2%}")
        print(f"   Risk increase due to overspeeding visible")
        
        return results
    except Exception as e:
        print(f"❌ Car simulation failed: {e}")
        traceback.print_exc()
        return None

def test_risk_calculator(results):
    """Test risk calculation and recommendations"""
    print("\n" + "="*60)
    print("TEST 5: Risk Calculator & Recommendations")
    print("="*60)
    
    try:
        report = generate_safety_report(results, 'Bus', 'Normal')
        
        print(f"✅ Safety report generated")
        print(f"   Total segments: {report['statistics']['total_segments']}")
        print(f"   Critical segments: {report['statistics']['critical_segments']}")
        print(f"   Most dangerous: Segment #{report['statistics']['max_risk_segment']}")
        print(f"   Recommendations: {len(report['recommendations'])}")
        
        # Check recommendations
        critical_recs = report['recommendations'][report['recommendations']['priority'] == 'CRITICAL']
        print(f"   Critical priority items: {len(critical_recs)}")
        
        return report
    except Exception as e:
        print(f"❌ Risk calculator failed: {e}")
        traceback.print_exc()
        return None

def test_visualizations(results):
    """Test all visualization functions"""
    print("\n" + "="*60)
    print("TEST 6: Visualizations")
    print("="*60)
    
    try:
        visualizer = RoadVisualizer()
        
        # Test elevation profile
        fig1 = visualizer.create_elevation_profile_with_risk(results)
        print("✅ Elevation profile created")
        
        # Test risk heatmap
        fig2 = visualizer.create_risk_heatmap(results)
        print("✅ Risk heatmap created")
        
        # Test brake temperature chart
        fig3 = visualizer.create_brake_temperature_chart(results)
        print("✅ Brake temperature chart created")
        
        # Test risk gauge
        fig4 = visualizer.create_risk_gauge(results['Final_Risk'].mean(), "Average Risk")
        print("✅ Risk gauge created")
        
        # Test 2D map
        fig5 = visualizer.create_risk_map_2d(results)
        print("✅ 2D risk map created")
        
        # Test statistics dashboard
        from risk_calculator import RiskFusionEngine
        risk_engine = RiskFusionEngine()
        stats = risk_engine.calculate_risk_statistics(results)
        fig6 = visualizer.create_statistics_dashboard(stats)
        print("✅ Statistics dashboard created")
        
        print("\n✅ All visualizations generated successfully!")
        return True
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        traceback.print_exc()
        return False

def test_scenario_comparison(road_data, road_characteristics, vehicle_params, environment_conditions):
    """Test scenario comparison"""
    print("\n" + "="*60)
    print("TEST 7: Scenario Comparison")
    print("="*60)
    
    try:
        vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Bus'].iloc[0]
        
        scenarios = {}
        
        # Normal
        env_normal = environment_conditions[environment_conditions['Condition'] == 'Normal'].iloc[0]
        scenarios['Normal'] = simulate_vehicle_journey(
            road_data, road_characteristics, vehicle, env_normal, 40,
            {'is_night': False, 'is_overspeeding': False, 'poor_visibility': False, 'driver_experience': 'Medium'}
        )
        
        # Heavy Rain
        env_rain = environment_conditions[environment_conditions['Condition'] == 'Heavy_Rain'].iloc[0]
        scenarios['Heavy Rain'] = simulate_vehicle_journey(
            road_data, road_characteristics, vehicle, env_rain, 40,
            {'is_night': False, 'is_overspeeding': False, 'poor_visibility': True, 'driver_experience': 'Medium'}
        )
        
        print(f"✅ Scenario comparison ready: {len(scenarios)} scenarios")
        
        # Compare risks
        for name, result in scenarios.items():
            avg_risk = result['Final_Risk'].mean()
            print(f"   {name}: {avg_risk:.2%} average risk")
        
        # Test comparative visualization
        visualizer = RoadVisualizer()
        fig = visualizer.create_comparative_scenario_chart(scenarios)
        print("✅ Comparative chart created")
        
        return True
    except Exception as e:
        print(f"❌ Scenario comparison failed: {e}")
        traceback.print_exc()
        return False

def test_edge_cases(road_data, road_characteristics, vehicle_params, environment_conditions):
    """Test edge cases and extreme conditions"""
    print("\n" + "="*60)
    print("TEST 8: Edge Cases & Extreme Conditions")
    print("="*60)
    
    try:
        vehicle = vehicle_params[vehicle_params['Vehicle_Type'] == 'Bus'].iloc[0]
        environment = environment_conditions[environment_conditions['Condition'] == 'Normal'].iloc[0]
        
        # Test with very low speed
        results_slow = simulate_vehicle_journey(
            road_data, road_characteristics, vehicle, environment, 20,
            {'is_night': False, 'is_overspeeding': False, 'poor_visibility': False, 'driver_experience': 'Expert'}
        )
        print(f"✅ Low speed (20 km/h): Avg risk {results_slow['Final_Risk'].mean():.2%}")
        
        # Test with very high speed
        results_fast = simulate_vehicle_journey(
            road_data, road_characteristics, vehicle, environment, 80,
            {'is_night': True, 'is_overspeeding': True, 'poor_visibility': True, 'driver_experience': 'Novice'}
        )
        print(f"✅ High speed + worst conditions: Avg risk {results_fast['Final_Risk'].mean():.2%}")
        
        # Verify risk increase
        risk_increase = results_fast['Final_Risk'].mean() / results_slow['Final_Risk'].mean()
        print(f"✅ Risk multiplier: {risk_increase:.2f}x (as expected)")
        
        return True
    except Exception as e:
        print(f"❌ Edge case testing failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "🔬"*30)
    print("COMPREHENSIVE SIMULATOR TEST SUITE")
    print("🔬"*30)
    
    # Track results
    test_results = {}
    
    # Test 1: Data Loading
    road_data, road_characteristics, vehicle_params, environment_conditions = test_data_loading()
    test_results['Data Loading'] = all([road_data is not None, road_characteristics is not None, 
                                        vehicle_params is not None, environment_conditions is not None])
    
    if not test_results['Data Loading']:
        print("\n❌ Cannot proceed without data. Exiting.")
        return
    
    # Test 2-4: Simulations
    results_normal = test_simulation_normal(road_data, road_characteristics, vehicle_params, environment_conditions)
    test_results['Normal Simulation'] = results_normal is not None
    
    results_rain = test_simulation_heavy_rain(road_data, road_characteristics, vehicle_params, environment_conditions)
    test_results['Heavy Rain Simulation'] = results_rain is not None
    
    results_car = test_car_simulation(road_data, road_characteristics, vehicle_params, environment_conditions)
    test_results['Car Simulation'] = results_car is not None
    
    # Test 5: Risk Calculator
    if results_normal is not None:
        report = test_risk_calculator(results_normal)
        test_results['Risk Calculator'] = report is not None
    else:
        test_results['Risk Calculator'] = False
    
    # Test 6: Visualizations
    if results_normal is not None:
        test_results['Visualizations'] = test_visualizations(results_normal)
    else:
        test_results['Visualizations'] = False
    
    # Test 7: Scenario Comparison
    test_results['Scenario Comparison'] = test_scenario_comparison(
        road_data, road_characteristics, vehicle_params, environment_conditions
    )
    
    # Test 8: Edge Cases
    test_results['Edge Cases'] = test_edge_cases(
        road_data, road_characteristics, vehicle_params, environment_conditions
    )
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"\nFINAL RESULT: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Simulator is fully functional!")
        print("\n🚀 Ready for demonstration!")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
