from fastapi import FastAPI
from backend.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Learning Evaluation SaaS",
    version="1.0.0"
)

# -------------------------
# CORS (PRODUCTION SAFE)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTES
# -------------------------
app.include_router(router)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "AI Evaluation SaaS"
    }