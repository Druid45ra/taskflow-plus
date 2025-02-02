from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from starlette.websockets import WebSocketDisconnect
from app.users import users as user_routes
from app.tasks import tasks as task_routes

app = FastAPI()

@app.websocket("/ws/status")
async def system_status_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Custom logic
    except WebSocketDisconnect:
        pass

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_routes.router)
app.include_router(task_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Taskflow Plus API"}
