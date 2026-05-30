import streamlit as st
import httpx
import pandas as pd
import numpy as np
import time
import random

# Set premium wide-screen tech configuration
st.set_page_config(
    page_title="NasikoFlow // Control Plane",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Ultra-Tech Cyberpunk Dark Theme CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #0d1527, #030712);
        font-family: 'JetBrains Mono', monospace !important;
    }
    div[data-testid="stSidebar"] {
        background-color: #090d16;
        border-right: 2px solid #1e293b;
    }
    h1 {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        color: #00f2fe !important;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    }
    h2, h3, h4, label, span {
        font-family: 'JetBrains Mono', monospace !important;
        color: #f1f5f9 !important;
    }
    .stMetric {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8)) !important;
        border: 1px solid #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.15) !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

# Sidebar Control Center
with st.sidebar:
    st.markdown("<h2 style='color: #fe0979; text-shadow: 0 0 15px rgba(254,9,121,0.4);'>🤖 NASIKO // CORE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("SELECT MATRIX VIEW", ["⚡ TELEMETRY STREAM", "⚙️ STRATEGY GOVERNOR"])
    st.markdown("---")
    auto_refresh = st.checkbox("REALTIME LIVE SYNC", value=True)
    
    # NEW: Presentation Chaos Controls
    st.markdown("---")
    st.markdown("<p style='color: #00f2fe; font-weight: bold;'>🎛️ DEMO VARIATION ENGINE</p>", unsafe_allow_html=True)
    enable_manual_control = st.checkbox("Enable Manual Sliders")
    add_random_jitter = st.checkbox("Inject Auto Network Jitter")

# Data fetcher targeting backend
def fetch_system_status():
    try:
        response = httpx.get(f"{API_BASE}/status", timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

data = fetch_system_status()
agents = data.get("agents", []) if data else []
current_strategy = data.get("strategy", "adaptive") if data else "offline"

# Apply variation adjustments based on sidebar inputs
if data and len(agents) > 0:
    for agent in agents:
        a_id = agent.get("id", "")
        
        # If auto-jitter is checked, add subtle random ripples to the latency
        if add_random_jitter:
            base_lat = agent.get("latency", 0.050)
            if base_lat == 0: base_lat = 0.050
            agent["latency"] = max(0.010, base_lat + random.uniform(-0.015, 0.015))
            agent["connections"] = random.randint(1, 5) if is_healthy else 0
            
        # If manual sliders are checked, give the presenter full override control
        if enable_manual_control:
            with st.sidebar:
                current_ms = int(agent.get("latency", 0.050) * 1000)
                override_ms = st.slider(f"{a_id.upper()} Latency (ms)", 10, 800, current_ms if current_ms > 0 else 50)
                agent["latency"] = override_ms / 1000.0
                
                if agent.get("healthy"):
                    override_conn = st.slider(f"{a_id.upper()} Active Connections", 0, 15, int(agent.get("connections", 0)))
                    agent["connections"] = override_conn

if page == "⚡ TELEMETRY STREAM":
    st.title("SYS // NODE_TELEMETRY")
    st.markdown(f"CURRENT TUNING POLICY CONFIGURATION: <span style='color:#fe0979; font-weight:bold;'>[{current_strategy.upper()}]</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    total_count = len(agents)
    healthy_count = sum(1 for a in agents if a.get("healthy"))
    total_loads = sum(a.get("connections", 0) for a in agents)
    
    with col1:
        st.metric(label="MANAGED CLUSTER NODES", value=f"{total_count:02d}")
    with col2:
        st.metric(label="OPERATIONAL REPLICAS", value=f"{healthy_count:02d} / {total_count:02d}")
    with col3:
        st.metric(label="CONCURRENT REQUEST INGESTS", value=f"{total_loads} SESS")
    with col4:
        gateway_text = "SYS_READY // 🟢" if data else "CRITICAL_OFFLINE // 🔴"
        st.metric(label="GATEWAY CORE STATE", value=gateway_text)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if not data:
        st.error("🚨 CRITICAL: UNABLE TO ESTABLISH TCP PORT CONNECTION TO ROUTER GATEWAY CORE ON LOCALHOST:8000.")
    else:
        # 2. Glowing Agent Cards
        st.markdown("<h3 style='color: #00f2fe; margin-bottom: 20px;'>🛰️ CLUSTER_NODE_MAP</h3>", unsafe_allow_html=True)
        cols = st.columns(max(total_count, 1))
        
        for idx, agent in enumerate(agents):
            with cols[idx]:
                is_healthy = agent.get("healthy", False)
                neon_accent = "#00ff87" if is_healthy else "#fe0979"
                glow_intensity = "rgba(0, 255, 135, 0.15)" if is_healthy else "rgba(254, 9, 121, 0.15)"
                status_label = "NODE_ACTIVE" if is_healthy else "NODE_QUARANTINED"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0f172a, #090d16); 
                            border: 2px solid {neon_accent}; 
                            box-shadow: 0 0 20px {glow_intensity}; 
                            border-radius: 16px; padding: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span style="font-size: 20px; font-weight: bold; color: #f8fafc; letter-spacing: 1px;">{agent.get('id', 'N/A').upper()}</span>
                        <span style="background-color: {neon_accent}20; color: {neon_accent}; padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: bold; border: 1px solid {neon_accent}50;">
                            {status_label}
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; line-height: 1.8;">
                        <p style="margin: 4px 0;"><span style="color: {neon_accent};">▶</span> <b>URL:</b> {agent.get('url')}</p>
                        <p style="margin: 4px 0;"><span style="color: {neon_accent};">▶</span> <b>ACTIVE_LOADS:</b> {agent.get('connections', 0)} sessions</p>
                        <p style="margin: 4px 0;"><span style="color: {neon_accent};">▶</span> <b>AVERAGE_LATENCY:</b> <span style="font-family: monospace; color: #f1f5f9; font-weight: bold;">{agent.get('latency', 0.0):.3f}s</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 3. Dynamic Latency Bar Graph
        st.markdown("<h3 style='color: #00f2fe; margin-bottom: 20px;'>📊 LIVE_NODE_LATENCY_MATRIX (ms)</h3>", unsafe_allow_html=True)
        if total_count > 0:
            chart_df = pd.DataFrame({
                "NODE ID": [a.get("id").upper() for a in agents],
                "RESPONSE TIME (ms)": [a.get("latency", 0.0) * 1000 for a in agents]
            })
            st.bar_chart(chart_df.set_index("NODE ID"), color="#00f2fe")

elif page == "⚙️ STRATEGY GOVERNOR":
    st.title("SYS // ROUTING_POLICY_GOVERNOR")
    st.write("Intercept and hot-swap active backend operational graph logic configurations dynamically.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_strategy = st.selectbox(
        "CHOOSE ACTIVE TRAFFIC INTERCEPTION ALGORITHM:",
        ["adaptive", "least_connections", "round_robin", "random"],
        index=["adaptive", "least_connections", "round_robin", "random"].index(current_strategy) if current_strategy in ["adaptive", "least_connections", "round_robin", "random"] else 0
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EXECUTE SYSTEM POLICY HOT-SWAP"):
        try:
            req = httpx.post(f"{API_BASE}/set-strategy/{selected_strategy}")
            if req.status_code == 200:
                st.success(f"SUCCESS // TRAFFIC CONFIGURED TO INTERCEPT MODE: {selected_strategy.upper()}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("FAILURE // CORE ROUTER REJECTED ALGORITHMIC ADJUSTMENT TRANSITION STATE.")
        except Exception as e:
            st.error(f"FATAL ERROR // EXCEPTION INTERACTING WITH LOGIC CORE: {e}")

if auto_refresh:
    time.sleep(1)
    st.rerun()