# 🚀 Quick Start Guide

## Get Running in 3 Steps

### Step 1: Verify Ollama Setup
```bash
# Check if Ollama is running
ollama list

# You should see llama3:8b in the list
# If not, run:
ollama pull llama3:8b
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch the App
```bash
streamlit run carbon_app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎯 First-Time User Flow

### 1. Calculate Your First Footprint (2 minutes)
- Go to **"Calculate Footprint"** tab
- Fill in your typical daily activities
- See instant results with visualizations
- Click **"Save This Calculation"** to start tracking

### 2. Get AI Insights (1 minute)
- Switch to **"AI Analysis"** tab
- Click **"Generate AI Analysis"**
- Wait ~30 seconds for Llama3:8b to analyze your data
- Read personalized recommendations

### 3. Track Progress (ongoing)
- Return daily/weekly to log new calculations
- View trends in **"Trends & History"** tab
- Set goals in **"Goals & Action Plan"** tab

## 💡 Pro Tips

### Make It Personal
- Enter your city/location in the sidebar for localized recommendations
- Select your actual region for accurate electricity calculations
- Save calculations regularly to build meaningful trend data

### Get the Best AI Insights
- The more data you track, the better the AI analysis
- Try "Compare with Previous" after saving multiple calculations
- Use the action plan generator after 1+ week of tracking

### Real-Time Data
- Check the sidebar for live climate data
- Grid intensity updates every 30 minutes (UK only)
- Atmospheric CO₂ updates weekly from NOAA

## 🔍 What Makes This Impressive

### 1. Real Data Extraction
Unlike basic calculators, this app:
- Fetches live CO₂ levels from NOAA Mauna Loa Observatory
- Gets real-time UK grid carbon intensity
- Pulls latest climate news from NASA

### 2. AI-Powered Analysis
Llama3:8b receives rich context:
- Your actual usage patterns
- Historical trends
- Real-time climate conditions
- Global benchmarks

Result: **Personalized, actionable recommendations** instead of generic tips.

### 3. Full Historical Tracking
- SQLite database stores everything locally
- Trend analysis with interactive charts
- Progress monitoring over time
- AI insights saved with each calculation

### 4. Scientific Accuracy
- Emissions factors from IPCC, DEFRA
- Regional grid intensity data
- Paris Agreement target integration
- Global benchmark comparisons

## 🎨 Key Features Demo

### Calculate Tab
- Multiple transport modes (car, bus, train, bike, EV, etc.)
- 6 diet types from vegan to high-meat omnivore
- Regional electricity calculations
- Consumption tracking (clothes, streaming)
- Instant visual feedback
- Compare against global benchmarks

### Trends Tab
- 30-day statistics dashboard
- Interactive time-series charts
- Category breakdown analysis
- Best/worst day tracking
- Recent records history

### AI Analysis Tab
- **Comprehensive Analysis**: Deep dive with context
- **Quick Tips**: Fast, specific suggestions
- **Compare Mode**: Track improvements
- All insights saved to database

### Goals Tab
- Set custom reduction targets
- 3-month AI-generated action plans
- Progress visualization
- Paris Agreement tracking

## 🐛 Troubleshooting

### "Connection Error" for Climate Data
- Internet connection required for real-time data
- App falls back to estimated values if APIs unavailable
- Check firewall settings if issues persist

### AI Analysis Not Working
```bash
# Verify Ollama is running
ollama list

# Test the model
echo "Hello" | ollama run llama3:8b
```

### Slow AI Responses
- First request after starting Ollama can be slow (model loading)
- Subsequent requests are faster
- Analysis takes 20-60 seconds depending on system

### No Historical Data Showing
- You must save at least one calculation first
- Click "Save This Calculation" in the Calculate tab
- Data persists in `carbon_footprint.db`

## 📊 Sample Workflow

**Day 1**: Calculate baseline, save it, get AI analysis
**Days 2-7**: Log daily variations, track patterns
**Week 2**: Review trends, compare improvements
**Week 3**: Set reduction goal, generate action plan
**Week 4**: Measure progress toward target

## 🌟 Demo the Impressive Features

To showcase this app:

1. **Show Real-Time Data**: Point to sidebar showing live CO₂ and grid intensity
2. **Calculate Footprint**: Enter realistic data, show instant visualizations
3. **Generate AI Analysis**: Demonstrate context-aware Llama3:8b recommendations
4. **Show Trends**: If you have data, display the trend charts
5. **Create Action Plan**: Generate the 3-month roadmap

The combination of **real data extraction + historical tracking + AI analysis** makes this far beyond a basic calculator!

## 🎓 Educational Value

This project demonstrates:
- ✅ LLM integration (Ollama + Llama3:8b)
- ✅ Real-time data extraction (APIs, web scraping)
- ✅ Database design (SQLite)
- ✅ Data visualization (Plotly)
- ✅ Full-stack development (Streamlit)
- ✅ Climate science application
- ✅ Prompt engineering
- ✅ Context-aware AI

## 🚀 You're Ready!

Start the app and begin tracking your carbon footprint with AI-powered insights:

```bash
streamlit run carbon_app.py
```

Happy climate action! 🌍
