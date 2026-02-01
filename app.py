"""
ENERGY MODELING OPTIMIZER BY SJ
===============================
Professional renewable energy optimization tool with BCG-style interface.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Energy Optimizer Pro | by SJ",
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
    
    .topology-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 3px solid #00D9FF;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
    }
    
    .flow-arrow {
        font-size: 40px;
        color: #FFD700;
        margin: 0 20px;
    }
    
    .component-icon {
        font-size: 60px;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Session State
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

# Header
st.markdown('<p class="big-font">⚡ ENERGY MODELING OPTIMIZER</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">BY SJ</p>', unsafe_allow_html=True)
st.markdown("---")

# Main tabs
tab1, tab2, tab3 = st.tabs(["🔌 System Design", "⚙️ Optimize", "📊 Results"])

# TAB 1: SYSTEM DESIGN
with tab1:
    
    # Visual Topology
    st.markdown("### 🔌 System Architecture")
    
    pv_cfg = st.session_state.pv_config
    wind_cfg = st.session_state.wind_config
    hydro_cfg = st.session_state.hydro_config
    bess_cfg = st.session_state.bess_config
    
    # Simple visual topology
    st.markdown('<div class="topology-box">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
    
    with col1:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<p class="component-icon">☀️</p>', unsafe_allow_html=True)
        st.markdown(f"**Solar PV**<br>{'✅ ' + str(pv_cfg['min']) + '-' + str(pv_cfg['max']) + ' MW' if pv_cfg['enabled'] else '❌ Disabled'}", unsafe_allow_html=True)
        st.markdown('<p class="component-icon">💨</p>', unsafe_allow_html=True)
        st.markdown(f"**Wind**<br>{'✅ ' + str(wind_cfg['min']) + '-' + str(wind_cfg['max']) + ' MW' if wind_cfg['enabled'] else '❌ Disabled'}", unsafe_allow_html=True)
        st.markdown('<p class="component-icon">💧</p>', unsafe_allow_html=True)
        st.markdown(f"**Hydro**<br>{'✅ ' + str(hydro_cfg['min']) + '-' + str(hydro_cfg['max']) + ' MW' if hydro_cfg['enabled'] else '❌ Disabled'}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="flow-arrow">→</p>', unsafe_allow_html=True)
        st.markdown('<p class="flow-arrow">→</p>', unsafe_allow_html=True)
        st.markdown('<p class="flow-arrow">→</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="text-align: center; padding-top: 80px;">', unsafe_allow_html=True)
        st.markdown('<p class="component-icon">⚡</p>', unsafe_allow_html=True)
        st.markdown("**Electricity Grid**<br>Distribution Hub", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<p class="flow-arrow" style="padding-top: 80px;">→</p>', unsafe_allow_html=True)
        st.markdown('<p class="flow-arrow">↕</p>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div style="text-align: center; padding-top: 80px;">', unsafe_allow_html=True)
        st.markdown('<p class="component-icon">🏭</p>', unsafe_allow_html=True)
        st.markdown("**Load Demand**<br>Consumer Load", unsafe_allow_html=True)
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<p class="component-icon">🔋</p>', unsafe_allow_html=True)
        st.markdown(f"**BESS**<br>{'✅ ' + str(bess_cfg['min_power']) + '-' + str(bess_cfg['max_power']) + ' MW' if bess_cfg['enabled'] else '❌ Disabled'}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Configuration panels
    if st.session_state.selected_component == 'pv':
        st.markdown("## ☀️ Solar PV Configuration")
        
        enabled = st.toggle("Enable Solar PV", value=pv_cfg['enabled'])
        
        if enabled:
            st.markdown("### 📊 Capacity Range")
            col1, col2 = st.columns(2)
            with col1:
                min_cap = st.slider("Minimum (MW)", 0.0, 50.0, pv_cfg['min'], 0.5)
                st.metric("Min Capacity", f"{min_cap:.1f} MW")
            with col2:
                max_cap = st.slider("Maximum (MW)", 0.0, 50.0, pv_cfg['max'], 0.5)
                st.metric("Max Capacity", f"{max_cap:.1f} MW")
            
            step = st.slider("Step Size (MW)", 0.1, 10.0, pv_cfg['step'], 0.1)
            
            num_opts = int((max_cap - min_cap) / step) + 1 if step > 0 else 1
            if num_opts <= 10:
                st.success(f"🟢 {num_opts} configurations - Small search space")
            elif num_opts <= 50:
                st.warning(f"🟡 {num_opts} configurations - Medium search space")
            else:
                st.error(f"🔴 {num_opts} configurations - Large search space")
            
            st.markdown("### 💰 Financial Parameters")
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=pv_cfg['capex'], step=50)
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=pv_cfg['opex'], step=1)
            with col3:
                lifetime = st.number_input("Lifetime (years)", value=pv_cfg['lifetime'], step=1)
            
            st.markdown("### 📁 Generation Profile")
            pv_file = st.file_uploader("Upload PV Profile (1 kW normalized)", type=['csv', 'xlsx'], key="pv_file")
            if pv_file:
                st.success(f"✅ Loaded: {pv_file.name}")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("✅ Save Solar PV Configuration", type="primary", use_container_width=True):
                    st.session_state.pv_config = {
                        'enabled': enabled, 'min': min_cap, 'max': max_cap, 'step': step,
                        'capex': capex, 'opex': opex, 'lifetime': lifetime, 'profile': pv_file
                    }
                    st.success("✅ Solar PV configuration saved!")
                    st.session_state.selected_component = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.selected_component = None
                    st.rerun()
        else:
            if st.button("✅ Save Configuration", type="primary"):
                st.session_state.pv_config['enabled'] = False
                st.session_state.selected_component = None
                st.rerun()
    
    elif st.session_state.selected_component == 'wind':
        st.markdown("## 💨 Wind Configuration")
        enabled = st.toggle("Enable Wind", value=wind_cfg['enabled'])
        
        if enabled:
            col1, col2 = st.columns(2)
            with col1:
                min_cap = st.slider("Minimum (MW)", 0.0, 50.0, wind_cfg['min'], 0.5)
            with col2:
                max_cap = st.slider("Maximum (MW)", 0.0, 50.0, wind_cfg['max'], 0.5)
            
            step = st.slider("Step (MW)", 0.1, 10.0, wind_cfg['step'], 0.1)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=wind_cfg['capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=wind_cfg['opex'])
            with col3:
                lifetime = st.number_input("Lifetime (yrs)", value=wind_cfg['lifetime'])
            
            wind_file = st.file_uploader("Wind Profile", type=['csv', 'xlsx'])
            
            if st.button("✅ Save Wind Configuration", type="primary"):
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
            hours = st.slider("Operating Hours/Day", 1, 24, hydro_cfg['hours_per_day'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                capex = st.number_input("CapEx ($/kW)", value=hydro_cfg['capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=hydro_cfg['opex'])
            with col3:
                lifetime = st.number_input("Lifetime (yrs)", value=hydro_cfg['lifetime'])
            
            hydro_file = st.file_uploader("Hydro Profile (Optional)", type=['csv', 'xlsx'])
            
            if st.button("✅ Save Hydro Configuration", type="primary"):
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
        st.markdown("## 🔋 Battery Storage Configuration")
        enabled = st.toggle("Enable BESS", value=bess_cfg['enabled'])
        
        if enabled:
            col1, col2 = st.columns(2)
            with col1:
                min_pow = st.slider("Min Power (MW)", 0.0, 100.0, bess_cfg['min_power'], 1.0)
            with col2:
                max_pow = st.slider("Max Power (MW)", 0.0, 100.0, bess_cfg['max_power'], 1.0)
            
            step_pow = st.slider("Step (MW)", 0.5, 20.0, bess_cfg['step_power'], 0.5)
            duration = st.slider("Duration (hours)", 0.5, 8.0, bess_cfg['duration'], 0.5)
            
            max_energy = max_pow * duration
            st.info(f"💡 Max Energy Capacity: {max_energy:.1f} MWh")
            
            col1, col2 = st.columns(2)
            with col1:
                power_capex = st.number_input("Power CapEx ($/kW)", value=bess_cfg['power_capex'])
                energy_capex = st.number_input("Energy CapEx ($/kWh)", value=bess_cfg['energy_capex'])
            with col2:
                opex = st.number_input("OpEx ($/kW/yr)", value=bess_cfg['opex'])
                lifetime = st.number_input("Lifetime (yrs)", value=bess_cfg['lifetime'])
            
            if st.button("✅ Save BESS Configuration", type="primary"):
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
                st.write(f"**Range:** {pv_cfg['min']:.1f} - {pv_cfg['max']:.1f} MW")
                st.write(f"**Step:** {pv_cfg['step']:.1f} MW")
                st.write(f"**CapEx:** ${pv_cfg['capex']}/kW")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### ☀️ Solar PV ❌ DISABLED")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if hydro_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### 💧 Hydro ✅")
                st.write(f"**Range:** {hydro_cfg['min']:.1f} - {hydro_cfg['max']:.1f} MW")
                st.write(f"**Hours/day:** {hydro_cfg['hours_per_day']}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### 💧 Hydro ❌ DISABLED")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if wind_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### 💨 Wind ✅")
                st.write(f"**Range:** {wind_cfg['min']:.1f} - {wind_cfg['max']:.1f} MW")
                st.write(f"**Step:** {wind_cfg['step']:.1f} MW")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### 💨 Wind ❌ DISABLED")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if bess_cfg['enabled']:
                st.markdown('<div class="component-card">', unsafe_allow_html=True)
                st.markdown("### 🔋 BESS ✅")
                st.write(f"**Power:** {bess_cfg['min_power']:.1f} - {bess_cfg['max_power']:.1f} MW")
                st.write(f"**Duration:** {bess_cfg['duration']:.1f} hours")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="component-card-disabled">', unsafe_allow_html=True)
                st.markdown("### 🔋 BESS ❌ DISABLED")
                st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("⚙️ Run Optimization")
    st.info("🚧 Optimization engine integration coming next")

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
    st.markdown("#### 🏭 Load Profile & Constraints")
    
    load_file = st.file_uploader("📁 Load Profile (kW)", type=['csv', 'xlsx'])
    if load_file:
        st.success(f"✅ Loaded: {load_file.name}")
    
    target_unmet = st.number_input("Target Unmet Load (%)", value=0.1, step=0.1)
    
    st.markdown("---")
    st.markdown("### 📊 Search Space")
    
    pv_opts = int((pv_cfg['max'] - pv_cfg['min']) / pv_cfg['step']) + 1 if pv_cfg['enabled'] and pv_cfg['step'] > 0 else 1
    wind_opts = int((wind_cfg['max'] - wind_cfg['min']) / wind_cfg['step']) + 1 if wind_cfg['enabled'] and wind_cfg['step'] > 0 else 1
    hydro_opts = int((hydro_cfg['max'] - hydro_cfg['min']) / hydro_cfg['step']) + 1 if hydro_cfg['enabled'] and hydro_cfg['step'] > 0 else 1
    bess_opts = int((bess_cfg['max_power'] - bess_cfg['min_power']) / bess_cfg['step_power']) + 1 if bess_cfg['enabled'] and bess_cfg['step_power'] > 0 else 1
    
    total = pv_opts * wind_opts * hydro_opts * bess_opts
    
    st.metric("Total Combinations", f"{total:,}")
    st.metric("Est. Runtime", f"{max(1, total * 0.05 / 60):.1f} min")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00D9FF; padding: 20px;">
    <p style="font-size: 18px;"><b>⚡ Energy Modeling Optimizer v4.0 Professional</b></p>
    <p style="font-size: 14px;">Developed by SJ | 2026</p>
</div>
""", unsafe_allow_html=True)
