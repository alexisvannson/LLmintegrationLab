"""
Advanced Carbon Footprint Analyzer with Real-Time Climate Data
Powered by Ollama Llama3:8b
"""

import streamlit as st
import json
from datetime import datetime
from src.data.emissions import EMISSIONS, TARGETS, GRID_INTENSITY
from src.services.climate_data import ClimateDataService
from src.services.database import CarbonFootprintDB
from src.services.llm import OllamaService
from src.visualizations import (
    create_emissions_breakdown_pie,
    create_trend_chart,
    create_comparison_bar,
    create_progress_gauge,
    create_category_comparison,
    create_atmospheric_co2_indicator,
    create_summary_metrics_chart
)

# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #2ECC71, #3498DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #7F8C8D;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498DB;
    }
    .stAlert {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def init_services():
    return {
        'climate': ClimateDataService(),
        'db': CarbonFootprintDB('data/carbon_footprint.db'),
        'llm': OllamaService()
    }

services = init_services()

# Header
st.markdown('<h1 class="main-header">Carbon Footprint Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Track, Analyze & Reduce Your Environmental Impact with AI-Powered Insights</p>', unsafe_allow_html=True)

# Fetch real-time climate data
with st.spinner("Loading real-time climate data..."):
    climate_context = services['climate'].get_climate_context()

# Sidebar - Climate Context
with st.sidebar:
    st.header("Live Climate Data")

    co2_ppm = climate_context.get('atmospheric_co2_ppm', 425)
    st.metric(
        label="Atmospheric CO₂",
        value=f"{co2_ppm:.1f} ppm",
        delta=f"+{co2_ppm - 280:.1f} from pre-industrial",
        delta_color="inverse"
    )

    if climate_context.get('grid_intensity'):
        intensity = climate_context['grid_intensity']
        st.metric(
            label="Grid Carbon Intensity (UK)",
            value=f"{intensity.get('actual', 'N/A')} gCO₂/kWh",
            help=f"Status: {intensity.get('index', 'N/A').upper()}"
        )

    st.info(climate_context.get('climate_headline', 'Climate action remains critical'))

    st.divider()

    # User location/region
    st.subheader("Settings")
    user_region = st.selectbox(
        "Your Region",
        options=list(GRID_INTENSITY.keys()),
        index=0,
        help="Used for accurate electricity carbon calculations"
    )

    user_location = st.text_input(
        "City/Location (optional)",
        placeholder="e.g., London, UK",
        help="For personalized recommendations"
    )

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Calculate Footprint",
    "Trends & History",
    "AI Analysis",
    "Goals & Action Plan"
])

# TAB 1: Calculate Footprint
with tab1:
    st.header("Calculate Your Daily Carbon Footprint")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transportation")
        transport_mode = st.selectbox(
            "Primary transport mode:",
            options=list(EMISSIONS["transport"].keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )
        distance = st.slider("Daily commute distance (km):", 0, 150, 20)

        st.subheader("Diet")
        diet_type = st.selectbox(
            "Dietary pattern:",
            options=list(EMISSIONS["diet"].keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )

        st.subheader("Consumption (optional)")
        buy_clothes = st.checkbox("Bought new clothes this month?")
        streaming_hours = st.slider("Daily streaming/screen time (hours):", 0, 12, 3)

    with col2:
        st.subheader("Heating")
        heating_type = st.selectbox(
            "Heating method:",
            options=list(EMISSIONS["heating"].keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )
        heating_hours = st.slider("Daily heating hours:", 0, 24, 6)

        st.subheader("Electricity")
        electricity_kwh = st.slider("Daily electricity use (kWh):", 0, 50, 12)

    # Calculate emissions
    transport_emissions = EMISSIONS["transport"][transport_mode] * distance
    diet_emissions = EMISSIONS["diet"][diet_type]
    heating_emissions = EMISSIONS["heating"][heating_type] * heating_hours

    # Get region-specific grid intensity
    grid_intensity = services['climate'].get_electricity_carbon_intensity_estimate(user_region)
    electricity_emissions = grid_intensity * electricity_kwh

    consumption_emissions = 0
    if buy_clothes:
        consumption_emissions += EMISSIONS["consumption"]["new_clothes_monthly"] / 30
    consumption_emissions += EMISSIONS["consumption"]["streaming_hours_daily"] * streaming_hours

    total_emissions = (
        transport_emissions +
        diet_emissions +
        heating_emissions +
        electricity_emissions +
        consumption_emissions
    )

    breakdown = {
        'Transport': transport_emissions,
        'Diet': diet_emissions,
        'Heating': heating_emissions,
        'Electricity': electricity_emissions,
        'Consumption': consumption_emissions
    }

    # Display results
    st.divider()
    st.subheader("Your Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Daily Footprint",
            f"{total_emissions:.2f} kg CO₂",
            help="Total daily carbon emissions"
        )

    with col2:
        annual = total_emissions * 365
        st.metric(
            "Annual Estimate",
            f"{annual/1000:.1f} tonnes CO₂",
            help="If you maintain this daily rate"
        )

    with col3:
        target = TARGETS['paris_agreement_daily']
        diff = total_emissions - target
        st.metric(
            "vs Paris Target",
            f"{diff:+.1f} kg CO₂",
            delta=f"{(diff/target*100):+.0f}%",
            delta_color="inverse"
        )

    with col4:
        world_avg = TARGETS['world_average_daily']
        diff_world = total_emissions - world_avg
        st.metric(
            "vs World Average",
            f"{diff_world:+.1f} kg CO₂",
            delta=f"{(diff_world/world_avg*100):+.0f}%",
            delta_color="inverse"
        )

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = create_emissions_breakdown_pie(breakdown)
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_gauge = create_progress_gauge(total_emissions, TARGETS['paris_agreement_daily'])
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Comparison chart
    fig_comparison = create_comparison_bar(total_emissions, TARGETS)
    st.plotly_chart(fig_comparison, use_container_width=True)

    # Save to database
    if st.button("Save This Calculation", type="primary", use_container_width=True):
        footprint_data = {
            'timestamp': datetime.now().isoformat(),
            'total_emissions': total_emissions,
            'transport_emissions': transport_emissions,
            'diet_emissions': diet_emissions,
            'heating_emissions': heating_emissions,
            'electricity_emissions': electricity_emissions,
            'consumption_emissions': consumption_emissions,
            'transport_mode': transport_mode,
            'distance_km': distance,
            'diet_type': diet_type,
            'heating_type': heating_type,
            'heating_hours': heating_hours,
            'electricity_kwh': electricity_kwh,
            'grid_carbon_intensity': grid_intensity,
            'atmospheric_co2_ppm': co2_ppm,
            'notes': f"Region: {user_region}, Location: {user_location or 'Not specified'}"
        }

        record_id = services['db'].save_footprint(footprint_data)
        st.success(f"Saved! Record ID: {record_id}. View trends in the 'Trends & History' tab.")

# TAB 2: Trends & History
with tab2:
    st.header("Your Carbon Footprint Trends")

    stats = services['db'].get_statistics(30)

    if stats.get('record_count', 0) > 0:
        # Summary metrics
        fig_metrics = create_summary_metrics_chart(stats)
        if fig_metrics:
            st.plotly_chart(fig_metrics, use_container_width=True)

        # Trend chart
        trend_data = services['db'].get_trend_data(30)
        if trend_data:
            fig_trend = create_trend_chart(trend_data, TARGETS['paris_agreement_daily'])
            st.plotly_chart(fig_trend, use_container_width=True)

        # Category breakdown
        category_avg = services['db'].get_category_breakdown(30)
        if category_avg and breakdown:
            fig_cat = create_category_comparison(breakdown, category_avg)
            st.plotly_chart(fig_cat, use_container_width=True)

        # Statistics table
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Records Tracked", stats['record_count'])
            st.metric("Total Emissions (30d)", f"{stats['total_emissions']:.1f} kg CO₂")

        with col2:
            st.metric("30-Day Average", f"{stats['avg_daily_emissions']:.2f} kg CO₂/day")
            improvement = stats['avg_daily_emissions'] - TARGETS['paris_agreement_daily']
            st.metric("Gap to Target", f"{improvement:+.2f} kg CO₂/day")

        with col3:
            st.metric("Best Day", f"{stats['min_emissions']:.2f} kg CO₂")
            st.metric("Worst Day", f"{stats['max_emissions']:.2f} kg CO₂")

        # Recent records
        with st.expander("View Recent Records"):
            recent = services['db'].get_recent_records(10)
            for record in recent:
                st.write(f"**{record['timestamp'][:10]}**: {record['total_emissions']:.2f} kg CO₂ - {record['notes'] or 'No notes'}")

    else:
        st.info("No historical data yet. Calculate and save your footprint in the 'Calculate Footprint' tab to start tracking trends!")

# TAB 3: AI Analysis
with tab3:
    st.header("AI-Powered Sustainability Insights")
    st.write("Get personalized recommendations from Llama3:8b based on your footprint and real-time climate data")

    if total_emissions > 0:
        analysis_type = st.radio(
            "Choose analysis type:",
            ["Comprehensive Analysis", "Quick Tips", "Compare with Previous"],
            horizontal=True
        )

        # Custom guidance text area
        st.subheader("Custom Guidance (Optional)")
        user_guidance = st.text_area(
            "Add any specific context or focus areas for the AI to consider:",
            placeholder="e.g., 'I want to focus on reducing transportation emissions' or 'I'm considering switching to renewable energy' or 'I have dietary restrictions'",
            help="This text will guide the AI to provide more personalized and relevant advice based on your specific situation or goals.",
            height=100
        )

        if st.button("Generate AI Analysis", type="primary", use_container_width=True):
            user_data = {
                'total_emissions': total_emissions,
                'breakdown': breakdown,
                'transport_mode': transport_mode,
                'distance_km': distance,
                'diet_type': diet_type,
                'heating_type': heating_type,
                'heating_hours': heating_hours,
                'electricity_kwh': electricity_kwh
            }

            with st.spinner("Llama3:8b is analyzing your carbon footprint..."):
                if analysis_type == "Comprehensive Analysis":
                    stats = services['db'].get_statistics(30) if services['db'].get_statistics(30).get('record_count', 0) > 0 else None
                    analysis = services['llm'].analyze_footprint(
                        user_data,
                        climate_context,
                        stats,
                        user_location or None,
                        user_guidance or None
                    )
                elif analysis_type == "Compare with Previous":
                    recent = services['db'].get_recent_records(2)
                    if len(recent) >= 2:
                        prev_total = recent[1]['total_emissions']
                        analysis = services['llm'].compare_footprints(
                            total_emissions,
                            prev_total,
                            breakdown
                        )
                    else:
                        analysis = "Not enough historical data for comparison. Save more records first!"
                else:
                    # Quick tips
                    quick_prompt = f"Give 3 quick, actionable tips to reduce a {total_emissions:.1f} kg CO₂/day footprint. The biggest contributor is {max(breakdown, key=breakdown.get)}. Be specific and brief."
                    if user_guidance:
                        quick_prompt += f"\n\nUser's specific context/goals: {user_guidance}"
                    analysis = services['llm'].generate_response(quick_prompt)

            st.markdown("### AI Analysis Results")
            st.markdown(analysis)

            # Save insight to database
            if analysis and not analysis.startswith("Error"):
                recent_records = services['db'].get_recent_records(1)
                if recent_records:
                    services['db'].save_llm_insight(recent_records[0]['id'], analysis)

    else:
        st.warning("Calculate your footprint first in the 'Calculate Footprint' tab!")

# TAB 4: Goals & Action Plan
with tab4:
    st.header("Set Goals & Create Your Action Plan")

    stats = services['db'].get_statistics(30)

    if stats.get('record_count', 0) > 0:
        current_avg = stats['avg_daily_emissions']

        st.metric(
            "Your 30-Day Average",
            f"{current_avg:.2f} kg CO₂/day",
            help="Based on your tracked records"
        )

        col1, col2 = st.columns(2)

        with col1:
            reduction_target = st.slider(
                "Set your reduction target (%):",
                min_value=10,
                max_value=100,
                value=50,
                step=5
            )

        with col2:
            target_emissions = current_avg * (1 - reduction_target / 100)
            st.metric(
                "Target Daily Footprint",
                f"{target_emissions:.2f} kg CO₂/day",
                delta=f"-{reduction_target}%",
                delta_color="normal"
            )

        if target_emissions < TARGETS['paris_agreement_daily']:
            st.success(f"This target would put you below the Paris Agreement goal of {TARGETS['paris_agreement_daily']} kg CO₂/day!")
        elif target_emissions < current_avg:
            st.info(f"Good goal! You'd still be {target_emissions - TARGETS['paris_agreement_daily']:.1f} kg above the Paris target, but making progress.")

        if st.button("Generate 3-Month Action Plan", type="primary", use_container_width=True):
            with st.spinner("Creating your personalized action plan..."):
                action_plan = services['llm'].create_action_plan(current_avg, target_emissions)

            st.markdown("### Your Personalized Action Plan")
            st.markdown(action_plan)

        # Progress visualization
        st.divider()
        st.subheader("Progress Toward Goals")

        goal_data = {
            'Current': current_avg,
            'Your Target': target_emissions,
            'Paris Agreement': TARGETS['paris_agreement_daily']
        }

        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Bar(
                x=list(goal_data.keys()),
                y=list(goal_data.values()),
                marker_color=['#E74C3C', '#3498DB', '#2ECC71'],
                text=[f"{v:.1f}" for v in goal_data.values()],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Your Goals at a Glance",
            yaxis_title="kg CO₂/day",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Track your footprint for at least a week to set meaningful goals and create action plans!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #7F8C8D; padding: 1rem;'>
    <p><strong>Every action counts.</strong> Together we can build a sustainable future.</p>
    <p style='font-size: 0.9rem;'>Powered by Ollama Llama3:8b | Data sources: NOAA, Carbon Intensity API, Climate.gov</p>
</div>
""", unsafe_allow_html=True)
