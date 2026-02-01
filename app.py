"""
ENERGY MODELING OPTIMIZER BY SJ
===============================
Professional renewable energy optimization tool with BCG-style interface.
Version 4.0 - Enhanced Edition
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
</style>
""", unsafe_allow_html=True)

# ============================================================================
# TOPOLOGY DIAGRAM FUNCTION
# ============================================================================

def create_topology_diagram(pv_enabled, wind_enabled, hydro_enabled, bess_enabled,
                            pv_range="", wind_range="", hydro_range="", bess_range=""):
    """Create interactive topology diagram."""
    
    fig = go.Figure()
    
    # Node positions
    node_pos = {
        'pv': (0.15, 0.85),
        'wind': (0.15, 0.5),
        'hydro': (0.15, 0.15),
        'bus': (0.5, 0.5),
        'bess': (0.75, 0.5),
        'load': (0.95, 0.5)
    }
    
    # Colors
    node_colors = {
        'pv': '#FDB462' if pv_enabled else '#555555',
        'wind': '#80B1D3' if wind_enabled else '#555555',
        'hydro': '#8DD3C7' if hydro_enabled else '#555555',
        'bus': '#FFD700',
        'bess': '#FB8072' if bess_enabled else '#555555',
        'load': '#B3DE69'
    }
    
    # Draw edges
    edges = []
    if pv_enabled:
        edges.append(('pv', 'bus', '#FDB462'))
    if wind_enabled:
        edges.append(('wind', 'bus', '#80B1D3'))
    if hydro_enabled:
        edges.append(('hydro', 'bus', '#8DD3C7'))
    edges.append(('bus', 'load', '#FFD700'))
    if bess_enabled:
        edges.append(('bus', 'bess', '#FB8072'))
    
    for start, end, color in edges:
        x0, y0 = node_pos[start]
        x1, y1 = node_pos[end]
        
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color=color, width=4),
            opacity=0.8,
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Arrow
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        angle = np.arctan2(y1 - y0, x1 - x0)
        
        fig.add_annotation(
            x=mid_x, y=mid_y,
            ax=mid_x - 0.02 * np.cos(angle),
            ay=mid_y - 0.02 * np.sin(angle),
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1.5,
            arrowwidth=3, arrowcolor=color
        )
    
    # Node info
    info = {
        'pv': ('Solar PV', '☀️', pv_range if pv_enabled else "Disabled"),
        'wind': ('Wind', '💨', wind_range if wind_enabled else "Disabled"),
        'hydro': ('Hydro', '💧', hydro_range if hydro_enabled else "Disabled"),
        'bus': ('Grid', '⚡', 'Distribution Hub'),
        'bess': ('BESS', '🔋', bess_range if bess_enabled else "Disabled"),
        'load': ('Load', '🏭', 'Consumer Load')
    }
    
    # Draw nodes
    for node, (x, y) in node_pos.items():
        name, icon, cap = info[node]
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=80,
                color=node_colors[node],
                line=dict(color='white', width=4)
            ),
            text=icon,
            textfont=dict(size=32),
            textposition='middle center',
            hovertemplate=f"<b>{name}</b><br>{cap}<extra></extra>",
            showlegend=False
        ))
        
        fig.add_annotation(
            x=x, y=y - 0.12,
            text=f"<b>{name}</b>",
            showarrow=False,
            font=dict(size=14, color='white')
        )
        
        fig.add_annotation(
            x=x, y=y - 0.16,
            text=f"<i>{cap}</i>",
            showarrow=False,
            font=dict(size=11, color='#00D9FF')
        )
    
    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 1.1]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 1.0]),
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='closest'
    )
    
    return fig

# ============================================================================
# SESSION STATE
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

if 'selected_component' not in st.session_state:
    st.session_state.selected_component = None

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
    st.markdown("### 🔌 System Architecture")
    st.markdown("**Interactive Energy Flow Diagram**")
    
    pv_cfg = st.session_state.pv_config
    wind_cfg = st.session_state.wind_config
    hydro_cfg = st.session_state.hydro_config
    bess_cfg = st.session_state.bess_config
    
    topology_fig = create_topology_diagram(
        pv_cfg['enabled'], wind_cfg['enabled'], hydro_cfg['enabled'], bess_cfg['enabled'],
        f"{pv_cfg['min']:.1f}-{pv_cfg['max']:.1f} MW",
        f"{wind_cfg['min']:.1f}-{wind_cfg['max']:.1f} MW",
        f"{hydro_cfg['min']:.1f}-{hydro_cfg['max']:.1f} MW",
        f"{bess_cfg['min_power']:.1f}-{bess_cfg['max_power']:.1f} MW"
    )
    
    st.plotly_chart(topology_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Component buttons
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
    
    # Configuration panel
    if st.session_state.selected_component == 'pv':
        st.markdown("## ☀️ Solar PV Configuration")
        
        enabled = st.toggle("Enable Solar PV", value=pv_cfg['enabled'])
        
        if enabled:
            st.markdown("### 📊 Capacity Range")
            col1, col2 = st.columns(2)
            
            with col1:
                min_cap = st.slider("Min (MW)", 0.0, 50.0, pv_cfg['min'], 0.5)
            with col2:
                max_cap = st.slider("Max (MW)", 0.0, 50.0, pv_cfg['max'], 0.5)
            
            step = st.slider("Step (MW)", 0.1, 10.0, pv_cfg['step'], 0.1)
            num_opts = int((max_cap - min_cap) / step) + 1 if step > 0 else 1
            
            if num_opts <= 10:
                st.success(f"🟢 {num_opts} configurations")
            elif num_opts <= 50:
                st.warning(f"🟡 {num_opts} configurations")
            else:
                st.error(f"🔴 {num_opts} configurations")
            
            st.markdown("### 💰 Financial")
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=pv_cfg['capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=pv_cfg['opex'])
            with col3:
                lifetime = st.number_input("Lifetime (yrs)", value=pv_cfg['lifetime'])
            
            st.markdown("### 📁 Profile")
            pv_file = st.file_uploader("PV Profile (1 kW)", type=['csv', 'xlsx'])
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("✅ Save", type="primary", use_container_width=True):
                    st.session_state.pv_config = {
                        'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                        'capex': capex, 'opex': opex, 'lifetime': lifetime, 'profile': pv_file
                    }
                    st.success("✅ Saved!")
                    st.session_state.selected_component = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.selected_component = None
                    st.rerun()
        else:
            if st.button("✅ Save", type="primary"):
                st.session_state.pv_config['enabled'] = False
                st.session_state.selected_component = None
                st.rerun()
    
    elif st.session_state.selected_component == 'wind':
        st.markdown("## 💨 Wind Configuration")
        
        enabled = st.toggle("Enable Wind", value=wind_cfg['enabled'])
        
        if enabled:
            col1, col2 = st.columns(2)
            with col1:
                min_cap = st.slider("Min (MW)", 0.0, 50.0, wind_cfg['min'], 0.5)
            with col2:
                max_cap = st.slider("Max (MW)", 0.0, 50.0, wind_cfg['max'], 0.5)
            
            step = st.slider("Step (MW)", 0.1, 10.0, wind_cfg['step'], 0.1)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=wind_cfg['capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=wind_cfg['opex'])
            with col3:
                lifetime = st.number_input("Lifetime (yrs)", value=wind_cfg['lifetime'])
            
            wind_file = st.file_uploader("Wind Profile", type=['csv', 'xlsx'])
            
            if st.button("✅ Save", type="primary"):
                st.session_state.wind_config = {
                    'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                    'capex': capex, 'opex': opex, 'lifetime': lifetime, 'profile': wind_file
                }
                st.session_state.selected_component = None
                st.rerun()
        else:
            if st.button("✅ Save", type="primary"):
                st.session_state.wind_config['enabled'] = False
                st.session_state.selected_component = None
                st.rerun()
    
    elif st.session_state.selected_component == 'hydro':
        st.markdown("## 💧 Hydro Configuration")
        
        enabled = st.toggle("Enable Hydro", value=hydro_cfg['enabled'])
        
        if enabled:
            col1, col2 = st.columns(2)
            with col1:
                min_cap = st.slider("Min (MW)", 0.0, 30.0, hydro_cfg['min'], 0.5)
            with col2:
                max_cap = st.slider("Max (MW)", 0.0, 30.0, hydro_cfg['max'], 0.5)
            
            step = st.slider("Step (MW)", 0.1, 10.0, hydro_cfg['step'], 0.1)
            hours = st.slider("Hours/day", 1, 24, hydro_cfg['hours_per_day'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=hydro_cfg['capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=hydro_cfg['opex'])
            with col3:
                lifetime = st.number_input("Lifetime (yrs)", value=hydro_cfg['lifetime'])
            
            hydro_file = st.file_uploader("Hydro Profile", type=['csv', 'xlsx'])
            
            if st.button("✅ Save", type="primary"):
                st.session_state.hydro_config = {
                    'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                    'hours_per_day': hours, 'capex': capex, 'opex': opex,
                    'lifetime': lifetime, 'profile': hydro_file
                }
                st.session_state.selected_component = None
                st.rerun()
        else:
            if st.button("✅ Save", type="primary"):
                st.session_state.hydro_config['enabled'] = False
                st.session_state.selected_component = None
                st.rerun()
    
    elif st.session_state.selected_component == 'bess':
        st.markdown("## 🔋 BESS Configuration")
        
        enabled = st.toggle("Enable BESS", value=bess_cfg['enabled'])
        
        if enabled:
            col1, col2 = st.columns(2)
            with col1:
                min_pow = st.slider("Min (MW)", 0.0, 100.0, bess_cfg['min_power'], 1.0)
            with col2:
                max_pow = st.slider("Max (MW)", 0.0, 100.0, bess_cfg['max_power'], 1.0)
            
            step_pow = st.slider("Step (MW)", 0.5, 20.0, bess_cfg['step_power'], 0.5)
            duration = st.slider("Duration (hrs)", 0.5, 8.0, bess_cfg['duration'], 0.5)
            
            col1, col2 = st.columns(2)
            with col1:
                power_capex = st.number_input("Power CapEx ($/kW)", value=bess_cfg['power_capex'])
                energy_capex = st.number_input("Energy CapEx ($/kWh)", value=bess_cfg['energy_capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=bess_cfg['opex'])
                lifetime = st.number_input("Lifetime (yrs)", value=bess_cfg['lifetime'])
            
            if st.button("✅ Save", type="primary"):
                st.session_state.bess_config = {
                    'enabled': enabled, 'min_power': min_pow, 'max_power': max_pow,
                    'step_power': step_pow, 'duration': duration,
                    'min_soc': bess_cfg['min_soc'], 'max_soc': bess_cfg['max_soc'],
                    'charge_eff': bess_cfg['charge_eff'], 'discharge_eff': bess_cfg['discharge_eff'],
                    'power_capex': power_capex, 'energy_capex': energy_capex,
                    'opex': opex, 'lifetime': lifetime
                }
                st.session_state.selected_component = None
                st.rerun()
        else:
            if st.button("✅ Save", type="primary"):
                st.session_state.bess_config['enabled'] = False
                st.session_state.selected_component = None
                st.rerun()
    
    else:
        # Summary
        st.markdown("## 📋 Configuration Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if pv_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### ☀️ Solar PV ✅")
                st.write(f"Range: {pv_cfg['min']:.1f}-{pv_cfg['max']:.1f} MW")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### ☀️ Solar PV ❌")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if hydro_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### 💧 Hydro ✅")
                st.write(f"Range: {hydro_cfg['min']:.1f}-{hydro_cfg['max']:.1f} MW")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### 💧 Hydro ❌")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if wind_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### 💨 Wind ✅")
                st.write(f"Range: {wind_cfg['min']:.1f}-{wind_cfg['max']:.1f} MW")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### 💨 Wind ❌")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if bess_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### 🔋 BESS ✅")
                st.write(f"Power: {bess_cfg['min_power']:.1f}-{bess_cfg['max_power']:.1f} MW")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### 🔋 BESS ❌")
                st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("⚙️ Run Optimization")
    st.info("🚧 Optimization engine integration coming next")

with tab3:
    st.header("📊 Results")
    st.info("ℹ️ No results yet")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    discount_rate = st.number_input("Discount Rate (%)", value=8.0)
    inflation_rate = st.number_input("Inflation Rate (%)", value=2.0)
    project_lifetime = st.number_input("Project Lifetime (yrs)", value=25)
    
    st.markdown("---")
    st.markdown("### 🏭 Load")
    
    load_file = st.file_uploader("Load Profile", type=['csv', 'xlsx'])
    target_unmet = st.number_input("Target Unmet (%)", value=0.1)
    
    st.markdown("---")
    st.markdown("### 📊 Search Space")
    
    pv_opts = int((pv_cfg['max'] - pv_cfg['min']) / pv_cfg['step']) + 1 if pv_cfg['enabled'] and pv_cfg['step'] > 0 else 1
    wind_opts = int((wind_cfg['max'] - wind_cfg['min']) / wind_cfg['step']) + 1 if wind_cfg['enabled'] and wind_cfg['step'] > 0 else 1
    hydro_opts = int((hydro_cfg['max'] - hydro_cfg['min']) / hydro_cfg['step']) + 1 if hydro_cfg['enabled'] and hydro_cfg['step'] > 0 else 1
    bess_opts = int((bess_cfg['max_power'] - bess_cfg['min_power']) / bess_cfg['step_power']) + 1 if bess_cfg['enabled'] and bess_cfg['step_power'] > 0 else 1
    
    total = pv_opts * wind_opts * hydro_opts * bess_opts
    
    st.metric("Total Combinations", f"{total:,}")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00D9FF; padding: 20px;">
    <p style="font-size: 18px;"><b>⚡ Energy Modeling Optimizer v4.0</b></p>
    <p style="font-size: 14px;">Developed by SJ | 2026</p>
</div>
""", unsafe_allow_html=True)
