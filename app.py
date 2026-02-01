"""
ENERGY MODELING OPTIMIZER BY SJ
===============================
Renewable energy optimization tool.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Energy Optimizer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    
    .big-font {
        font-size: 42px !important;
        font-weight: bold;
        color: #00D9FF;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-size: 18px;
        color: #00D9FF;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }
    
    div[data-testid="metric-container"] {
        background-color: #1E1E1E;
        border: 1px solid #00D9FF;
        padding: 15px;
        border-radius: 10px;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-font">⚡ Energy Modeling Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">by SJ</p>', unsafe_allow_html=True)
st.markdown("---")

# Session State
if 'pv_config' not in st.session_state:
    st.session_state.pv_config = {
        'enabled': True, 'min': 1.0, 'max': 5.0, 'step': 1.0,
        'capex': 1000, 'opex': 10, 'lifetime': 25
    }

if 'wind_config' not in st.session_state:
    st.session_state.wind_config = {
        'enabled': True, 'min': 0.0, 'max': 3.0, 'step': 1.0,
        'capex': 1200, 'opex': 15, 'lifetime': 20
    }

if 'hydro_config' not in st.session_state:
    st.session_state.hydro_config = {
        'enabled': True, 'min': 0.0, 'max': 2.0, 'step': 1.0,
        'hours_per_day': 8, 'capex': 2000, 'opex': 20, 'lifetime': 50
    }

if 'bess_config' not in st.session_state:
    st.session_state.bess_config = {
        'enabled': True, 'min_power': 5.0, 'max_power': 20.0, 'step_power': 5.0,
        'duration': 4.0, 'min_soc': 20, 'max_soc': 100,
        'charge_eff': 95, 'discharge_eff': 95,
        'power_capex': 300, 'energy_capex': 200, 'opex': 2, 'lifetime': 15
    }

# Main tabs
tab1, tab2, tab3 = st.tabs(["🏠 System Design", "⚙️ Optimize", "📊 Results"])

with tab1:
    st.header("🔌 System Architecture")
    
    # Simple topology visualization
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ☀️ Solar PV")
        if st.session_state.pv_config['enabled']:
            st.success("✅ Enabled")
            st.metric("Range", f"{st.session_state.pv_config['min']:.1f} - {st.session_state.pv_config['max']:.1f} MW")
        else:
            st.error("❌ Disabled")
        
        if st.button("Configure PV", key="config_pv"):
            st.session_state.selected_component = 'pv'
    
    with col2:
        st.markdown("### 💨 Wind")
        if st.session_state.wind_config['enabled']:
            st.success("✅ Enabled")
            st.metric("Range", f"{st.session_state.wind_config['min']:.1f} - {st.session_state.wind_config['max']:.1f} MW")
        else:
            st.error("❌ Disabled")
        
        if st.button("Configure Wind", key="config_wind"):
            st.session_state.selected_component = 'wind'
    
    with col3:
        st.markdown("### 💧 Hydro")
        if st.session_state.hydro_config['enabled']:
            st.success("✅ Enabled")
            st.metric("Range", f"{st.session_state.hydro_config['min']:.1f} - {st.session_state.hydro_config['max']:.1f} MW")
        else:
            st.error("❌ Disabled")
        
        if st.button("Configure Hydro", key="config_hydro"):
            st.session_state.selected_component = 'hydro'
    
    with col4:
        st.markdown("### 🔋 BESS")
        if st.session_state.bess_config['enabled']:
            st.success("✅ Enabled")
            st.metric("Range", f"{st.session_state.bess_config['min_power']:.1f} - {st.session_state.bess_config['max_power']:.1f} MW")
        else:
            st.error("❌ Disabled")
        
        if st.button("Configure BESS", key="config_bess"):
            st.session_state.selected_component = 'bess'
    
    st.markdown("---")
    
    # Component configuration
    if 'selected_component' in st.session_state and st.session_state.selected_component == 'pv':
        st.markdown("## ☀️ Solar PV Configuration")
        
        enabled = st.toggle("Enable Solar PV", value=st.session_state.pv_config['enabled'])
        
        if enabled:
            col1, col2 = st.columns(2)
            with col1:
                min_cap = st.slider("Minimum Capacity (MW)", 0.0, 50.0, st.session_state.pv_config['min'], 0.5)
                max_cap = st.slider("Maximum Capacity (MW)", 0.0, 50.0, st.session_state.pv_config['max'], 0.5)
            with col2:
                step = st.slider("Step Size (MW)", 0.1, 10.0, st.session_state.pv_config['step'], 0.1)
                num_opts = int((max_cap - min_cap) / step) + 1 if step > 0 else 1
                st.metric("Configurations", num_opts)
            
            st.markdown("### 💰 Financial Parameters")
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=st.session_state.pv_config['capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=st.session_state.pv_config['opex'])
            with col3:
                lifetime = st.number_input("Lifetime (years)", value=st.session_state.pv_config['lifetime'])
            
            if st.button("✅ Save Configuration", type="primary"):
                st.session_state.pv_config = {
                    'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                    'capex': capex, 'opex': opex, 'lifetime': lifetime
                }
                st.success("✅ Configuration saved!")
                del st.session_state.selected_component
                st.rerun()
        else:
            if st.button("✅ Save Configuration", type="primary"):
                st.session_state.pv_config['enabled'] = False
                st.success("✅ Solar PV disabled!")
                del st.session_state.selected_component
                st.rerun()

with tab2:
    st.header("⚙️ Run Optimization")
    st.info("🚧 Optimization engine integration coming soon")
    
    st.markdown("### 📁 Upload Profiles")
    col1, col2 = st.columns(2)
    with col1:
        load_file = st.file_uploader("Load Profile", type=['csv', 'xlsx'])
        pv_file = st.file_uploader("PV Profile", type=['csv', 'xlsx'])
    with col2:
        wind_file = st.file_uploader("Wind Profile", type=['csv', 'xlsx'])
        hydro_file = st.file_uploader("Hydro Profile", type=['csv', 'xlsx'])

with tab3:
    st.header("📊 Results")
    st.info("ℹ️ No results yet. Run optimization first.")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Global Settings")
    
    st.markdown("#### 💰 Financial Parameters")
    discount_rate = st.number_input("Discount Rate (%)", value=8.0, step=0.5)
    inflation_rate = st.number_input("Inflation Rate (%)", value=2.0, step=0.5)
    project_lifetime = st.number_input("Project Lifetime (years)", value=25, step=1)
    
    st.markdown("---")
    
    # Calculate search space
    pv_opts = int((st.session_state.pv_config['max'] - st.session_state.pv_config['min']) / 
                  st.session_state.pv_config['step']) + 1 if st.session_state.pv_config['enabled'] else 1
    wind_opts = int((st.session_state.wind_config['max'] - st.session_state.wind_config['min']) / 
                    st.session_state.wind_config['step']) + 1 if st.session_state.wind_config['enabled'] else 1
    hydro_opts = int((st.session_state.hydro_config['max'] - st.session_state.hydro_config['min']) / 
                     st.session_state.hydro_config['step']) + 1 if st.session_state.hydro_config['enabled'] else 1
    bess_opts = int((st.session_state.bess_config['max_power'] - st.session_state.bess_config['min_power']) / 
                    st.session_state.bess_config['step_power']) + 1 if st.session_state.bess_config['enabled'] else 1
    
    total_combinations = pv_opts * wind_opts * hydro_opts * bess_opts
    
    st.markdown("### 📊 Search Space")
    st.metric("Total Combinations", f"{total_combinations:,}")
    st.metric("Est. Runtime", f"{max(1, total_combinations * 0.05 / 60):.1f} min")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><b>Energy Modeling Optimizer v4.0 Professional</b></p>
    <p>Developed by SJ | 2026</p>
</div>
""", unsafe_allow_html=True)
