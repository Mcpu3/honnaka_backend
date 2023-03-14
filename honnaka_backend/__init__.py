import azure.functions as func
from fastapi import FastAPI

from honnaka_backend.api.v1 import api


app = FastAPI()
app.include_router(api.api_router, prefix="/api/v1")

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return await func.AsgiMiddleware(app).handle_async(req, context)
