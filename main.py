from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List
from uuid import uuid4

app = FastAPI()

class Student(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr

# In-memory storage for students
students = {}

# Helper function to generate a unique ID
def generate_id():
    return str(uuid4())

# Add initial data
def populate_initial_data():
    initial_students = [
        Student(id=generate_id(), name="Alice Johnson", age=21, email="alice.johnson@example.com"),
        Student(id=generate_id(), name="Bob Smith", age=19, email="bob.smith@example.com"),
        Student(id=generate_id(), name="Carol White", age=22, email="carol.white@example.com"),
    ]
    for student in initial_students:
        students[student.id] = student

# Populate data on app startup
populate_initial_data()

@app.post("/students", response_model=Student)
async def create_student(student: Student):
    student_id = generate_id()
    new_student = student.copy(update={"id": student_id})
    students[student_id] = new_student
    return new_student

@app.get("/students", response_model=List[Student])
async def get_all_students():
    return list(students.values())

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student_data: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student = student_data.copy(update={"id": student_id})
    students[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}", response_model=dict)
async def delete_student(student_id: str):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"detail": "Student deleted successfully"}

@app.get("/students/{student_id}/summary")
async def generate_student_summary(student_id: str):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Placeholder for AI-based summary generation
    summary = f"Student {student.name}, aged {student.age}, has email {student.email}."
    return {"summary": summary}
