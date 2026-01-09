# 🏔️ Mountain Road Safety Simulator

**Predicting and Preventing Accidents on India's Most Dangerous Hill Roads**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Project Overview

A groundbreaking computer-based simulation platform that creates virtual models of mountain roads to **predict and prevent accidents before they occur**. This hackathon project focuses on **Bhikyasen Road, Uttarakhand** - analyzing 10.11 km of treacherous mountain terrain with 90 road segments.

### 🎯 Problem Statement

India's mountain regions face recurring tragedies:
- 🚌 Vehicles plunging into gorges
- 🛑 Brake systems failing on steep descents
- 🌧️ Landslides sweeping away roads without warning
- **100+ lives lost annually** on Uttarakhand mountain roads alone

### 💡 Our Solution

Multi-hazard prediction system that identifies:
- ✅ **Cliff-fall risk zones**
- ✅ **Brake failure segments** (temperature-based modeling)
- ✅ **Landslide-prone areas**
- ✅ **Vehicle stability issues** on curves
- ✅ **Actionable safety recommendations**

---

## 🚀 Features

### Core Simulation Engine
- **Vehicle Physics Modeling**: Realistic simulation of buses, cars, and trucks
- **Brake Temperature Model**: Predicts brake failure based on heat buildup
- **Stability Analysis**: Evaluates tipping and rollover risks on curves
- **Landslide Prediction**: Weather and soil-based risk assessment
- **Driver Behavior Adjustment**: Accounts for night driving, overspeeding, experience

### Interactive Dashboard
- 📊 **Real-time Risk Visualization**: Color-coded danger zones
- 🗺️ **2D Road Maps**: Interactive segment-by-segment analysis
- 🔥 **Brake Monitoring**: Temperature progression charts
- ⚠️ **Dangerous Zone Identification**: Top 10 critical segments
- 📋 **Safety Recommendations**: Infrastructure and operational improvements

### Scenario Comparison
- 🌦️ Normal vs Rainy vs Foggy conditions
- 🚗 Different vehicle types
- ⚡ Speed variation analysis
- 🌙 Day vs Night driving

---

## 📂 Project Structure

```
mountain-road-safety/
├── data/
│   ├── road_characteristics.csv      # Road geometry (width, curves, cliffs)
│   ├── vehicle_params.csv            # Vehicle specifications
│   └── environment_conditions.csv    # Weather & soil data
├── src/
│   ├── simulation_engine.py          # Core physics & risk algorithms
│   ├── risk_calculator.py            # Risk fusion & recommendations
│   └── visualizer.py                 # Charts & maps
├── bhikyasen road data.csv           # Real Google Earth elevation data
├── app.py                            # Streamlit dashboard
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone/Download Project
```bash
cd "d:/App/mountain road safety"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Verify Data Files
Ensure these files exist:
- `bhikyasen road data.csv` (your Google Earth data)
- `data/road_characteristics.csv`
- `data/vehicle_params.csv`
- `data/environment_conditions.csv`

---

## 🎮 How to Run

### Launch the Dashboard
```powershell
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Using the Simulator

#### **Single Simulation Mode**

1. **Select Vehicle Type**
   - Bus (12,000 kg) - Worst case scenario
   - Car (1,200 kg) - Lighter vehicle
   - Truck (16,000 kg) - Heavy cargo

2. **Choose Environment**
   - Normal: Clear, dry conditions
   - Light_Rain: Moderate rainfall
   - Heavy_Rain: Monsoon conditions (highest risk)
   - Winter: Cold with possible ice
   - Foggy: Poor visibility

3. **Set Driving Parameters**
   - Speed: 20-80 km/h
   - Night driving: ON/OFF
   - Overspeeding: ON/OFF
   - Visibility: Good/Poor
   - Driver experience: Novice/Medium/Expert

4. **Click "Run Simulation"**

5. **Explore Results in 5 Tabs:**
   - 📊 **Overview**: Key metrics & statistics
   - 🗺️ **Risk Map**: Visual danger zones
   - 🔥 **Brake Analysis**: Temperature monitoring
   - ⚠️ **Dangerous Zones**: Top 10 critical segments
   - 📋 **Recommendations**: Safety improvements

#### **Scenario Comparison Mode**

1. Switch to "Scenario Comparison" in sidebar
2. Click "Run Scenario Comparison"
3. View side-by-side comparison of:
   - Normal weather
   - Heavy rain
   - Overspeeding
   - Night + Rain (worst case)

---

## 📊 Understanding the Results

### Risk Score Scale
- 🟢 **0-25%**: Low risk (Safe)
- 🟡 **25-40%**: Medium risk (Caution)
- 🟠 **40-60%**: High risk (Safety measures needed)
- 🔴 **60-80%**: Extreme risk (High priority intervention)
- ⚫ **80-100%**: Critical (Immediate action required)

### Key Metrics Explained

| Metric | What It Means | Critical Threshold |
|--------|---------------|-------------------|
| **Brake Temperature** | Heat buildup in brake system | > 250°C (Warning), > 350°C (Failure) |
| **Stability Risk** | Vehicle tipping/rollover chance | > 60% (Dangerous curves) |
| **Cliff Fall Risk** | Probability of falling off edge | > 60% (Need guardrails) |
| **Landslide Risk** | Slope failure probability | > 60% (Road closure in rain) |

### Recommendation Types

1. **INFRASTRUCTURE** 🏗️
   - Guardrails, escape ramps, retaining walls
   - Cost: High (₹20 lakhs - ₹2 crores)
   - Time: 2-12 months

2. **SIGNAGE** 🚸
   - Warning boards, speed limits, curve markers
   - Cost: Low (₹30,000 - ₹1 lakh)
   - Time: 1-2 weeks

3. **TRAFFIC MANAGEMENT** 🚦
   - Speed limits, vehicle restrictions, road closures
   - Cost: Low-Medium (₹10-50 lakhs)
   - Time: Immediate - 1 month

4. **MONITORING** 📡
   - Sensors, cameras, weather stations
   - Cost: Medium (₹10-50 lakhs)
   - Time: 1-3 months

---

## 🧪 Sample Test Cases

### Test 1: Bus in Normal Conditions
```
Vehicle: Bus
Weather: Normal
Speed: 40 km/h
Expected: Moderate risk on extreme slopes (Segments 8, 30, 64)
```

### Test 2: Bus in Heavy Rain
```
Vehicle: Bus
Weather: Heavy_Rain
Speed: 35 km/h
Expected: High risk, multiple landslide warnings
```

### Test 3: Overspeeding Car
```
Vehicle: Car
Weather: Normal
Speed: 70 km/h
Expected: High stability risk on sharp curves
```

### Test 4: Night Driving in Fog
```
Vehicle: Bus
Weather: Foggy
Night: Yes
Speed: 30 km/h
Expected: High cliff-fall risk due to poor visibility
```

---

## 🎓 Technical Implementation

### Algorithms Used

#### 1. **Vehicle Stability Risk**
```python
stability_risk = (
    lateral_risk * 0.3 +           # Curve sharpness + speed
    longitudinal_risk * 0.25 +     # Slope + weight
    clearance_risk * 0.2 +         # Road width vs vehicle size
    tipping_risk * 0.15 +          # Center of gravity
    friction_risk * 0.1            # Road surface condition
)
```

#### 2. **Brake Temperature Model**
```python
# Energy dissipated on downhill
E = m * g * h = mass * 9.81 * height_loss

# Temperature increase
ΔT = (E * heat_factor) / (brake_mass * specific_heat)

# Failure risk
risk = (temperature - 200) / 200  if temp > 200°C
```

#### 3. **Landslide Probability**
```python
landslide_risk = base_risk * (
    slope_factor * 0.35 +          # Steepness
    soil_factor * 0.30 +           # Loose vs rocky
    rainfall_factor * 0.25 +       # Intensity
    vegetation_factor * 0.10       # Ground cover
)
```

#### 4. **Risk Fusion**
```python
overall_risk = (
    stability_risk * 0.25 +
    brake_failure_risk * 0.30 +
    cliff_fall_risk * 0.25 +
    landslide_risk * 0.20
) * driver_behavior_multiplier
```

---

## 📈 Data Sources

**See [DATA_SOURCES.md](DATA_SOURCES.md) for complete data attribution and references.**

### Road Geometry
- **Source**: Google Earth Pro (2025-2026)
- **Method**: Manual elevation waypoint plotting
- **Data**: 90 segments, 10.11 km of Bhikyasen Road
- **Attributes**: Distance, elevation, slope percentage, GPS coordinates

### Accident Statistics (NEW!)
- **Source**: Government of Uttarakhand / Ministry of Road Transport & Highways
- **Coverage**: 20 years (2005-2024)
- **Data**: 28,000+ accidents, 17,500+ deaths, injury statistics
- **File**: `data/uttarakhand_accident_statistics.csv`

### Weather Data (NEW!)
- **Source**: India Meteorological Department (IMD) - Shimla Airport (VISM)
- **Coverage**: 5 years (2022-2026)
- **Data**: Temperature, humidity, wind speed, monsoon patterns
- **Files**: `data/uttarakhand_weather_historical.csv`, `uttarakhand_weather_detailed.csv`

### Vehicle Specifications
- **Source**: Manufacturer technical sheets (Tata Motors, Maruti Suzuki)
- **Vehicles**: Tata Starbus, Maruti Swift, Tata LPT 1613
- **Parameters**: Weight, dimensions, brake capacity, center of gravity

### Environmental Data
- **Rainfall**: IMD historical data
- **Soil**: Geological Survey of India (GSI) classifications
- **Landslide**: GSI Hazard Zonation reports

**All data sources are properly cited and attributed. See DATA_SOURCES.md for detailed references.**

---


## 💰 Cost-Benefit Analysis

### Implementation Cost
- **Software Development**: ₹10-15 lakhs (one-time)
- **Data Collection**: ₹5-8 lakhs per 100 km
- **Annual Maintenance**: ₹3-5 lakhs

### Potential Savings
- **Per Accident Prevented**: ₹50 lakhs - ₹2 crores
  - Medical costs
  - Vehicle damage
  - Legal costs
  - Lost productivity
- **Lives Saved**: Priceless

### ROI: 10:1 or higher

---

## 🔮 Future Enhancements

### Phase 2 (Next 3 months)
- [ ] Real-time weather integration (API)
- [ ] GPS-based vehicle tracking
- [ ] Mobile app for drivers
- [ ] Multi-language support (Hindi, local languages)

### Phase 3 (6-12 months)
- [ ] AI/ML for predictive maintenance
- [ ] Historical accident data integration
- [ ] IoT sensor network integration
- [ ] Government dashboard for authorities

### Phase 4 (Long-term)
- [ ] Expand to 100+ mountain roads
- [ ] Integration with Google Maps
- [ ] Real-time traffic advisories
- [ ] Autonomous vehicle integration

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

### How to Contribute
1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 👨‍💻 Developer

**Akanksha Bisht**  
B.Tech CSE, 4th Year  
Shivalik College of Engineering  
Uttarakhand

---

## 📝 License

MIT License - Feel free to use for educational and non-commercial purposes.

---

## 🙏 Acknowledgments

- **Data Source**: Google Earth, India Meteorological Department
- **Inspiration**: Real accident statistics from Uttarakhand
- **Framework**: Streamlit for rapid prototyping
- **Visualization**: Plotly for interactive charts

---

## 📞 Support & Contact

For questions, issues, or collaboration:
- 📧 Email: [akankshabisht145@gmail.com]
- 💼 LinkedIn: [www.linkedin.com/in/akanksha-bisht-00a1951b7]
- 🐙 GitHub: [https://github.com/akankshabisht01]

---



## 📚 References

1. Ministry of Road Transport & Highways - "Road Accidents in India" (Annual Report)
2. Geological Survey of India - Landslide Hazard Zonation
3. India Meteorological Department - Rainfall Data
4. Research papers on brake system thermodynamics
5. Vehicle dynamics and stability analysis literature

---

**"An ounce of prevention is worth a pound of cure."**  
*- Benjamin Franklin*

Let's make mountain roads safer, one simulation at a time. 🏔️🚗✨

