from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, analyses, subscription

app = FastAPI(title="LabLeaf API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analyses.router)
app.include_router(subscription.router)


@app.get("/")
def root():
    return {"status": "LabLeaf API rodando!"}
