from fastapi import FastAPI, WebSocket,Request
from query_router import query_router
from answer_router import answer_router
from upload_router import upload_router
from read_data_router import read_data_router
from urls_router import load_url_router
from ws_router import ws_router
from files_router import files_router
from fastapi.staticfiles import StaticFiles
import chroma_setup
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
import secrets
from modules.websocket_connections import active_websockets
import json

@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    nonce = secrets.token_urlsafe(16)  # Generate a secure nonce
    response = await call_next(request)
    # Add CSP header with nonce
    csp_policy = f"script-src 'nonce-{nonce}';"
    response.headers['Content-Security-Policy'] = csp_policy
    # You might need to adjust response handling for your use case
    return response
 
 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    try:
        while True:
            # Receive text (JSON) message from the client
            data = await websocket.receive_text()
            
            # Deserialize the JSON data from the client
            json_data = json.loads(data)
            print("Message received from client:", json_data)
            
            # Process the data (this is just an example)
            json_data["response"] = "Processed by server"
            
            # Serialize the JSON response to a string
            response_data = json.dumps(json_data)
            
            # Send the JSON data back to the client
            await websocket.send_text(response_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_websockets.remove(websocket)



# Include routers for different endpoints
app.include_router(query_router, prefix="/api/query")
app.include_router(answer_router, prefix="/api/answer")
app.include_router(upload_router, prefix="/api/upload")
app.include_router(files_router, prefix="/api/files")
app.include_router(read_data_router, prefix="/api/read-data")
app.include_router(load_url_router, prefix="/api/load-urls")
app.include_router(ws_router, prefix="/api/websockets")
 
app.mount("/files", StaticFiles(directory="files"), name="static")
# Define a startup event handler to call setup_chroma asynchronously
@app.on_event("startup")
async def startup_event():
    await chroma_setup.setup_chroma(is_reset=False)

# Add middleware to the app

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (you can restrict this to specific origins)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow these HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Command to start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000 )