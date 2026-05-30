import httpx
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from balancer import get_agent, agents

app = FastAPI(title="NasikoFlow Router")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

strategy = "round_robin"

@app.get("/status")
def get_status():
    return {"agents": agents, "strategy": strategy}

@app.post("/set-strategy/{name}")
def set_strategy(name: str):
    global strategy
    strategy = name
    return {"strategy": strategy}

@app.api_route("/route/{path:path}", methods=["GET", "POST"])
async def route_request(path: str, request: Request):
    try:
        agent = get_agent(strategy)
    except Exception as e:
        return {"error": "CRITICAL_FAILURE", "message": "No healthy agents available in cluster!"}
        
    agent["connections"] += 1
    start_time = time.time()
    
    try:
        # Super safe routing logic that won't crash on browser GET requests
        async with httpx.AsyncClient() as client:
            if request.method == "GET":
                response = await client.get(f"{agent['url']}/{path}", timeout=2.0)
            else:
                body = await request.body()
                response = await client.post(f"{agent['url']}/{path}", content=body, timeout=2.0)
        
        duration = time.time() - start_time
        agent["latency"] = round((agent["latency"] * 0.7) + (duration * 0.3), 4)
        return {"status": "SUCCESS", "node_used": agent["id"]}
        
    except Exception as e:
        # THIS IS THE REAL FAILOVER TRIGGER
        agent["latency"] = 5.0
        agent["healthy"] = False
        return {"error": "NODE_QUARANTINED", "message": f"{agent['id']} failed and was removed from rotation."}
    finally:
        agent["connections"] -= 1