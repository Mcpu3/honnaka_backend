import azure.functions as func
from fastapi import FastAPI

from users.api.v1 import api


app = FastAPI()
app.include_router(api.api_router, prefix="/api/v1")

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req, context)
