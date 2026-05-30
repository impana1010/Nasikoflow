# Nasikoflow
Real-time telemetry dashboard and routing system built using Python and Streamlit.
🚀 NasikoFlow

A distributed routing and failover simulation platform that demonstrates intelligent request routing, health monitoring, and automatic failover in a multi-agent architecture.

---

📌 Project Overview

NasikoFlow is designed to simulate how modern distributed systems maintain reliability and availability when individual services fail.

The system consists of:

- Multiple Agent Nodes
- Intelligent Router
- Health Checker
- Monitoring Dashboard
- Docker-Based Deployment

When an agent becomes unavailable, the health checker detects the failure and the router automatically redirects traffic to healthy agents.

---

🏗️ Architecture

                 ┌─────────────────┐
                 │    Dashboard    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │      Router     │
                 └────────┬────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │ Agent 1 │      │ Agent 2 │      │ Agent 3 │
   └─────────┘      └─────────┘      └─────────┘
                          ▲
                          │
                 ┌─────────────────┐
                 │ Health Checker  │
                 └─────────────────┘

---

✨ Features

Intelligent Routing

- Round Robin Routing
- Least Connections Routing
- Random Routing
- Adaptive Routing

Health Monitoring

- Continuous Agent Monitoring
- Automatic Failure Detection
- Agent Recovery Detection

Fault Tolerance

- Automatic Failover
- Traffic Redirection
- Service Availability Management

Monitoring Dashboard

- Agent Status Tracking
- Latency Monitoring
- Active Connections Display
- Routing Strategy Visualization

Containerization

- Docker Support
- Docker Compose Orchestration
- Multi-Service Deployment

---

🛠️ Tech Stack

Backend

- Python
- FastAPI
- HTTPX

Monitoring

- Streamlit

Containerization

- Docker
- Docker Compose

---

📂 Project Structure

nasikoflow/
│
├── docker-compose.yml
│
├── router/
│   ├── main.py
│   ├── balancer.py
│   ├── checker.py
│   └── Dockerfile
│
├── dashboard/
│   └── app.py
│
└── README.md

---

⚙️ Installation

Prerequisites

- Python 3.12+
- Docker Desktop
- Docker Compose

---

🚀 Running the Project

Start All Services

docker compose up --build

Stop All Services

docker compose down

---

📊 Launch Dashboard

Navigate to the dashboard directory and run:

streamlit run app.py

Dashboard URL:

http://localhost:8501

---

🔄 Failover Demonstration

1. Start all containers.
2. Open the monitoring dashboard.
3. Stop one of the agent containers.
4. Observe the health checker detecting the failure.
5. Verify that the router excludes the failed agent.
6. Restart the agent.
7. Observe automatic recovery.

---

🎯 Key Learning Outcomes

- Distributed System Design
- Load Balancing Techniques
- Health Monitoring
- Fault Tolerance
- Container Networking
- Docker Orchestration
- Service Integration

---

👥 Team Contributions

Routing Layer

- Request Distribution
- Routing Algorithms
- Traffic Management

Health Monitoring

- Agent Health Checks
- Failover Detection
- Recovery Handling

Dashboard

- Real-Time Monitoring
- Visualization
- Metrics Display

Docker & Integration

- Containerization
- Service Orchestration
- System Integration
- Deployment Testing

---

🔮 Future Enhancements

- Dynamic Agent Registration
- Kubernetes Deployment
- Predictive Routing
- Advanced Analytics Dashboard
- Distributed Logging
- Authentication & Authorization

---

📄 License

This project was developed as part of a hackathon/academic project to demonstrate distributed system concepts, load balancing, and automated failover mechanisms.
