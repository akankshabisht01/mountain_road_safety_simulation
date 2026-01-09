# Mountain Road Safety Simulator - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Open Terminal
Press `Ctrl + ~` in VS Code or open PowerShell

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Simulator
```powershell
streamlit run app.py
```

### Step 4: Open Browser
- Automatically opens at: http://localhost:8501
- If not, manually navigate to the URL

## 🎮 Quick Demo

### Recommended First Test:
1. **Vehicle**: Bus
2. **Weather**: Heavy_Rain
3. **Speed**: 40 km/h
4. **Enable**: Poor Visibility
5. Click **"🚀 Run Simulation"**

### What to Look For:
- ❌ High risk on segments 8, 30, 37, 64
- 🔥 Brake temperature spike > 250°C
- ⚠️ Multiple landslide warnings
- 📊 Critical segments count

## 📋 Keyboard Shortcuts

- `Ctrl + R` - Rerun simulation
- `Ctrl + L` - Clear cache
- `Ctrl + C` (in terminal) - Stop server

## 🆘 Troubleshooting

### Port Already in Use
```powershell
streamlit run app.py --server.port 8502
```

### Module Not Found
```powershell
pip install --upgrade -r requirements.txt
```

### Data File Error
Ensure `bhikyasen road data.csv` is in the root directory

## 💡 Tips for Judges

1. **Compare scenarios** - Use Scenario Comparison mode
2. **Check brake analysis** - Tab 3 shows temperature model
3. **View recommendations** - Tab 5 shows actionable items
4. **Explore risk map** - Tab 2 has interactive visualization

## 📱 For Presentation

### 5-Minute Demo Flow:
1. Show road statistics (10.11 km, 90 segments)
2. Run normal condition (moderate risk)
3. Run heavy rain (risk increase demo)
4. Show brake temperature spike
5. Display top recommendations

### Key Talking Points:
- "Physics-based brake failure model"
- "Real Google Earth elevation data"
- "100+ lives saved potential annually"
- "₹50 lakhs - ₹2 crores per accident prevented"
- "Deployable immediately, no hardware"

---

**Need Help?** Check README.md for full documentation.

**Ready to Demo?** Run the command and open the browser!
