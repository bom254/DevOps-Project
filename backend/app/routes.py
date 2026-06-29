from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random
import logging
import time

logger = logging.getLogger("trivia-api")
router = APIRouter()

QUESTIONS = [
    {
        "id": 1,
        "question": "what does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Central Processor Utility", "Core Processing Unit"],
        "answer": "Central Processing Unit",
        "category": "Technology",
    },
    {
        "id": 2,
        "question": "Which company created Kubernetes?",
        "options": ["Amazon", "Microsoft", "Google", "IBM"],
        "answer": "Google",
        "category": "DevOps",
    },
    {
        "id": 3,
        "question": "What is the default port for HTTPS?",
        "options": ["80", "443", "8080", "3000"],
        "answer": "443",
        "category": "Networking",
    },
    {
        "id": 4,
        "question": "What does CI/CD stand for?",
        "options": [
            "Continuous Integration / Continuous Delivery",
            "Code Integration / Code Deployment",
            "Continuous Iteration / Continuous Design",
            "Core Infrastructure / Core Deployment",
        ],
        "answer": "Continuous Integration / Continuous Delivery",
        "category": "DevOps",
    },
    {
        "id": 5,
        "question": "Which file format does Docker use for build instructions?",
        "options": ["Makefile", "Dockerfile", "docker.yaml", "container.conf"],
        "answer": "Dockerfile",
        "category": "DevOps",
    },
    {
        "id": 6,
        "question": "What is the primary purpose of Elasticsearch?",
        "options": ["Container orchestration", "Search and analytics", "CI/CD pipelines", "Load balancing"],
        "answer": "Search and analytics",
        "category": "Technology",
    },
    {
        "id": 7,
        "question": "What does DNS stand for?",
        "options": ["Domain Name System", "Data Network Service", "Dynamic Node Server", "Distributed Name Service"],
        "answer": "Domain Name System",
        "category": "Networking",
    },
    {
        "id": 8,
        "question": "In Git, which command creates a new branch and switches to it?",
        "options": ["git branch -new", "git checkout -b", "git switch --create", "git new-branch"],
        "answer": "git checkout -b",
        "category": "Development",
    },
    {
        "id": 9,
        "question": "What does ArgoCD implement?",
        "options": ["GitOps continuous delivery", "Container scanning", "Log aggregation", "Service mesh"],
        "answer": "GitOps continuous delivery",
        "category": "DevOps",
    },
    {
        "id": 10,
        "question": "Which HTTP method is used to update an existing resource?",
        "options": ["GET", "POST", "PUT", "DELETE"],
        "answer": "PUT",
        "category": "Development",
    },
]

class AnswerRequest(BaseModel):
    question_id: int
    answer: str

@router.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok", "service": "trivia-api", "timestamp": time.time()}

@router.get("/questions")
def get_questions(count: int = 5):
    start = time.time()
    if count < 1 or count > len(QUESTIONS):
        raise HTTPException(
            status_code=400,
            detail=f"count must be between 1 and {len(QUESTIONS)}",
        )
    selected = random.sample(QUESTIONS, count)
    # strip answers before sending to client
    safe = [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "category": q["category"],
        }
        for q in selected
    ]
    elapsed = round((time.time() - start) * 1000, 2)
    logger.info(f"Served {count} questions in {elapsed}ms")
    return {"questions": safe, "total": count}

@router.post("/answer")
def check_answer(payload: AnswerRequest):
    start = time.time()
    question = next((q for q in QUESTIONS if q["id"] == payload.question_id), None)
    if not question:
        logger.warning(f"Answer attempt for unknown question id={payload.question_id}")
        raise HTTPException(status_code=404, details="Question not found")
    correct = question["answer"] == payload.answer
    elapsed = round((time.time() - start) * 1000, 2)
    logger.info(
        f"Answer checked: question_id={payload.question_id} correct={correct} elapsed={elapsed}ms"
    )
    return {
        "correct": correct,
        "correct_answer": question["answer"],
        "question_id": payload.question_id,
    }