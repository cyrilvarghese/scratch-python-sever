from fastapi import APIRouter
from modules.websocket_connections  import active_websockets
import json
ws_router = APIRouter()
 

@ws_router.get("/")
async def answer():
    # Your logic here...
    print("sending data .........")
    # Example JSON object to send
    json_obj = {
        "meta": {
            "layoutType": "branding"
        },
        "title": "TEstasddddddddddddddddddddddddddddddddddddddddddddd",
        "subtitle": "Our commitment to fostering a culture of inventive thinking positions us as a dynamic force in the ever-evolving business landscape."
    }

    json_str = json.dumps(json_obj)
    
    # Send the JSON string to all active WebSocket connections
    for websocket in active_websockets:
        await websocket.send_text(json_str)
        print("data sent .........")
    
    return {"status": "WebSocket message sent"}