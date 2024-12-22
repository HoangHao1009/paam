from fastapi import FastAPI
from app.routes import survey, analyze, export, survey

app = FastAPI()

app.include_router(survey.router, prefix="/survey", tags=["Survey"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analytic"])
app.include_router(export.router, prefix="/export", tags=["Export"])

@app.get("/")
async def root():
    return {"message": "PAAM"}
