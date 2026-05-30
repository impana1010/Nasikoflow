import httpx
import asyncio
import logging
from balancer import agents

# Configure logging format
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("HealthChecker")

CHECK_INTERVAL = 5  # seconds between checks
TIMEOUT = 2         # seconds before marking agent dead

async def ping_agent(agent: dict) -> bool:
    """Ping a single agent. Returns True if alive."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                agent["url"] + "/",
                timeout=TIMEOUT
            )
            return response.status_code == 200
    except Exception:
        return False

async def check_all_agents():
    """Check all agents once and update their status."""
    for agent in agents:
        was_healthy = agent["healthy"]
        is_healthy = await ping_agent(agent)
        agent["healthy"] = is_healthy
        
        # Log state changes
        if was_healthy and not is_healthy:
            log.warning(f"Agent {agent['id']} went DOWN ❌")
        elif not was_healthy and is_healthy:
            log.info(f"Agent {agent['id']} came back UP  ")

async def health_check_loop():
    """Run forever - check agents every 5 seconds."""
    log.info("Health checker started")
    while True:
        await check_all_agents()
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(health_check_loop())