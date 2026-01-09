"""Quick test of statistics dashboard visualization"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.visualizer import RoadVisualizer

# Create sample risk stats
risk_stats = {
    'total_segments': 90,
    'critical_segments': 2,
    'extreme_segments': 5,
    'high_risk_segments': 12,
    'average_risk': 0.145,
    'max_risk': 0.39,
    'max_risk_segment': 64,
    'max_brake_temp': 20.0,
    'brake_critical_segments': 0,
    'cliff_zones': 18,
    'landslide_zones': 8
}

print("Creating statistics dashboard...")
visualizer = RoadVisualizer()
fig = visualizer.create_statistics_dashboard(risk_stats)

print(f"✅ Dashboard created with {len(fig.data)} traces")
print(f"   Traces: {[trace.type for trace in fig.data]}")
print("\n📊 Statistics:")
for key, value in risk_stats.items():
    print(f"   {key}: {value}")

# Try to save as HTML to verify it works
output_file = Path(__file__).parent / "test_dashboard.html"
fig.write_html(str(output_file))
print(f"\n✅ Dashboard saved to: {output_file}")
print("   Open this file in a browser to view the complete dashboard!")
