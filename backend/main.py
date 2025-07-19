from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from simulation import Simulation
import asyncio
import uvicorn

app = FastAPI()
simulation = Simulation()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            simulation.step()
            await websocket.send_json(simulation.get_state())
            await asyncio.sleep(0.016)  # fps thingy
    except Exception as e:
        print("WebSocket closed:", e)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)