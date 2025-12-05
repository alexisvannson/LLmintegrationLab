"""
Data visualization module using Plotly for interactive charts
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List, Dict
from datetime import datetime
import pandas as pd


def create_emissions_breakdown_pie(breakdown: Dict) -> go.Figure:
    """
    Create a pie chart showing emissions breakdown by category
    """
    categories = list(breakdown.keys())
    values = list(breakdown.values())

    # Filter out zero values
    non_zero = [(cat, val) for cat, val in zip(categories, values) if val > 0]
    if not non_zero:
        return None

    categories, values = zip(*non_zero)

    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.3,
        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']),
        textinfo='label+percent',
        textfont=dict(size=14)
    )])

    fig.update_layout(
        title="Daily Emissions Breakdown",
        showlegend=True,
        height=400,
        margin=dict(t=40, b=20, l=20, r=20)
    )

    return fig


def create_trend_chart(trend_data: List[Dict], target_line: float = 6.0) -> go.Figure:
    """
    Create a line chart showing emissions trend over time
    """
    if not trend_data:
        return None

    df = pd.DataFrame(trend_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    fig = go.Figure()

    # Main total emissions line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['total_emissions'],
        mode='lines+markers',
        name='Total Daily Emissions',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.1)'
    ))

    # Paris Agreement target line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=[target_line] * len(df),
        mode='lines',
        name='Paris Agreement Target (1.5°C)',
        line=dict(color='#2ECC71', width=2, dash='dash')
    ))

    # Add category breakdown as stacked area
    categories = ['transport_emissions', 'diet_emissions', 'heating_emissions',
                  'electricity_emissions', 'consumption_emissions']
    colors = ['#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C']

    for cat, color in zip(categories, colors):
        if cat in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[cat],
                mode='lines',
                name=cat.replace('_emissions', '').title(),
                line=dict(width=1),
                stackgroup='one',
                fillcolor=color
            ))

    fig.update_layout(
        title="Carbon Footprint Trend",
        xaxis_title="Date",
        yaxis_title="kg CO₂/day",
        hovermode='x unified',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, b=40, l=40, r=40)
    )

    return fig


def create_comparison_bar(user_avg: float, benchmarks: Dict) -> go.Figure:
    """
    Create a bar chart comparing user's average to global benchmarks
    """
    categories = ['Your Average', 'Paris Target', 'EU Average', 'World Average', 'US Average']
    values = [
        user_avg,
        benchmarks.get('paris_agreement_daily', 6.0),
        benchmarks.get('eu_average_daily', 20.0),
        benchmarks.get('world_average_daily', 12.0),
        benchmarks.get('us_average_daily', 44.0)
    ]
    colors = ['#3498DB', '#2ECC71', '#F39C12', '#E67E22', '#E74C3C']

    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors),
        text=[f'{v:.1f}' for v in values],
        textposition='auto',
        textfont=dict(size=14, color='white')
    )])

    fig.update_layout(
        title="How You Compare Globally",
        yaxis_title="kg CO₂/day",
        height=400,
        showlegend=False,
        margin=dict(t=40, b=40, l=40, r=40)
    )

    # Add horizontal line at Paris target
    fig.add_hline(
        y=6.0,
        line_dash="dash",
        line_color="green",
        annotation_text="1.5°C Target",
        annotation_position="right"
    )

    return fig


def create_progress_gauge(current: float, target: float = 6.0) -> go.Figure:
    """
    Create a gauge chart showing progress toward target
    """
    percentage = min((target / current) * 100, 100) if current > 0 else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Daily Footprint vs Target", 'font': {'size': 20}},
        delta={'reference': target, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, max(50, current * 1.2)], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, target], 'color': '#2ECC71'},
                {'range': [target, target * 2], 'color': '#F39C12'},
                {'range': [target * 2, max(50, current * 1.2)], 'color': '#E74C3C'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(t=40, b=20, l=20, r=20)
    )

    return fig


def create_category_comparison(current: Dict, average: Dict) -> go.Figure:
    """
    Create a grouped bar chart comparing current vs average emissions by category
    """
    categories = list(current.keys())
    current_values = list(current.values())
    average_values = [average.get(cat, 0) for cat in categories]

    fig = go.Figure(data=[
        go.Bar(name='Current', x=categories, y=current_values, marker_color='#3498DB'),
        go.Bar(name='Your 30-Day Avg', x=categories, y=average_values, marker_color='#95A5A6')
    ])

    fig.update_layout(
        title="Category Breakdown: Current vs Average",
        yaxis_title="kg CO₂/day",
        barmode='group',
        height=400,
        margin=dict(t=40, b=40, l=40, r=40)
    )

    return fig


def create_atmospheric_co2_indicator(co2_ppm: float) -> go.Figure:
    """
    Create an indicator showing current atmospheric CO2 levels
    """
    # Historical context: pre-industrial was ~280 ppm, safe limit ~350 ppm
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=co2_ppm,
        title={'text': "Atmospheric CO₂ (ppm)", 'font': {'size': 18}},
        delta={
            'reference': 350,
            'increasing': {'color': "red"},
            'suffix': " ppm above safe limit"
        },
        number={'suffix': " ppm", 'font': {'size': 36}}
    ))

    fig.update_layout(
        height=200,
        margin=dict(t=40, b=20, l=20, r=20)
    )

    return fig


def create_summary_metrics_chart(stats: Dict) -> go.Figure:
    """
    Create a summary chart with key metrics
    """
    if stats.get('record_count', 0) == 0:
        return None

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Average', 'Best Day', 'Worst Day'),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]]
    )

    fig.add_trace(go.Indicator(
        mode="number",
        value=stats.get('avg_daily_emissions', 0),
        title={'text': "Avg Daily", 'font': {'size': 14}},
        number={'suffix': " kg CO₂", 'font': {'size': 24}},
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="number",
        value=stats.get('min_emissions', 0),
        title={'text': "Best Day", 'font': {'size': 14}},
        number={'suffix': " kg CO₂", 'font': {'size': 24}, 'font.color': 'green'},
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="number",
        value=stats.get('max_emissions', 0),
        title={'text': "Worst Day", 'font': {'size': 14}},
        number={'suffix': " kg CO₂", 'font': {'size': 24}, 'font.color': 'red'},
    ), row=1, col=3)

    fig.update_layout(
        height=200,
        margin=dict(t=60, b=20, l=20, r=20),
        showlegend=False
    )

    return fig
