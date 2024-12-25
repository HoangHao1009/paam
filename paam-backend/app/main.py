from fastapi import FastAPI
from app.routes import survey, analyze, export, survey
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost", 
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép các domain này
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)


app.include_router(survey.router, prefix="/survey", tags=["Survey"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analytic"])
app.include_router(export.router, prefix="/export", tags=["Export"])

@app.get("/")
async def root():
    return {"message": "PAAM"}
