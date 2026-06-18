from ai_engine.evaluator import evaluate_video
from ai_engine.scoring import clean_numpy

from backend.database import (
    videos_collection,
    evaluations_collection,
    users_collection,
    tasks_collection,
    db
)

from backend.auth.security import create_access_token
from backend.auth.password import hash_password, verify_password

from fastapi import APIRouter, UploadFile, File, Body, BackgroundTasks
import uuid
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# NEW COLLECTIONS (SAAS LAYER)
submissions_collection = db["submissions"]
analytics_collection = db["analytics"]


# =========================
# HEALTH
# =========================
@router.get("/health")
def health():
    return {"status": "ok"}


# =========================
# TASKS
# =========================
@router.get("/tasks")
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    return {"success": True, "tasks": tasks}


# =========================
# REGISTER
# =========================
@router.post("/register")
def register(payload: dict = Body(...)):

    email = payload.get("email")
    password = payload.get("password")
    name = payload.get("name")
    role = payload.get("role", "student")

    if users_collection.find_one({"email": email}):
        return {"success": False, "message": "User already exists"}

    user = {
        "user_id": str(uuid.uuid4()),
        "email": email,
        "password": hash_password(password),
        "name": name,
        "role": role
    }

    users_collection.insert_one(user)

    return {"success": True, "message": "User created"}


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(payload: dict = Body(...)):

    email = payload.get("email")
    password = payload.get("password")

    user = users_collection.find_one({"email": email})

    if not user:
        return {"success": False, "message": "User not found"}

    if not verify_password(password, user["password"]):
        return {"success": False, "message": "Invalid password"}

    token = create_access_token({
        "user_id": user["user_id"],
        "role": user["role"]
    })

    return {
        "success": True,
        "access_token": token,
        "user": {
            "user_id": user["user_id"],
            "email": user["email"],
            "role": user["role"]
        }
    }


# =========================
# CREATE TASK
# =========================
@router.post("/create-task")
def create_task(payload: dict = Body(...)):

    task = {
        "task_id": str(uuid.uuid4()),
        "title": payload.get("title"),
        "topic": payload.get("topic"),
        "expected_concepts": payload.get("expected_concepts", []),
        "difficulty": payload.get("difficulty", "medium"),
        "created_at": datetime.utcnow().isoformat()
    }

    tasks_collection.insert_one(task)

    return {"success": True, "task": task}


# =========================
# UPLOAD VIDEO (SUBMISSION LAYER)
# =========================
@router.post("/upload-video")
async def upload_video(
    file: UploadFile = File(...),
    task_id: str = None,
    user_id: str = None
):

    video_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    video_doc = {
        "video_id": video_id,
        "file_name": file.filename,
        "file_path": file_path,
        "task_id": task_id,
        "user_id": user_id,
        "status": "uploaded",
        "created_at": datetime.utcnow().isoformat()
    }

    videos_collection.insert_one(video_doc)

    # NEW: submission tracking
    submissions_collection.insert_one({
        "submission_id": str(uuid.uuid4()),
        "video_id": video_id,
        "task_id": task_id,
        "user_id": user_id,
        "status": "uploaded",
        "created_at": datetime.utcnow().isoformat()
    })

    return {
        "success": True,
        "video_id": video_id,
        "task_id": task_id,
        "user_id": user_id
    }


# =========================
# BACKGROUND EVALUATION ENGINE
# =========================
def run_evaluation(video_id: str, video_path: str, task_id: str, user_id: str):

    try:
        evaluation = evaluate_video(video_path)
        evaluation = clean_numpy(evaluation)

        evaluations_collection.insert_one({
            "video_id": video_id,
            "task_id": task_id,
            "user_id": user_id,
            "evaluation": evaluation,
            "created_at": datetime.utcnow().isoformat()
        })

        # update submission status
        submissions_collection.update_one(
            {"video_id": video_id},
            {"$set": {"status": "evaluated"}}
        )

        # update video status
        videos_collection.update_one(
            {"video_id": video_id},
            {"$set": {"status": "evaluated"}}
        )

        # NEW: analytics aggregation entry
        analytics_collection.insert_one({
            "user_id": user_id,
            "task_id": task_id,
            "video_id": video_id,
            "final_score": evaluation.get("result", {}).get("final_score", 0),
            "grade": evaluation.get("result", {}).get("grade", "N/A"),
            "created_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        evaluations_collection.insert_one({
            "video_id": video_id,
            "error": str(e),
            "status": "failed"
        })


# =========================
# TRIGGER EVALUATION (SaaS Async)
# =========================
@router.post("/evaluate-video")
def evaluate(video_id: str, background_tasks: BackgroundTasks):

    video = videos_collection.find_one({"video_id": video_id})

    if not video:
        return {"success": False, "message": "Video not found"}

    background_tasks.add_task(
        run_evaluation,
        video_id,
        video["file_path"],
        video.get("task_id"),
        video.get("user_id")
    )

    return {
        "success": True,
        "message": "Evaluation started",
        "video_id": video_id
    }


# =========================
# GET EVALUATION RESULT
# =========================
@router.get("/evaluation/{video_id}")
def get_evaluation(video_id: str):

    result = evaluations_collection.find_one(
        {"video_id": video_id},
        {"_id": 0}
    )

    if not result:
        return {
            "success": False,
            "message": "Evaluation not ready"
        }

    return {"success": True, "data": result}


# =========================
# SAAS DASHBOARD API (STEP 22 CORE)
# =========================
@router.get("/dashboard/{user_id}")
def dashboard(user_id: str):

    submissions = list(submissions_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ))

    analytics = list(analytics_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ))

    total = len(submissions)
    evaluated = len([s for s in submissions if s["status"] == "evaluated"])

    avg_score = 0
    if analytics:
        avg_score = sum([a.get("final_score", 0) for a in analytics]) / len(analytics)

    return {
        "success": True,
        "stats": {
            "total_submissions": total,
            "evaluated": evaluated,
            "average_score": round(avg_score, 2)
        },
        "submissions": submissions,
        "analytics": analytics
    }