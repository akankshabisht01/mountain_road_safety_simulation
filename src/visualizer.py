"""
Mountain Road Safety Simulator - Visualization Module
Creates interactive charts, maps, and risk visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


class RoadVisualizer:
    """Creates visualizations for road safety analysis"""
    
    def __init__(self):
        self.risk_colors = {
            'CRITICAL': '#8B0000',
            'EXTREME': '#FF0000',
            'HIGH': '#FF8C00',
            'MEDIUM': '#FFD700',
            'LOW': '#32CD32'
        }
    
    def create_elevation_profile_with_risk(self, simulation_results: pd.DataFrame) -> go.Figure:
        """
        Create elevation profile overlaid with risk indicators
        
        Args:
            simulation_results: DataFrame with simulation results
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Road Elevation Profile', 'Risk Distribution'),
            row_heights=[0.6, 0.4],
            vertical_spacing=0.12,
            specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
        )
        
        # Elevation profile
        fig.add_trace(
            go.Scatter(
                x=simulation_results['Distance_km'],
                y=simulation_results['Elevation_m'],
                name='Elevation',
                mode='lines',
                line=dict(color='#2E86AB', width=2),
                fill='tozeroy',
                fillcolor='rgba(46, 134, 171, 0.3)'
            ),
            row=1, col=1
        )
        
        # Risk overlay - color coded segments
        risk_colors_map = {
            'Green': '#32CD32',
            'Yellow': '#FFD700',
            'Red': '#FF8C00',
            'Extreme': '#FF0000'
        }
        
        for risk_category, color in risk_colors_map.items():
            risk_data = simulation_results[simulation_results['Risk_Category'] == risk_category]
            if not risk_data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=risk_data['Distance_km'],
                        y=risk_data['Elevation_m'],
                        name=f'{risk_category} Risk',
                        mode='markers',
                        marker=dict(
                            size=10,
                            color=color,
                            symbol='diamond',
                            line=dict(color='white', width=1)
                        )
                    ),
                    row=1, col=1
                )
        
        # Risk score line
        fig.add_trace(
            go.Scatter(
                x=simulation_results['Distance_km'],
                y=simulation_results['Final_Risk'] * 100,
                name='Risk Score (%)',
                mode='lines',
                line=dict(color='red', width=2, dash='dot'),
                yaxis='y2'
            ),
            row=1, col=1,
            secondary_y=True
        )
        
        # Risk distribution bar chart
        risk_categories = simulation_results['Risk_Category'].value_counts()
        fig.add_trace(
            go.Bar(
                x=risk_categories.index,
                y=risk_categories.values,
                marker=dict(
                    color=[risk_colors_map.get(cat, '#CCCCCC') for cat in risk_categories.index]
                ),
                text=risk_categories.values,
                textposition='auto',
                name='Segment Count',
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_xaxes(title_text="Distance (km)", row=1, col=1)
        fig.update_xaxes(title_text="Risk Category", row=2, col=1)
        fig.update_yaxes(title_text="Elevation (m)", row=1, col=1)
        fig.update_yaxes(title_text="Risk Score (%)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Number of Segments", row=2, col=1)
        
        fig.update_layout(
            height=800,
            title_text="<b>Bhikyasen Road - Elevation Profile & Risk Analysis</b>",
            title_font_size=20,
            showlegend=True,
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    def create_risk_heatmap(self, simulation_results: pd.DataFrame) -> go.Figure:
        """
        Create heatmap showing all risk factors across segments
        
        Args:
            simulation_results: DataFrame with simulation results
            
        Returns:
            Plotly figure object
        """
        # Prepare data for heatmap
        risk_data = simulation_results[['Segment', 'Stability_Risk', 'Brake_Failure_Risk', 
                                        'Cliff_Fall_Risk', 'Landslide_Risk', 'Final_Risk']].copy()
        
        # Transpose for heatmap
        heatmap_data = risk_data.set_index('Segment').T
        
        # Sample every nth segment for readability if too many segments
        if len(simulation_results) > 30:
            sample_segments = simulation_results['Segment'][::3].tolist()
            heatmap_data = heatmap_data[sample_segments]
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=['Stability', 'Brake Failure', 'Cliff Fall', 'Landslide', 'Overall Risk'],
            colorscale=[
                [0, '#32CD32'],      # Green
                [0.25, '#FFD700'],   # Yellow
                [0.5, '#FF8C00'],    # Orange
                [0.75, '#FF0000'],   # Red
                [1, '#8B0000']       # Dark Red
            ],
            text=np.round(heatmap_data.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Risk Score")
        ))
        
        fig.update_layout(
            title="<b>Multi-Hazard Risk Heatmap by Road Segment</b>",
            title_font_size=18,
            xaxis_title="Segment Number",
            yaxis_title="Risk Type",
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def create_brake_temperature_chart(self, simulation_results: pd.DataFrame) -> go.Figure:
        """
        Create brake temperature progression chart
        
        Args:
            simulation_results: DataFrame with simulation results
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Brake temperature line
        fig.add_trace(go.Scatter(
            x=simulation_results['Distance_km'],
            y=simulation_results['Brake_Temperature_C'],
            mode='lines+markers',
            name='Brake Temperature',
            line=dict(color='#FF4500', width=3),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(255, 69, 0, 0.2)'
        ))
        
        # Critical temperature threshold lines
        fig.add_hline(
            y=250, line_dash="dash", line_color="orange",
            annotation_text="Warning Threshold (250°C)",
            annotation_position="right"
        )
        
        fig.add_hline(
            y=350, line_dash="dash", line_color="red",
            annotation_text="Critical Threshold (350°C)",
            annotation_position="right"
        )
        
        # Highlight downhill sections
        downhill_segments = simulation_results[simulation_results['Is_Downhill']]
        if not downhill_segments.empty:
            fig.add_trace(go.Scatter(
                x=downhill_segments['Distance_km'],
                y=[20] * len(downhill_segments),  # Bottom of chart
                mode='markers',
                name='Downhill Section',
                marker=dict(
                    size=15,
                    symbol='triangle-down',
                    color='blue',
                    opacity=0.6
                ),
                showlegend=True
            ))
        
        fig.update_layout(
            title="<b>Brake Temperature Monitoring - Brake Failure Risk Assessment</b>",
            title_font_size=18,
            xaxis_title="Distance (km)",
            yaxis_title="Brake Temperature (°C)",
            height=500,
            hovermode='x unified',
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    def create_risk_gauge(self, risk_score: float, title: str = "Overall Risk") -> go.Figure:
        """
        Create gauge chart for risk score
        
        Args:
            risk_score: Risk score between 0 and 1
            title: Title for the gauge
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 24}},
            delta={'reference': 50, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 25], 'color': '#32CD32'},
                    {'range': [25, 40], 'color': '#FFD700'},
                    {'range': [40, 60], 'color': '#FF8C00'},
                    {'range': [60, 80], 'color': '#FF0000'},
                    {'range': [80, 100], 'color': '#8B0000'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig.update_layout(
            height=350,
            font={'color': "darkblue", 'family': "Arial"}
        )
        
        return fig
    
    def create_comparative_scenario_chart(self, scenarios: Dict[str, pd.DataFrame]) -> go.Figure:
        """
        Compare risk across different scenarios (Normal vs Rainy vs Overspeed)
        
        Args:
            scenarios: Dictionary with scenario names and their simulation results
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        colors = ['#32CD32', '#FF8C00', '#FF0000', '#8B0000']
        
        for idx, (scenario_name, results) in enumerate(scenarios.items()):
            fig.add_trace(go.Scatter(
                x=results['Distance_km'],
                y=results['Final_Risk'],
                mode='lines',
                name=scenario_name,
                line=dict(width=3, color=colors[idx % len(colors)])
            ))
        
        fig.update_layout(
            title="<b>Scenario Comparison: Risk Variation Under Different Conditions</b>",
            title_font_size=18,
            xaxis_title="Distance (km)",
            yaxis_title="Risk Score (0-1)",
            height=500,
            hovermode='x unified',
            template='plotly_white',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
    
    def create_risk_map_2d(self, simulation_results: pd.DataFrame) -> go.Figure:
        """
        Create 2D road map with color-coded risk segments
        
        Args:
            simulation_results: DataFrame with simulation results
            
        Returns:
            Plotly figure object
        """
        # Create synthetic coordinates for visualization (curved road)
        theta = np.linspace(0, 4 * np.pi, len(simulation_results))
        x = simulation_results['Distance_km'].values * np.cos(theta / 4)
        y = simulation_results['Distance_km'].values * np.sin(theta / 4)
        
        # Color mapping
        colors = simulation_results['Final_Risk'].apply(
            lambda r: '#8B0000' if r >= 0.8 else 
                     '#FF0000' if r >= 0.6 else 
                     '#FF8C00' if r >= 0.4 else 
                     '#FFD700' if r >= 0.25 else '#32CD32'
        )
        
        fig = go.Figure()
        
        # Road path
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines+markers',
            marker=dict(
                size=15,
                color=colors,
                line=dict(color='white', width=2)
            ),
            line=dict(color='gray', width=8),
            text=[f"Segment {s}<br>Risk: {r:.2f}<br>Elevation: {e}m" 
                  for s, r, e in zip(simulation_results['Segment'], 
                                     simulation_results['Final_Risk'],
                                     simulation_results['Elevation_m'])],
            hoverinfo='text',
            name='Road Segments'
        ))
        
        # Add start and end markers
        fig.add_trace(go.Scatter(
            x=[x[0]], y=[y[0]],
            mode='markers+text',
            marker=dict(size=20, color='green', symbol='star'),
            text=['START'],
            textposition='top center',
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=[x[-1]], y=[y[-1]],
            mode='markers+text',
            marker=dict(size=20, color='red', symbol='star'),
            text=['END'],
            textposition='top center',
            showlegend=False
        ))
        
        fig.update_layout(
            title="<b>Bhikyasen Road - 2D Risk Map (Color-Coded Danger Zones)</b>",
            title_font_size=18,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            showlegend=False,
            template='plotly_white',
            plot_bgcolor='#F5F5F5'
        )
        
        return fig
    
    def create_statistics_dashboard(self, risk_stats: Dict) -> go.Figure:
        """
        Create comprehensive statistics dashboard
        
        Args:
            risk_stats: Risk statistics dictionary
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                'Risk Distribution',
                'Hazard Breakdown',
                'Critical Metrics',
                'Segment Classification',
                'Temperature Analysis',
                'Safety Score'
            ),
            specs=[
                [{'type': 'indicator'}, {'type': 'pie'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'indicator'}, {'type': 'indicator'}]
            ]
        )
        
        # Average Risk Indicator
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=risk_stats['average_risk'] * 100,
            title={'text': "Avg Risk %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgreen"},
                    {'range': [40, 60], 'color': "yellow"},
                    {'range': [60, 100], 'color': "red"}
                ]
            }
        ), row=1, col=1)
        
        # Hazard Breakdown Pie
        hazards = {
            'Brake Failure': risk_stats['brake_critical_segments'],
            'Cliff Zones': risk_stats['cliff_zones'],
            'Landslide Zones': risk_stats['landslide_zones']
        }
        fig.add_trace(go.Pie(
            labels=list(hazards.keys()),
            values=list(hazards.values()),
            marker=dict(colors=['#FF4500', '#8B0000', '#DAA520'])
        ), row=1, col=2)
        
        # Critical Segments Bar
        segments_data = {
            'Critical': risk_stats['critical_segments'],
            'Extreme': risk_stats['extreme_segments'],
            'High Risk': risk_stats['high_risk_segments']
        }
        fig.add_trace(go.Bar(
            x=list(segments_data.keys()),
            y=list(segments_data.values()),
            marker_color=['#8B0000', '#FF0000', '#FF8C00'],
            text=list(segments_data.values()),
            textposition='auto'
        ), row=1, col=3)
        
        # Segment Classification Bar (row 2, col 1)
        classification_data = {
            'Low': risk_stats['total_segments'] - risk_stats['high_risk_segments'],
            'Medium': risk_stats['high_risk_segments'] - risk_stats['extreme_segments'],
            'High': risk_stats['extreme_segments'] - risk_stats['critical_segments'],
            'Critical': risk_stats['critical_segments']
        }
        fig.add_trace(go.Bar(
            x=list(classification_data.keys()),
            y=list(classification_data.values()),
            marker_color=['#32CD32', '#FFD700', '#FF8C00', '#8B0000'],
            text=list(classification_data.values()),
            textposition='auto'
        ), row=2, col=1)
        
        # Max Brake Temp Indicator
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=risk_stats['max_brake_temp'],
            title={'text': "Max Brake Temp (°C)"},
            delta={'reference': 250, 'increasing': {'color': "red"}},
            number={'font': {'size': 40}}
        ), row=2, col=2)
        
        # Most Dangerous Segment
        fig.add_trace(go.Indicator(
            mode="number",
            value=risk_stats['max_risk_segment'],
            title={'text': "Most Dangerous Segment"},
            number={'font': {'size': 50, 'color': 'red'}}
        ), row=2, col=3)
        
        fig.update_layout(
            height=700,
            showlegend=False,
            title_text="<b>Road Safety Statistics Dashboard</b>",
            title_font_size=20
        )
        
        return fig


def create_executive_summary_visual(report: Dict) -> go.Figure:
    """
    Create executive summary visualization
    
    Args:
        report: Safety report dictionary
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    summary = report['executive_summary']
    
    # Create text summary
    summary_text = f"""
    <b>EXECUTIVE SUMMARY</b><br>
    <br>
    Vehicle Type: {report['vehicle_type']}<br>
    Environment: {report['environment_condition']}<br>
    <br>
    <b>Overall Risk Score:</b> {summary['total_risk_score']:.2%}<br>
    <b>Most Dangerous Segment:</b> #{summary['most_dangerous_segment']}<br>
    <b>Critical Action Items:</b> {summary['critical_action_items']}<br>
    <br>
    <b>Key Hazards Identified:</b><br>
    """
    
    for hazard in summary['key_hazards']:
        summary_text += f"• {hazard}<br>"
    
    fig.add_annotation(
        text=summary_text,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, family="Arial"),
        align="left",
        bgcolor="white",
        bordercolor="black",
        borderwidth=2
    )
    
    fig.update_layout(
        height=400,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#F0F0F0'
    )
    
    return fig
