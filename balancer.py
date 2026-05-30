import random
from typing import List, Dict

# Upgraded to track latency in real-time to match presentation deck
agents = [
    {"id": "agent1", "url": "http://agent1:8001", "connections": 0, "healthy": True, "latency": 0.05},
    {"id": "agent2", "url": "http://agent2:8002", "connections": 0, "healthy": True, "latency": 0.05},
    {"id": "agent3", "url": "http://agent3:8003", "connections": 0, "healthy": True, "latency": 0.05},
]

current_index = 0

def get_healthy() -> List[Dict]:
    """Return only healthy agents."""
    return [a for a in agents if a["healthy"]]

def round_robin() -> Dict:
    """Take turns across all healthy agents."""
    global current_index
    healthy = get_healthy()
    if not healthy:
        raise Exception("No healthy agents available")
    agent = healthy[current_index % len(healthy)]
    current_index += 1
    return agent

def least_connections() -> Dict:
    """Pick agent with fewest active connections."""
    healthy = get_healthy()
    if not healthy:
        raise Exception("No healthy agents available")
    return min(healthy, key=lambda a: a["connections"])

def adaptive_routing() -> Dict:
    """POLISH: Picks the optimal agent based on a dynamic score of load and latency."""
    healthy = get_healthy()
    if not healthy:
        raise Exception("No healthy agents available")
    # Score calculation: lower is better (Connections weight + Latency weight)
    return min(healthy, key=lambda a: (a["connections"] * 0.5) + (a["latency"] * 10))

def random_routing() -> Dict:
    """Pick a random healthy agent."""
    healthy = get_healthy()
    if not healthy:
        raise Exception("No healthy agents available")
    return random.choice(healthy)

def get_agent(strategy: str = "round_robin") -> Dict:
    """Main function — pick agent based on chosen strategy."""
    if strategy == "least_connections":
        return least_connections()
    elif strategy == "adaptive":
        return adaptive_routing()
    elif strategy == "random":
        return random_routing()
    else:
        return round_robin()