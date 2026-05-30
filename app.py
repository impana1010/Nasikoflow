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

# Elegant Cyberpunk Dark Theme CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');

    /* Global App Styling */
    .stApp {
        background: linear-gradient(160deg, #0b0f19, #111827);
        font-family: 'JetBrains Mono', monospace !important;
        color: #e5e7eb;
    }

    /* Sidebar */
    div[data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid #1f2937;
        padding: 1rem;
    }

    /* Headings */
    h1 {
        font-weight: 700 !important;
        color: #38bdf8 !important;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }
    h2, h3, h4, label, span {
        font-weight: 400 !important;
        color: #f3f4f6 !important;
    }

    /* Metrics Cards */
    .stMetric {
        background: linear-gradient(145deg, #1e293b, #111827);
        border: 1px solid #38bdf8;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
        border-radius: 12px !important;
        padding: 16px !important;
        color: #f9fafb !important;
    }

    /* Buttons */
    button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb, #1e40af);
        color: #f9fafb !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 0 8px rgba(37, 99, 235, 0.4);
    }
    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #1e40af, #1e3a8a);
        box-shadow: 0 0 12px rgba(37, 99, 235, 0.6);
    }

    /* Agent Cards */
    .agent-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #374151;
        box-shadow: 0 0 12px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .agent-card h4 {
        color: #38bdf8;
        margin-bottom: 10px;
    }
    .agent-card p {
        color: #d1d5db;
        font-size: 13px;
        margin: 4px 0;
    }

    /* Charts */
    .stPlotlyChart, .stBarChart {
        background: #0f172a;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 0 12px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

# Sidebar Control Center
with st.sidebar:
    st.markdown("<h2 style='color: #38bdf8; text-shadow: 0 0 12px rgba(56,189,248,0.4);'>🤖 NASIKO // CORE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("SELECT MATRIX VIEW", ["⚡ TELEMETRY STREAM", "⚙️ STRATEGY GOVERNOR"])
    st.markdown("---")
    auto_refresh = st.checkbox("REALTIME LIVE SYNC", value=True)
    
    # Presentation Chaos Controls
    st.markdown("---")
    st.markdown("<p style='color: #38bdf8; font-weight: bold;'>🎛️ DEMO VARIATION ENGINE</p>", unsafe_allow_html=True)
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

# Admin Override Controls
st.markdown("---")
st.markdown("<p style='color: #38bdf8; font-weight: bold;'>🛡️ ADMIN CONTROLS</p>", unsafe_allow_html=True)
        
if st.button("🔄 REVIVE QUARANTINED NODES"):
    try:
        httpx.post(f"{API_BASE}/revive", timeout=2)
        st.success("Cluster memory reset! All nodes active.")
    except Exception:
        st.error("Failed to contact router.")

# Apply variation adjustments based on sidebar inputs
if data and len(agents) > 0:
    for agent in agents:
        a_id = agent.get("id", "")
        
        if add_random_jitter:
            base_lat = agent.get("latency", 0.050)
            if base_lat == 0: base_lat = 0.050
            agent["latency"] = max(0.010, base_lat + random.uniform(-0.015, 0.015))
            agent["connections"] = random.randint(1, 5) if agent.get("healthy") else 0
            
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
    st.markdown(f"CURRENT TUNING POLICY CONFIGURATION: <span style='color:#38bdf8; font-weight:bold;'>[{current_strategy.upper()}]</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Row
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
        st.markdown("<h3 style='color: #38bdf8; margin-bottom: 20px;'>🛰️ CLUSTER_NODE_MAP</h3>", unsafe_allow_html=True)
        cols = st.columns(max(total_count, 1))
        
        for idx, agent in enumerate(agents):
            with cols[idx]:
                is_healthy = agent.get("healthy", False)
                neon_accent = "#00ff87" if is_healthy else "#fe0979"
                glow_intensity = "rgba(0, 255, 135, 0.15)" if is_healthy else "rgba(254, 9, 121, 0.15)"
                status_label = "NODE_ACTIVE" if is_healthy else "NODE_QUARANTINED"
                
                st.markdown(f"""
                <div class="agent-card" style="border: 2px solid {neon_accent}; box-shadow: 0 0 20px {glow_intensity};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span style="font-size: 18px; font-weight: bold; color: #f8fafc; letter-spacing: 1px;">
                            {agent.get('id', 'N/A').upper()}
                        </span>
                        <span style="background-color: {neon_accent}20; color: {neon_accent};
                                    padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: bold;
                                    border: 1px solid {neon_accent}50;">
                            {status_label}
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; line-height: 1.8;">
                        <p style="margin: 4px 0;"><span style="color: {neon_accent};">▶</span> <b>URL:</b> {agent.get('url')}</p>
                        <p style="margin: 4px 0;"><span style="color: {neon_accent};">▶</span> <b>ACTIVE_LOADS:</b> {agent.get('connections', 0)} sessions</p>
                        <p style="margin: 4px 0;"><span style="color: {neon_accent};">▶</span> <b>AVERAGE_LATENCY:</b>
                            <span style="font-family: monospace; color: #f1f5f9; font-weight: bold;">
                                {agent.get('latency', 0.0):.3f}s
                            </span>
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Dynamic Latency Bar Graph
        st.markdown("<h3 style='color: #38bdf8; margin-bottom: 20px;'>📊 LIVE_NODE_LATENCY_MATRIX (ms)</h3>", unsafe_allow_html=True)
        if total_count > 0:
            chart_df = pd.DataFrame({
                "NODE ID": [a.get("id").upper() for a in agents],
                "RESPONSE TIME (ms)": [a.get("latency", 0.0) * 1000 for a in agents]
            })
            st.bar_chart(chart_df.set_index("NODE ID"), color="#38bdf8")

elif page == "⚙️ STRATEGY GOVERNOR":
    st.title("SYS // ROUTING_POLICY_GOVERNOR")
    st.write("Intercept and hot-swap active backend operational graph logic configurations dynamically.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_strategy = st.selectbox(
        "CHOOSE ACTIVE TRAFFIC INTERCEPTION ALGORITHM:",
        ["adaptive", "least_connections", "round_robin", "random"],
        index=["adaptive", "least_connections", "round_robin", "random"].index(current_strategy)
        if current_strategy in ["adaptive", "least_connections", "round_robin", "random"] else 0
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

# Auto-refresh loop
if auto_refresh:
    time.sleep(1)
    st.rerun()
