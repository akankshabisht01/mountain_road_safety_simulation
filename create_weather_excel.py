"""
Create Excel version of Uttarakhand weather data
"""
import pandas as pd
from pathlib import Path

base_path = Path(__file__).parent

# Load the CSV data
weather_monthly = pd.read_csv(base_path / 'data' / 'uttarakhand_weather_historical.csv')
weather_detailed = pd.read_csv(base_path / 'data' / 'uttarakhand_weather_detailed.csv')

# Create Excel file with multiple sheets
excel_file = base_path / 'data' / 'uttarakhand_weather_data.xlsx'

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    # Sheet 1: Monthly Averages
    weather_monthly.to_excel(writer, sheet_name='Monthly Averages', index=False)
    
    # Sheet 2: Detailed Year-Month Data
    weather_detailed.to_excel(writer, sheet_name='Detailed Data', index=False)
    
    # Sheet 3: Summary Statistics
    summary_data = {
        'Metric': [
            'Average Annual Temperature (Max)',
            'Average Annual Temperature (Min)',
            'Average Annual Humidity',
            'Average Wind Speed',
            'Monsoon Months',
            'Monsoon Humidity',
            'Coldest Month',
            'Hottest Month',
            'Data Source',
            'Years Covered'
        ],
        'Value': [
            f"{weather_monthly['Max_Temp_Avg_C'].mean():.1f}°C",
            f"{weather_monthly['Min_Temp_Avg_C'].mean():.1f}°C",
            f"{weather_monthly['Humidity_Avg_Percent'].mean():.1f}%",
            f"{weather_monthly['Wind_Speed_Avg_kmh'].mean():.1f} km/h",
            'July-August',
            '87%',
            'January (14.5°C max)',
            'June (27.1°C max)',
            'Shimla Airport (VISM)',
            '2022-2026'
        ]
    }
    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
    # Sheet 4: Seasonal Analysis
    seasonal = weather_monthly.groupby('Season').agg({
        'Max_Temp_Avg_C': 'mean',
        'Min_Temp_Avg_C': 'mean',
        'Humidity_Avg_Percent': 'mean',
        'Wind_Speed_Avg_kmh': 'mean'
    }).round(1).reset_index()
    seasonal.columns = ['Season', 'Avg Max Temp (°C)', 'Avg Min Temp (°C)', 'Avg Humidity (%)', 'Avg Wind Speed (km/h)']
    seasonal.to_excel(writer, sheet_name='Seasonal Analysis', index=False)

print(f"✅ Excel file created: {excel_file}")
print("\nSheets included:")
print("  1. Monthly Averages - Climate patterns by month")
print("  2. Detailed Data - Year-by-year monthly data (2022-2026)")
print("  3. Summary - Key statistics and metadata")
print("  4. Seasonal Analysis - Winter/Spring/Monsoon/Autumn comparison")
print(f"\n📊 You can now open this file in Excel!")
