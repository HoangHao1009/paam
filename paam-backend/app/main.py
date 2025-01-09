from fastapi import FastAPI
from app.routes import create, process, analyze, report
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


app.include_router(create.router, prefix="/create", tags=["Create"])
app.include_router(process.router, prefix="/process", tags=["Process"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
app.include_router(report.router, prefix="/report", tags=["Report"])

@app.get("/")
async def root():
    return {"message": "PAAM"}
