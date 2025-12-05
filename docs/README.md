# 🌍 Advanced Carbon Footprint Analyzer

An intelligent carbon footprint tracking and analysis application powered by **Ollama Llama3:8b** with real-time climate data integration.

## ✨ Features

### 🎯 Core Functionality
- **Real-Time Climate Data Extraction**: Pulls live atmospheric CO₂ levels from NOAA, UK grid carbon intensity, and climate news
- **Comprehensive Footprint Calculation**: Tracks transport, diet, heating, electricity, and consumption emissions
- **Historical Tracking**: SQLite database stores your footprint history with trend analysis
- **AI-Powered Insights**: Llama3:8b provides personalized, context-aware sustainability recommendations
- **Interactive Visualizations**: Plotly charts for trends, breakdowns, and comparisons

### 🚀 Advanced Features
- **Regional Carbon Intensity**: Uses real-time grid data or regional estimates for accurate electricity calculations
- **Comparative Analysis**: Compare against Paris Agreement targets, global averages, and your own history
- **Goal Setting & Action Plans**: AI-generated 3-month carbon reduction roadmaps
- **Personalized Recommendations**: Context-aware suggestions based on your specific usage patterns and location

## 📋 Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally
- Llama3:8b model downloaded in Ollama

## 🔧 Installation

### 1. Install Ollama and Download Llama3:8b

```bash
# Install Ollama (visit https://ollama.ai/ for your OS)

# Pull Llama3:8b model
ollama pull llama3:8b
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run carbon_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 How to Use

### Calculate Your Footprint
1. Navigate to the **"Calculate Footprint"** tab
2. Input your daily activities:
   - Transportation mode and distance
   - Diet type
   - Heating method and hours
   - Electricity usage
   - Optional: Consumption habits
3. View real-time results with visualizations
4. Save your calculation to track trends

### Track Your Progress
1. Go to **"Trends & History"** tab
2. View your 30-day statistics and trends
3. See category breakdowns and best/worst days
4. Analyze improvement over time

### Get AI Insights
1. Open **"AI Analysis"** tab
2. Choose analysis type:
   - **Comprehensive Analysis**: Deep dive with personalized recommendations
   - **Quick Tips**: Fast, actionable suggestions
   - **Compare with Previous**: Track changes from your last calculation
3. Click "Generate AI Analysis" to get insights from Llama3:8b

### Set Goals
1. Visit **"Goals & Action Plan"** tab
2. Set your reduction target (%)
3. Generate a 3-month personalized action plan
4. Track progress toward Paris Agreement targets

## 🌐 Data Sources

- **Atmospheric CO₂**: NOAA Mauna Loa Observatory
- **Grid Carbon Intensity**: Carbon Intensity API (UK)
- **Climate News**: NASA Climate RSS Feed
- **Emissions Factors**: IPCC, DEFRA, and scientific literature

## 🎨 Key Innovations

### 1. Real-Time Data Integration
Unlike static calculators, this app pulls live climate data:
- Current atmospheric CO₂ levels
- Real-time electricity grid carbon intensity
- Latest climate news headlines

### 2. Context-Aware AI Analysis
Llama3:8b receives rich context including:
- Your personal usage patterns
- Historical trends
- Real-time climate conditions
- Regional factors
- Global benchmarks

The AI provides specific, actionable recommendations based on YOUR data, not generic advice.

### 3. Historical Intelligence
SQLite database tracks:
- All your calculations
- AI insights
- Trends over time
- Progress toward goals

### 4. Professional Visualization
Interactive Plotly charts:
- Trend analysis with Paris Agreement target overlay
- Category breakdowns (pie charts, stacked areas)
- Comparative benchmarking
- Progress gauges

## 🏗️ Architecture

```
carbon_app.py              # Main Streamlit application
├── emissions_data.py      # Enhanced emissions factors + regional data
├── climate_data_service.py # Real-time climate data extraction
├── database.py            # SQLite historical tracking
├── llm_service.py         # Ollama/Llama3 integration
└── visualizations.py      # Plotly chart generators
```

## 🧪 Testing Individual Components

Each module can be tested independently:

```bash
# Test climate data service
python climate_data_service.py

# Test database
python database.py

# Test LLM service (requires Ollama running)
python llm_service.py
```

## 📈 Example Use Cases

1. **Daily Tracking**: Log your footprint each day to identify patterns
2. **Lifestyle Changes**: Test the impact of switching to electric vehicles, changing diet, etc.
3. **Goal Achievement**: Work toward Paris Agreement targets with AI guidance
4. **Education**: Learn about carbon emissions and climate science
5. **Workplace Sustainability**: Track team or organizational footprints

## 🔮 Future Enhancements

Potential additions:
- OAuth integration for personal data import (Google Maps timeline, energy bills)
- Multi-user support with team challenges
- Carbon offset marketplace integration
- Mobile app version
- Integration with smart home devices
- Flight and travel tracking
- Gamification with achievements

## 📝 Notes

- **Privacy**: All data is stored locally in SQLite. No external servers.
- **Accuracy**: Emissions factors are estimates based on scientific literature. Real-world values vary.
- **Internet**: Required for real-time climate data; app works offline with cached values.
- **Ollama**: Must be running for AI analysis features.

## 🤝 Contributing

This is a lab project demonstrating:
- ✅ Ollama integration
- ✅ Llama3:8b LLM usage
- ✅ Streamlit interface
- ✅ Climate focus
- ✅ Real-time data extraction

## 📄 License

Educational project for LLM integration lab.

## 🌱 Impact

By tracking and understanding your carbon footprint, you're taking the first step toward meaningful climate action. Every reduction counts! 🌍
