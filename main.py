from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from courses import COURSE_CATALOG
from logic import process_subject_marks, calculate_cgpa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint 1: Send list of available courses to frontend dropdown
@app.get("/courses")
def get_courses():
    return COURSE_CATALOG


class SubjectInput(BaseModel):
    course_code: str
    cca1: float
    cca2: float
    assignment: float
    endsem: float


class CGPARequest(BaseModel):
    subjects: list[SubjectInput]


# Endpoint 2: Process all entered subjects and return CGPA report
@app.post("/calculate-cgpa")
def compute_cgpa_api(data: CGPARequest):
    processed_list = []

    for item in data.subjects:
        res = process_subject_marks(
            item.course_code, item.cca1, item.cca2, item.assignment, item.endsem
        )
        if res:
            processed_list.append(res)

    cgpa = calculate_cgpa(processed_list)
    total_credits = sum(x["credits"] for x in processed_list)

    return {
        "cgpa": cgpa,
        "total_credits": total_credits,
        "subjects_detail": processed_list
    }