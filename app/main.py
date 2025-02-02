from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users import routes as user_routes
from app.tasks import routes as task_routes
from app.core.database import Base, engine
from starlette.websockets import WebSocketDisconnect

app = FastAPI()  # Ensure app is defined

@app.websocket("/ws/status")
async def system_status_websocket(websocket: WebSocket):
    # Exemplu: Endpoint pentru admini cu verificare suplimentară
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Logica custom
    except WebSocketDisconnect:
        pass
    
# Creează toate tabelele în baza de date
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include rutele
app.include_router(user_routes.router)
app.include_router(task_routes.router)

@app.get("/")
def root():
    return {"message": "TaskFlow+ API Running 🚀"}
