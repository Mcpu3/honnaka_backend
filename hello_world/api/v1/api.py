from fastapi import APIRouter


api_router = APIRouter()

@api_router.get("/sample")
def index():
    return {
        "info": "Try /hello/honnaka for parameterized route."
    }

@api_router.get("/hello/{name}")
def get_name(name: str):
    return {
        "name": name
    }