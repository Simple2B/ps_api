# Project S
import os

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from .config import CFG

from .route import router



def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


api = FastAPI(generate_unique_id_function=custom_generate_unique_id, version=CFG.VERSION)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(router)


@api.get("/", tags=["root"])
async def root():
    return FileResponse(os.path.join(CFG.STATIC_DIR, "index.html"))


@api.get("/{wildcard_path:path}", tags=["root"])
async def wildcard_path(request: Request, wildcard_path: str):
    accept = request.headers.get("accept")
    if not accept or "text/html" not in accept:
        return FileResponse(os.path.join(CFG.STATIC_DIR, wildcard_path))
    return FileResponse(os.path.join(CFG.STATIC_DIR, "index.html"))
