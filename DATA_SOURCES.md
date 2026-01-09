# 📊 Data Sources and References

This document provides complete attribution for all data sources used in the Mountain Road Safety Simulator.

---

## 🗺️ Road Geometry Data

### **Bhikyasen Road Elevation and Slope Data**
- **Source**: Google Earth Pro
- **Method**: Manual waypoint plotting and elevation extraction
- **Location**: Bhikyasen Road, Uttarakhand, India
- **Coverage**: 10.11 km, 90 road segments
- **Data Points**: Distance, Elevation, Slope percentage
- **Collection Date**: December 2025 - January 2026
- **File**: `bhikyasen road data.csv`
- **Accuracy**: ±5 meters (Google Earth elevation accuracy)

**Citation**:
```
Google Earth Pro. (2025). Elevation data for Bhikyasen Road, Uttarakhand, India. 
Retrieved from https://earth.google.com/
```

---

## 🚗 Vehicle Specifications

### **Vehicle Technical Parameters**
- **Source**: Manufacturer technical specifications
- **Vehicles Included**:
  - **Tata Starbus** (Bus - 12,000 kg)
  - **Maruti Swift** (Car - 1,200 kg)  
  - **Tata LPT 1613** (Truck - 16,000 kg)
- **Data Points**: Weight, dimensions, brake capacity, center of gravity
- **File**: `data/vehicle_params.csv`

**References**:
- Tata Motors. (2024). Starbus Technical Specifications. https://www.tatamotors.com/
- Maruti Suzuki. (2024). Swift Specifications. https://www.marutisuzuki.com/
- Tata Motors. (2024). LPT 1613 Truck Specifications. https://www.tatamotors.com/

---

## 🚨 Accident Statistics

### **Uttarakhand Road Accident Data (2005-2024)**
- **Source**: Government of Uttarakhand / Ministry of Road Transport & Highways
- **Coverage**: 20 years (2005-2024)
- **Data Points**: 
  - Total accidents per year
  - Fatal accident percentage
  - Persons killed
  - Persons injured
  - Accident severity index
- **File**: `data/uttarakhand_accident_statistics.csv`
- **Total Records**: 28,000+ accidents, 17,500+ deaths

**Citation**:
```
Government of Uttarakhand. (2024). Road Accident Statistics 2005-2024. 
Transport Department, Uttarakhand.

Ministry of Road Transport & Highways. (2024). Road Accidents in India - Annual Report.
Retrieved from https://morth.nic.in/
```

**Key Statistics**:
- 2024: 1,747 accidents, 1,090 deaths (highest on record)
- Average fatality rate: 50-57% (extremely high compared to national average ~30%)
- Economic impact: ₹873+ crores in damages (2024 alone)

---

## 🌦️ Weather and Climate Data

### **Uttarakhand Weather Patterns (2022-2026)**
- **Source**: Shimla Airport (VISM) Meteorological Data
- **Provider**: India Meteorological Department (IMD)
- **Coverage**: 5 years (2022-2026)
- **Data Points**:
  - Maximum and minimum temperatures
  - Relative humidity
  - Wind speed
  - Days above temperature thresholds
- **Files**: 
  - `data/uttarakhand_weather_historical.csv`
  - `data/uttarakhand_weather_detailed.csv`
  - `data/uttarakhand_weather_data.xlsx`

**Citation**:
```
India Meteorological Department (IMD). (2022-2026). 
Weather Data for Shimla Airport (VISM), Himachal Pradesh/Uttarakhand Region.
Retrieved from https://www.imd.gov.in/
```

**Key Insights**:
- Monsoon months (July-August): 87% average humidity
- Coldest month: January (14.5°C max, 7.6°C min)
- Hottest month: June (27.1°C max)
- Peak wind speeds: February-May (~3.7 km/h)

---

## 🌍 Environmental and Geological Data

### **Soil and Terrain Classification**
- **Source**: Geological Survey of India (GSI)
- **Reference**: Landslide Hazard Zonation reports for Uttarakhand
- **Data Used**: Soil types (Rocky, Clay, Sandy, Mixed)
- **File**: `data/environment_conditions.csv`

**Citation**:
```
Geological Survey of India (GSI). (2020). Landslide Hazard Zonation - Uttarakhand.
GSI Report Series.
```

### **Rainfall Patterns**
- **Source**: IMD Historical Rainfall Data
- **Region**: Uttarakhand Himalayan region
- **Data Used**: Monthly rainfall averages, monsoon intensity

**Citation**:
```
India Meteorological Department. (2020-2024). 
Rainfall Statistics for Uttarakhand State.
```

---

## 🛣️ Road Infrastructure Data

### **Road Characteristics (Synthetic/Enhanced)**
- **Base Source**: Google Earth + field observations
- **Enhancement Method**: Realistic assumptions based on typical mountain road standards
- **Data Points**: Road width, curve sharpness, cliff presence, guardrail locations
- **File**: `data/road_characteristics.csv`
- **Note**: These are estimated/derived values based on visual analysis and standard road parameters

**Methodology**:
- Road widths: Estimated from Google Earth satellite imagery
- Curve classifications: Calculated from elevation changes and road geometry
- Cliff/Guardrail data: Visual identification from satellite imagery
- Visibility: Estimated based on typical mountain road conditions

---

## 📚 Scientific and Technical References

### **Physics Models**

**Brake Heat Model**:
```
Energy Dissipated (E) = m × g × h
where:
  m = vehicle mass (kg)
  g = gravitational acceleration (9.81 m/s²)
  h = vertical descent (meters)
```
- **Reference**: Limpert, R. (2011). Brake Design and Safety (3rd ed.). SAE International.

**Vehicle Stability**:
- **Reference**: Gillespie, T. D. (1992). Fundamentals of Vehicle Dynamics. SAE International.

**Landslide Probability**:
- **Reference**: GSI Landslide Risk Assessment Methodology
- Based on slope angle, soil type, and rainfall intensity

---

## ⚖️ Disclaimer

### Data Accuracy:
- **Road geometry**: High accuracy (±5m from Google Earth)
- **Accident statistics**: Official government data
- **Weather data**: Meteorological measurements (±1°C accuracy)
- **Vehicle specs**: Manufacturer specifications
- **Road infrastructure**: Estimated from visual analysis (moderate accuracy)

### Limitations:
1. Road characteristic data (width, curves, cliffs) are estimates and should be validated with on-site surveys
2. Landslide risk model is theoretical and requires calibration with historical landslide data
3. Brake heating model uses simplified thermodynamic assumptions
4. Weather data from Shimla Airport may not perfectly represent micro-climates along specific road segments

---

## 📧 Data Usage and Attribution

If you use this simulator or its data for research, publications, or projects, please cite:

```
Bisht, A. (2026). Mountain Road Safety Simulator: Predictive Risk Analysis for Bhikyasen Road, 
Uttarakhand. B.Tech Project, Shivalik College of Engineering.

Data sources: Google Earth Pro, Government of Uttarakhand Transport Department, 
India Meteorological Department, Geological Survey of India.
```

---

## 🔄 Data Updates

- **Last Updated**: January 9, 2026
- **Next Planned Update**: June 2026 (add 2025 accident data when available)
- **Contributor**: Akanksha Bisht (akankshabisht01)

---

## 📝 License

The simulator code is released under MIT License. However, the data sources retain their original licenses:
- Government data: Public domain
- Google Earth data: For non-commercial educational use
- IMD weather data: As per IMD data policy
- Vehicle manufacturer data: Fair use for educational purposes

---

**For questions about data sources, please contact:**
- Email: [your-email]
- GitHub: https://github.com/akankshabisht01
- Project: Mountain Road Safety Simulator

---

**Acknowledgments:**
Special thanks to Google Earth, India Meteorological Department, Geological Survey of India, 
Government of Uttarakhand, and vehicle manufacturers for making data accessible for educational research.
