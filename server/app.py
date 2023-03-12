import mimetypes
from pathlib import Path
from fastapi import FastAPI, responses, WebSocket, WebSocketDisconnect

import ntpro_server
from routers import db_test
from db.database import engine, Base

api = FastAPI()
api.include_router(db_test.router)

server = ntpro_server.NTProServer()
html = Path("static/test.html").read_text()
Base.metadata.create_all(engine)

# ---[METHODS]---

@api.get('/')
async def get():
    return responses.HTMLResponse(html)


@api.get('/static/{path}')
async def get(path: Path):
    static_file = (Path('static') / path).read_text()
    mime_type, encoding = mimetypes.guess_type(path)
    return responses.PlainTextResponse(static_file, media_type=mime_type)


@api.websocket('/ws/')
async def websocket_endpoint(websocket: WebSocket):
    await server.connect(websocket)

    try:
        await server.serve(websocket)
    except WebSocketDisconnect:
        server.disconnect(websocket)
