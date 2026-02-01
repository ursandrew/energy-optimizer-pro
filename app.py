"""
ENERGY MODELING OPTIMIZER BY SJ
===============================
Professional renewable energy optimization tool with BCG-style interface.
Version 4.0 - Enhanced with Interactive Topology
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Energy Optimizer Pro | by SJ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Dark Theme
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    
    .big-font {
        font-size: 48px !important;
        font-weight: bold;
        background: linear-gradient(90deg, #00D9FF 0%, #00FFB3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .subtitle {
        font-size: 22px;
        color: #00D9FF;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
        letter-spacing: 3px;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border: 2px solid #00D9FF;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.2);
    }
    
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 217, 255, 0.4);
    }
    
    .component-card {
        background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
        border: 2px solid #00FF88;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.15);
    }
    
    .component-card-disabled {
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        border: 2px solid #666;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        opacity: 0.5;
    }
    
    .status-enabled {
        color: #00FF88;
        font-weight: bold;
        font-size: 18px;
    }
    
    .status-disabled {
        color: #FF6B6B;
        font-weight: bold;
        font-size: 18px;
    }
    
    .topology-title {
        font-size: 32px;
        font-weight: bold;
        color: #00D9FF;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# TOPOLOGY DIAGRAM FUNCTION
# ============================================================================

def create_interactive_topology(pv_cfg, wind_cfg, hydro_cfg, bess_cfg):
    """Create interactive energy system topology diagram."""
    
    fig = go.Figure()
    
    # Node positions (x, y)
    nodes = {
        'pv': (0.15, 0.85),
        'wind': (0.15, 0.5),
        'hydro': (0.15, 0.15),
        'bus': (0.5, 0.5),
        'bess': (0.75, 0.5),
        'load': (0.95, 0.5)
    }
    
    # Colors based on enabled state
    colors = {
        'pv': '#FDB462' if pv_cfg['enabled'] else '#555555',
        'wind': '#80B1D3' if wind_cfg['enabled'] else '#555555',
        'hydro': '#8DD3C7' if hydro_cfg['enabled'] else '#555555',
        'bus': '#FFD700',
        'bess': '#FB8072' if bess_cfg['enabled'] else '#555555',
        'load': '#B3DE69'
    }
    
    # Draw connection lines (edges)
    edges = []
    if pv_cfg['enabled']:
        edges.append(('pv', 'bus', '#FDB462'))
    if wind_cfg['enabled']:
        edges.append(('wind', 'bus', '#80B1D3'))
    if hydro_cfg['enabled']:
        edges.append(('hydro', 'bus', '#8DD3C7'))
    
    edges.append(('bus', 'load', '#FFD700'))
    
    if bess_cfg['enabled']:
        edges.append(('bus', 'bess', '#FB8072'))
    
    # Draw edges as animated lines
    for start_node, end_node, color in edges:
        x0, y0 = nodes[start_node]
        x1, y1 = nodes[end_node]
        
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color=color, width=4, dash='solid'),
            opacity=0.8,
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Add arrow at midpoint
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        angle = np.arctan2(y1 - y0, x1 - x0)
        
        fig.add_annotation(
            x=mid_x,
            y=mid_y,
            ax=mid_x - 0.02 * np.cos(angle),
            ay=mid_y - 0.02 * np.sin(angle),
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=3,
            arrowcolor=color
        )
    
    # Node information
    node_info = {
        'pv': {
            'name': 'Solar PV',
            'icon': '☀️',
            'capacity': f"{pv_cfg['min']:.1f}-{pv_cfg['max']:.1f} MW" if pv_cfg['enabled'] else "Disabled",
            'status': '✅ Online' if pv_cfg['enabled'] else '❌ Offline'
        },
        'wind': {
            'name': 'Wind Turbine',
            'icon': '💨',
            'capacity': f"{wind_cfg['min']:.1f}-{wind_cfg['max']:.1f} MW" if wind_cfg['enabled'] else "Disabled",
            'status': '✅ Online' if wind_cfg['enabled'] else '❌ Offline'
        },
        'hydro': {
            'name': 'Hydro Power',
            'icon': '💧',
            'capacity': f"{hydro_cfg['min']:.1f}-{hydro_cfg['max']:.1f} MW" if hydro_cfg['enabled'] else "Disabled",
            'status': '✅ Online' if hydro_cfg['enabled'] else '❌ Offline'
        },
        'bus': {
            'name': 'Electricity Grid',
            'icon': '⚡',
            'capacity': 'Distribution Hub',
            'status': '✅ Active'
        },
        'bess': {
            'name': 'Battery Storage',
            'icon': '🔋',
            'capacity': f"{bess_cfg['min_power']:.1f}-{bess_cfg['max_power']:.1f} MW" if bess_cfg['enabled'] else "Disabled",
            'status': '✅ Online' if bess_cfg['enabled'] else '❌ Offline'
        },
        'load': {
            'name': 'Load Demand',
            'icon': '🏭',
            'capacity': 'Consumer Load',
            'status': '✅ Active'
        }
    }
    
    # Draw nodes
    for node, (x, y) in nodes.items():
        info = node_info[node]
        
        # Node circle
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=80,
                color=colors[node],
                line=dict(color='white', width=4),
                opacity=1.0 if node in ['bus', 'load'] or (node == 'pv' and pv_cfg['enabled']) or 
                         (node == 'wind' and wind_cfg['enabled']) or (node == 'hydro' and hydro_cfg['enabled']) or 
                         (node == 'bess' and bess_cfg['enabled']) else 0.4
            ),
            text=info['icon'],
            textfont=dict(size=32),
            textposition='middle center',
            hovertemplate=(
                f"<b>{info['name']}</b><br>"
                f"Status: {info['status']}<br>"
                f"Capacity: {info['capacity']}<br>"
                "<extra></extra>"
            ),
            name=info['name'],
            showlegend=False
        ))
        
        # Labels below nodes
        fig.add_annotation(
            x=x,
            y=y - 0.12,
            text=f"<b>{info['name']}</b>",
            showarrow=False,
            font=dict(size=14, color='white'),
            align='center'
        )
        
        # Capacity label
        fig.add_annotation(
            x=x,
            y=y - 0.16,
            text=f"<i>{info['capacity']}</i>",
            showarrow=False,
            font=dict(size=11, color='#00D9FF'),
            align='center'
        )
    
    # Update layout
    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[0, 1.1]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[0, 1.0]
        ),
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='closest'
    )
    
    return fig

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'pv_config' not in st.session_state:
    st.session_state.pv_config = {
        'enabled': True, 'min': 1.0, 'max': 5.0, 'step': 1.0,
        'capex': 1000, 'opex': 10, 'lifetime': 25, 'profile': None
    }

if 'wind_config' not in st.session_state:
    st.session_state.wind_config = {
        'enabled': True, 'min': 0.0, 'max': 3.0, 'step': 1.0,
        'capex': 1200, 'opex': 15, 'lifetime': 20, 'profile': None
    }

if 'hydro_config' not in st.session_state:
    st.session_state.hydro_config = {
        'enabled': True, 'min': 0.0, 'max': 2.0, 'step': 1.0,
        'hours_per_day': 8, 'capex': 2000, 'opex': 20, 'lifetime': 50, 'profile': None
    }

if 'bess_config' not in st.session_state:
    st.session_state.bess_config = {
        'enabled': True, 'min_power': 5.0, 'max_power': 20.0, 'step_power': 5.0,
        'duration': 4.0, 'min_soc': 20, 'max_soc': 100,
        'charge_eff': 95, 'discharge_eff': 95,
        'power_capex': 300, 'energy_capex': 200, 'opex': 2, 'lifetime': 15
    }

if 'load_profile' not in st.session_state:
    st.session_state.load_profile = None

if 'target_unmet' not in st.session_state:
    st.session_state.target_unmet = 0.1

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<p class="big-font">⚡ ENERGY MODELING OPTIMIZER</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">BY SJ</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["🔌 System Design", "⚙️ Optimize", "📊 Results"])

# ============================================================================
# TAB 1: SYSTEM DESIGN
# ============================================================================

with tab1:
    
    # Topology Diagram
    st.markdown('<p class="topology-title">🔌 System Architecture</p>', unsafe_allow_html=True)
    st.markdown("**Interactive Energy Flow Diagram** - Click components below to configure")
    
    topology_fig = create_interactive_topology(
        st.session_state.pv_config,
        st.session_state.wind_config,
        st.session_state.hydro_config,
        st.session_state.bess_config
    )
    
    st.plotly_chart(topology_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Component Configuration Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("☀️ Configure Solar PV", use_container_width=True, type="primary"):
            st.session_state.selected_component = 'pv'
            st.rerun()
    
    with col2:
        if st.button("💨 Configure Wind", use_container_width=True, type="primary"):
            st.session_state.selected_component = 'wind'
            st.rerun()
    
    with col3:
        if st.button("💧 Configure Hydro", use_container_width=True, type="primary"):
            st.session_state.selected_component = 'hydro'
            st.rerun()
    
    with col4:
        if st.button("🔋 Configure BESS", use_container_width=True, type="primary"):
            st.session_state.selected_component = 'bess'
            st.rerun()
    
    st.markdown("---")
    
    # Component Configuration Panel
    if 'selected_component' in st.session_state and st.session_state.selected_component:
        
        if st.session_state.selected_component == 'pv':
            st.markdown("## ☀️ Solar PV Configuration")
            
            enabled = st.toggle("Enable Solar PV", value=st.session_state.pv_config['enabled'], key="pv_toggle")
            
            if enabled:
                st.markdown("### 📊 Capacity Search Range")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Minimum Capacity**")
                    min_cap = st.slider("Min (MW)", 0.0, 50.0, st.session_state.pv_config['min'], 0.5, key="pv_min")
                    st.metric("Minimum", f"{min_cap:.1f} MW", label_visibility="collapsed")
                
                with col2:
                    st.markdown("**Maximum Capacity**")
                    max_cap = st.slider("Max (MW)", 0.0, 50.0, st.session_state.pv_config['max'], 0.5, key="pv_max")
                    st.metric("Maximum", f"{max_cap:.1f} MW", label_visibility="collapsed")
                
                st.markdown("**Search Step Size**")
                step = st.slider("Step (MW)", 0.1, 10.0, st.session_state.pv_config['step'], 0.1, key="pv_step")
                
                num_opts = int((max_cap - min_cap) / step) + 1 if step > 0 else 1
                if num_opts <= 10:
                    st.success(f"🟢 **{num_opts} configurations** - Small search space")
                elif num_opts <= 50:
                    st.warning(f"🟡 **{num_opts} configurations** - Medium search space")
                else:
                    st.error(f"🔴 **{num_opts} configurations** - Large search space")
                
                st.markdown("---")
                st.markdown("### 💰 Financial Parameters")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    capex = st.number_input("CapEx ($/kW)", value=st.session_state.pv_config['capex'], step=50, key="pv_capex")
                with col2:
                    opex = st.number_input("OpEx ($/kW/yr)", value=st.session_state.pv_config['opex'], step=1, key="pv_opex")
                with col3:
                    lifetime = st.number_input("Lifetime (years)", value=st.session_state.pv_config['lifetime'], step=1, key="pv_lifetime")
                
                st.markdown("---")
                st.markdown("### 📁 PV Generation Profile")
                pv_file = st.file_uploader("Upload PV Profile (1 kW normalized)", type=['csv', 'xlsx'], key="pv_file_upload")
                
                if pv_file:
                    st.success(f"✅ Loaded: {pv_file.name}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("✅ Save Solar PV Configuration", type="primary", use_container_width=True):
                        st.session_state.pv_config = {
                            'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                            'capex': capex, 'opex': opex, 'lifetime': lifetime,
                            'profile': pv_file
                        }
                        st.success("✅ Solar PV configuration saved!")
                        del st.session_state.selected_component
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", type="secondary", use_container_width=True):
                        del st.session_state.selected_component
                        st.rerun()
            
            else:
                if st.button("✅ Save Configuration", type="primary"):
                    st.session_state.pv_config['enabled'] = False
                    st.success("✅ Solar PV disabled!")
                    del st.session_state.selected_component
                    st.rerun()
        
        elif st.session_state.selected_component == 'wind':
            st.markdown("## 💨 Wind Configuration")
            
            enabled = st.toggle("Enable Wind", value=st.session_state.wind_config['enabled'], key="wind_toggle")
            
            if enabled:
                st.markdown("### 📊 Capacity Search Range")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Minimum Capacity**")
                    min_cap = st.slider("Min (MW)", 0.0, 50.0, st.session_state.wind_config['min'], 0.5, key="wind_min")
                    st.metric("Minimum", f"{min_cap:.1f} MW", label_visibility="collapsed")
                
                with col2:
                    st.markdown("**Maximum Capacity**")
                    max_cap = st.slider("Max (MW)", 0.0, 50.0, st.session_state.wind_config['max'], 0.5, key="wind_max")
                    st.metric("Maximum", f"{max_cap:.1f} MW", label_visibility="collapsed")
                
                st.markdown("**Search Step Size**")
                step = st.slider("Step (MW)", 0.1, 10.0, st.session_state.wind_config['step'], 0.1, key="wind_step")
                
                num_opts = int((max_cap - min_cap) / step) + 1 if step > 0 else 1
                if num_opts <= 10:
                    st.success(f"🟢 **{num_opts} configurations** - Small search space")
                elif num_opts <= 50:
                    st.warning(f"🟡 **{num_opts} configurations** - Medium search space")
                else:
                    st.error(f"🔴 **{num_opts} configurations** - Large search space")
                
                st.markdown("---")
                st.markdown("### 💰 Financial Parameters")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    capex = st.number_input("CapEx ($/kW)", value=st.session_state.wind_config['capex'], step=50, key="wind_capex")
                with col2:
                    opex = st.number_input("OpEx ($/kW/yr)", value=st.session_state.wind_config['opex'], step=1, key="wind_opex")
                with col3:
                    lifetime = st.number_input("Lifetime (years)", value=st.session_state.wind_config['lifetime'], step=1, key="wind_lifetime")
                
                st.markdown("---")
                st.markdown("### 📁 Wind Generation Profile")
                wind_file = st.file_uploader("Upload Wind Profile (1 kW normalized)", type=['csv', 'xlsx'], key="wind_file_upload")
                
                if wind_file:
                    st.success(f"✅ Loaded: {wind_file.name}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("✅ Save Wind Configuration", type="primary", use_container_width=True):
                        st.session_state.wind_config = {
                            'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                            'capex': capex, 'opex': opex, 'lifetime': lifetime,
                            'profile': wind_file
                        }
                        st.success("✅ Wind configuration saved!")
                        del st.session_state.selected_component
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", type="secondary", use_container_width=True):
                        del st.session_state.selected_component
                        st.rerun()
            
            else:
                if st.button("✅ Save Configuration", type="primary"):
                    st.session_state.wind_config['enabled'] = False
                    st.success("✅ Wind disabled!")
                    del st.session_state.selected_component
                    st.rerun()
        
        elif st.session_state.selected_component == 'hydro':
            st.markdown("## 💧 Hydro Configuration")
            
            enabled = st.toggle("Enable Hydro", value=st.session_state.hydro_config['enabled'], key="hydro_toggle")
            
            if enabled:
                st.markdown("### 📊 Capacity Search Range")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Minimum Capacity**")
                    min_cap = st.slider("Min (MW)", 0.0, 30.0, st.session_state.hydro_config['min'], 0.5, key="hydro_min")
                    st.metric("Minimum", f"{min_cap:.1f} MW", label_visibility="collapsed")
                
                with col2:
                    st.markdown("**Maximum Capacity**")
                    max_cap = st.slider("Max (MW)", 0.0, 30.0, st.session_state.hydro_config['max'], 0.5, key="hydro_max")
                    st.metric("Maximum", f"{max_cap:.1f} MW", label_visibility="collapsed")
                
                st.markdown("**Search Step Size**")
                step = st.slider("Step (MW)", 0.1, 10.0, st.session_state.hydro_config['step'], 0.1, key="hydro_step")
                
                num_opts = int((max_cap - min_cap) / step) + 1 if step > 0 else 1
                if num_opts <= 10:
                    st.success(f"🟢 **{num_opts} configurations** - Small search space")
                elif num_opts <= 50:
                    st.warning(f"🟡 **{num_opts} configurations** - Medium search space")
                else:
                    st.error(f"🔴 **{num_opts} configurations** - Large search space")
                
                st.markdown("---")
                st.markdown("### ⚙️ Operating Configuration")
                hours = st.slider("Operating Hours per Day", 1, 24, st.session_state.hydro_config['hours_per_day'], key="hydro_hours")
                
                st.markdown("---")
                st.markdown("### 💰 Financial Parameters")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    capex = st.number_input("CapEx ($/kW)", value=st.session_state.hydro_config['capex'], step=50, key="hydro_capex")
                with col2:
                    opex = st.number_input("OpEx ($/kW/yr)", value=st.session_state.hydro_config['opex'], step=1, key="hydro_opex")
                with col3:
                    lifetime = st.number_input("Lifetime (years)", value=st.session_state.hydro_config['lifetime'], step=1, key="hydro_lifetime")
                
                st.markdown("---")
                st.markdown("### 📁 Hydro Generation Profile (Optional)")
                hydro_file = st.file_uploader("Upload Hydro Profile", type=['csv', 'xlsx'], key="hydro_file_upload")
                
                if hydro_file:
                    st.success(f"✅ Loaded: {hydro_file.name}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("✅ Save Hydro Configuration", type="primary", use_container_width=True):
                        st.session_state.hydro_config = {
                            'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                            'hours_per_day': hours, 'capex': capex, 'opex': opex, 'lifetime': lifetime,
                            'profile': hydro_file
                        }
                        st.success("✅ Hydro configuration saved!")
                        del st.session_state.selected_component
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", type="secondary", use_container_width=True):
                        del st.session_state.selected_component
                        st.rerun()
            
            else:
                if st.button("✅ Save Configuration", type="primary"):
                    st.session_state.hydro_config['enabled'] = False
                    st.success("✅ Hydro disabled!")
                    del st.session_state.selected_component
                    st.rerun()
        
        elif st.session_state.selected_component == 'bess':
            st.markdown("## 🔋 Battery Energy Storage Configuration")
            
            enabled = st.toggle("Enable BESS", value=st.session_state.bess_config['enabled'], key="bess_toggle")
            
            if enabled:
                st.markdown("### ⚡ Power Capacity Range")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Minimum Power**")
                    min_pow = st.slider("Min (MW)", 0.0, 100.0, st.session_state.bess_config['min_power'], 1.0, key="bess_min")
                    st.metric("Minimum", f"{min_pow:.1f} MW", label_visibility="collapsed")
                
                with col2:
                    st.markdown("**Maximum Power**")
                    max_pow = st.slider("Max (MW)", 0.0, 100.0, st.session_state.bess_config['max_power'], 1.0, key="bess_max")
                    st.metric("Maximum", f"{max_pow:.1f} MW", label_visibility="collapsed")
                
                st.markdown("**Search Step Size**")
                step_pow = st.slider("Step (MW)", 0.5, 20.0, st.session_state.bess_config['step_power'], 0.5, key="bess_step")
                
                num_opts = int((max_pow - min_pow) / step_pow) + 1 if step_pow > 0 else 1
                if num_opts <= 10:
                    st.success(f"🟢 **{num_opts} configurations** - Small search space")
                elif num_opts <= 50:
                    st.warning(f"🟡 **{num_opts} configurations** - Medium search space")
                else:
                    st.error(f"🔴 **{num_opts} configurations** - Large search space")
                
                st.markdown("---")
                st.markdown("### 🔋 Energy Storage Parameters")
                
                col1, col2 = st.columns(2)
                with col1:
                    duration = st.slider("Duration (hours)", 0.5, 8.0, st.session_state.bess_config['duration'], 0.5, key="bess_duration")
                    min_soc = st.slider("Min SOC (%)", 0, 100, st.session_state.bess_config['min_soc'], 5, key="bess_min_soc")
                    charge_eff = st.slider("Charge Efficiency (%)", 50, 100, st.session_state.bess_config['charge_eff'], 1, key="bess_charge_eff")
                
                with col2:
                    max_energy = max_pow * duration
                    st.metric("Energy Capacity", f"{max_energy:.1f} MWh", help="Calculated as Max Power × Duration")
                    max_soc = st.slider("Max SOC (%)", 0, 100, st.session_state.bess_config['max_soc'], 5, key="bess_max_soc")
                    discharge_eff = st.slider("Discharge Efficiency (%)", 50, 100, st.session_state.bess_config['discharge_eff'], 1, key="bess_discharge_eff")
                
                st.markdown("---")
                st.markdown("### 💰 Financial Parameters")
                
                col1, col2 = st.columns(2)
                with col1:
                    power_capex = st.number_input("Power CapEx ($/kW)", value=st.session_state.bess_config['power_capex'], step=10, key="bess_power_capex")
                    energy_capex = st.number_input("Energy CapEx ($/kWh)", value=st.session_state.bess_config['energy_capex'], step=10, key="bess_energy_capex")
                
                with col2:
                    opex = st.number_input("OpEx ($/kW/yr)", value=st.session_state.bess_config['opex'], step=1, key="bess_opex")
                    lifetime = st.number_input("Lifetime (years)", value=st.session_state.bess_config['lifetime'], step=1, key="bess_lifetime")
                
                # Cost preview
                total_power_cost = power_capex * max_pow * 1000
                total_energy_cost = energy_capex * max_energy * 1000
                total_bess_capex = total_power_cost + total_energy_cost
                
                st.info(f"💵 **Estimated Total CapEx (at max capacity):** ${total_bess_capex/1e6:.2f}M")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("✅ Save BESS Configuration", type="primary", use_container_width=True):
                        st.session_state.bess_config = {
                            'enabled': enabled, 'min_power': min_pow, 'max_power': max_pow, 'step_power': step_pow,
                            'duration': duration, 'min_soc': min_soc, 'max_soc': max_soc,
                            'charge_eff': charge_eff, 'discharge_eff': discharge_eff,
                            'power_capex': power_capex, 'energy_capex': energy_capex,
                            'opex': opex, 'lifetime': lifetime
                        }
                        st.success("✅ BESS configuration saved!")
                        del st.session_state.selected_component
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", type="secondary", use_container_width=True):
                        del st.session_state.selected_component
                        st.rerun()
            
            else:
                if st.button("✅ Save Configuration", type="primary"):
                    st.session_state.bess_config['enabled'] = False
                    st.success("✅ BESS disabled!")
                    del st.session_state.selected_component
                    st.rerun()
    
    else:
        # Show configuration summary
        st.markdown("## 📋 Configuration Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # PV Summary
            if st.session_state.pv_config['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown('### ☀️ Solar PV <span class="status-enabled">✅ ENABLED</span>', unsafe_allow_html=True)
                st.write(f"**Range:** {st.session_state.pv_config['min']:.1f} - {st.session_state.pv_config['max']:.1f} MW")
                st.write(f"**Step:** {st.session_state.pv_config['step']:.1f} MW")
                st.write(f"**CapEx:** ${st.session_state.pv_config['capex']}/kW")
                st.write(f"**Profile:** {'✅ Uploaded' if st.session_state.pv_config.get('profile') else '❌ Not uploaded'}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown('### ☀️ Solar PV <span class="status-disabled">❌ DISABLED</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Hydro Summary
            if st.session_state.hydro_config['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown('### 💧 Hydro <span class="status-enabled">✅ ENABLED</span>', unsafe_allow_html=True)
                st.write(f"**Range:** {st.session_state.hydro_config['min']:.1f} - {st.session_state.hydro_config['max']:.1f} MW")
                st.write(f"**Step:** {st.session_state.hydro_config['step']:.1f} MW")
                st.write(f"**Hours/day:** {st.session_state.hydro_config['hours_per_day']}")
                st.write(f"**Profile:** {'✅ Uploaded' if st.session_state.hydro_config.get('profile') else '⚠️ Optional'}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown('### 💧 Hydro <span class="status-disabled">❌ DISABLED</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Wind Summary
            if st.session_state.wind_config['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown('### 💨 Wind <span class="status-enabled">✅ ENABLED</span>', unsafe_allow_html=True)
                st.write(f"**Range:** {st.session_state.wind_config['min']:.1f} - {st.session_state.wind_config['max']:.1f} MW")
                st.write(f"**Step:** {st.session_state.wind_config['step']:.1f} MW")
                st.write(f"**CapEx:** ${st.session_state.wind_config['capex']}/kW")
                st.write(f"**Profile:** {'✅ Uploaded' if st.session_state.wind_config.get('profile') else '❌ Not uploaded'}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown('### 💨 Wind <span class="status-disabled">❌ DISABLED</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # BESS Summary
            if st.session_state.bess_config['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown('### 🔋 BESS <span class="status-enabled">✅ ENABLED</span>', unsafe_allow_html=True)
                st.write(f"**Power:** {st.session_state.bess_config['min_power']:.1f} - {st.session_state.bess_config['max_power']:.1f} MW")
                st.write(f"**Duration:** {st.session_state.bess_config['duration']:.1f} hours")
                max_e = st.session_state.bess_config['max_power'] * st.session_state.bess_config['duration']
                st.write(f"**Max Energy:** {max_e:.1f} MWh")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown('### 🔋 BESS <span class="status-disabled">❌ DISABLED</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 2: OPTIMIZE
# ============================================================================

with tab2:
    st.header("⚙️ Run Optimization")
    
    st.info("🚧 **Optimization engine integration coming next**")
    
    st.markdown("""
    ### Ready for Integration
    
    Your existing optimization engine will be integrated here to:
    - Read all component configurations
    - Process uploaded profiles
    - Execute grid search optimization
    - Calculate NPC, LCOE, and electrical metrics
    - Display real-time progress
    """)

# ============================================================================
# TAB 3: RESULTS
# ============================================================================

with tab3:
    st.header("📊 Optimization Results")
    st.info("ℹ️ No results yet. Run optimization first.")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Global Settings")
    
    st.markdown("#### 💰 Financial Parameters")
    discount_rate = st.number_input("Discount Rate (%)", value=8.0, step=0.5, key="discount_rate")
    inflation_rate = st.number_input("Inflation Rate (%)", value=2.0, step=0.5, key="inflation_rate")
    project_lifetime = st.number_input("Project Lifetime (years)", value=25, step=1, min_value=1, max_value=50, key="project_lifetime")
    
    st.markdown("---")
    st.markdown("#### 🏭 Load Profile & Constraints")
    
    load_file = st.file_uploader("📁 Load Profile (kW)", type=['csv', 'xlsx'], key="load_file_upload")
    if load_file:
        st.success(f"✅ Loaded: {load_file.name}")
        st.session_state.load_profile = load_file
    
    target_unmet = st.number_input("Target Unmet Load (%)", value=0.1, step=0.1, min_value=0.0, max_value=5.0, key="target_unmet_input")
    st.session_state.target_unmet = target_unmet
    
    st.markdown("---")
    
    # Calculate search space
    pv_opts = int((st.session_state.pv_config['max'] - st.session_state.pv_config['min']) / 
                  st.session_state.pv_config['step']) + 1 if st.session_state.pv_config['enabled'] and st.session_state.pv_config['step'] > 0 else 1
    wind_opts = int((st.session_state.wind_config['max'] - st.session_state.wind_config['min']) / 
                    st.session_state.wind_config['step']) + 1 if st.session_state.wind_config['enabled'] and st.session_state.wind_config['step'] > 0 else 1
    hydro_opts = int((st.session_state.hydro_config['max'] - st.session_state.hydro_config['min']) / 
                     st.session_state.hydro_config['step']) + 1 if st.session_state.hydro_config['enabled'] and st.session_state.hydro_config['step'] > 0 else 1
    bess_opts = int((st.session_state.bess_config['max_power'] - st.session_state.bess_config['min_power']) / 
                    st.session_state.bess_config['step_power']) + 1 if st.session_state.bess_config['enabled'] and st.session_state.bess_config['step_power'] > 0 else 1
    
    total_combinations = pv_opts * wind_opts * hydro_opts * bess_opts
    
    st.markdown("### 📊 Search Space")
    st.metric("Total Combinations", f"{total_combinations:,}")
    st.metric("PV Options", pv_opts)
    st.metric("Wind Options", wind_opts)
    st.metric("Hydro Options", hydro_opts)
    st.metric("BESS Options", bess_opts)
    
    est_time = max(1, total_combinations * 0.05 / 60)
    st.metric("Est. Runtime", f"{est_time:.1f} min")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00D9FF; padding: 20px;">
    <p style="font-size: 18px;"><b>⚡ Energy Modeling Optimizer v4.0 Professional</b></p>
    <p style="font-size: 14px;">Developed by SJ | 2026</p>
    <p style="font-size: 12px; color: #666;">Professional Energy System Optimization Tool</p>
</div>
""", unsafe_allow_html=True)
