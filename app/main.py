from fastapi import FastAPI
from app.routes import config, dashboard

app = FastAPI()

app.include_router(config.router, prefix="/config", tags=["Configuration"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {"message": "PAAM"}
