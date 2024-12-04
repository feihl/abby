from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# Database initialization function
def initialize_db():
    connection = sqlite3.connect('pquiz_db.sqlite3')
    cursor = connection.cursor()

    # Create tables if not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quiz_id INTEGER,
                        question_text TEXT NOT NULL,
                        choices TEXT NOT NULL,
                        correct_answer INTEGER,
                        FOREIGN KEY (quiz_id) REFERENCES quizzes (id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quiz_id INTEGER,
                        user_id INTEGER,
                        answers TEXT NOT NULL,
                        FOREIGN KEY (quiz_id) REFERENCES quizzes (id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_name TEXT NOT NULL,
                        description TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS levels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level_name TEXT NOT NULL,
                        description TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic_name TEXT NOT NULL,
                        description TEXT)''')

    connection.commit()
    connection.close()

# Initialize the database at startup
initialize_db()

# Function to get a database connection
def get_db_connection():
    return sqlite3.connect('pquiz_db.sqlite3')

# Define Pydantic models for request/response validation

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None

class QuizResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

class QuestionCreate(BaseModel):
    quiz_id: int
    question_text: str
    choices: str
    correct_answer: int

class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    choices: str
    correct_answer: int

class AttemptCreate(BaseModel):
    quiz_id: int
    user_id: int
    answers: str

class AttemptResponse(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    answers: str

class CategoryCreate(BaseModel):
    category_name: str
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    category_name: str
    description: Optional[str] = None

class LevelCreate(BaseModel):
    level_name: str
    description: Optional[str] = None

class LevelResponse(BaseModel):
    id: int
    level_name: str
    description: Optional[str] = None

class TopicCreate(BaseModel):
    topic_name: str
    description: Optional[str] = None

class TopicResponse(BaseModel):
    id: int
    topic_name: str
    description: Optional[str] = None

# API Endpoints with integrated Pydantic models

@app.post("/quizzes/", response_model=QuizResponse)
def create_quiz(quiz: QuizCreate):
    connection = get_db_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO quizzes (title, description) VALUES (?, ?)",
                (quiz.title, quiz.description)
            )
            quiz_id = cursor.lastrowid
        return {"id": quiz_id, "title": quiz.title, "description": quiz.description}
    finally:
        connection.close()

@app.get("/quizzes/", response_model=List[QuizResponse])
def get_quizzes():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM quizzes")
        quizzes = cursor.fetchall()
        return [QuizResponse(id=q[0], title=q[1], description=q[2]) for q in quizzes]
    finally:
        connection.close()

@app.put("/quizzes/{quiz_id}", response_model=QuizResponse)
def update_quiz(quiz_id: int, quiz: QuizCreate):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute(
                "UPDATE quizzes SET title = ?, description = ? WHERE id = ?",
                (quiz.title, quiz.description, quiz_id)
            )
        return {"id": quiz_id, "title": quiz.title, "description": quiz.description}
    finally:
        connection.close()

@app.delete("/quizzes/{quiz_id}", response_model=QuizResponse)
def delete_quiz(quiz_id: int):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
        return {"message": "Quiz deleted successfully"}
    finally:
        connection.close()

@app.post("/quizzes/{quiz_id}/questions/", response_model=QuestionResponse)
def add_question(quiz_id: int, question: QuestionCreate):
    connection = get_db_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO questions (quiz_id, question_text, choices, correct_answer) VALUES (?, ?, ?, ?)",
                (quiz_id, question.question_text, question.choices, question.correct_answer)
            )
            question_id = cursor.lastrowid
        return {**question.dict(), "id": question_id}
    finally:
        connection.close()

@app.get("/quizzes/{quiz_id}/questions/", response_model=List[QuestionResponse])
def get_questions(quiz_id: int):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
        questions = cursor.fetchall()
        return [QuestionResponse(id=q[0], quiz_id=q[1], question_text=q[2], choices=q[3], correct_answer=q[4]) for q in questions]
    finally:
        connection.close()

@app.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, question: QuestionCreate):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute(
                "UPDATE questions SET question_text = ?, choices = ?, correct_answer = ? WHERE id = ?",
                (question.question_text, question.choices, question.correct_answer, question_id)
            )
        return {**question.dict(), "id": question_id}
    finally:
        connection.close()

@app.delete("/questions/{question_id}", response_model=QuestionResponse)
def delete_question(question_id: int):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        return {"message": "Question deleted successfully"}
    finally:
        connection.close()

# Attempts CRUD with Pydantic models

@app.post("/attempts/", response_model=AttemptResponse)
def create_attempt(attempt: AttemptCreate):
    connection = get_db_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO attempts (quiz_id, user_id, answers) VALUES (?, ?, ?)",
                (attempt.quiz_id, attempt.user_id, attempt.answers)
            )
            attempt_id = cursor.lastrowid
        return {**attempt.dict(), "id": attempt_id}
    finally:
        connection.close()

@app.get("/attempts/{attempt_id}", response_model=AttemptResponse)
def get_attempt(attempt_id: int):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,))
        attempt = cursor.fetchone()
        if attempt:
            return AttemptResponse(id=attempt[0], quiz_id=attempt[1], user_id=attempt[2], answers=attempt[3])
        else:
            raise HTTPException(status_code=404, detail="Attempt not found")
    finally:
        connection.close()

# Categories CRUD with Pydantic models

@app.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    connection = get_db_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO categories (category_name, description) VALUES (?, ?)",
                (category.category_name, category.description)
            )
            category_id = cursor.lastrowid
        return {**category.dict(), "id": category_id}
    finally:
        connection.close()

@app.get("/categories/", response_model=List[CategoryResponse])
def get_categories():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return [CategoryResponse(id=c[0], category_name=c[1], description=c[2]) for c in categories]
    finally:
        connection.close()

@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute(
                "UPDATE categories SET category_name = ?, description = ? WHERE id = ?",
                (category.category_name, category.description, category_id)
            )
        return {**category.dict(), "id": category_id}
    finally:
        connection.close()

@app.delete("/categories/{category_id}", response_model=dict)
def delete_category(category_id: int):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        return {"message": "Category deleted successfully"}
    finally:
        connection.close()

# Levels CRUD with Pydantic models

@app.post("/levels/", response_model=LevelResponse)
def create_level(level: LevelCreate):
    connection = get_db_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO levels (level_name, description) VALUES (?, ?)",
                (level.level_name, level.description)
            )
            level_id = cursor.lastrowid
        return {**level.dict(), "id": level_id}
    finally:
        connection.close()

@app.get("/levels/", response_model=List[LevelResponse])
def get_levels():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM levels")
        levels = cursor.fetchall()
        return [LevelResponse(id=l[0], level_name=l[1], description=l[2]) for l in levels]
    finally:
        connection.close()

@app.put("/levels/{level_id}", response_model=LevelResponse)
def update_level(level_id: int, level: LevelCreate):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute(
                "UPDATE levels SET level_name = ?, description = ? WHERE id = ?",
                (level.level_name, level.description, level_id)
            )
        return {**level.dict(), "id": level_id}
    finally:
        connection.close()

@app.delete("/levels/{level_id}", response_model=dict)
def delete_level(level_id: int):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute("DELETE FROM levels WHERE id = ?", (level_id,))
        return {"message": "Level deleted successfully"}
    finally:
        connection.close()

# Topics CRUD with Pydantic models

@app.post("/topics/", response_model=TopicResponse)
def create_topic(topic: TopicCreate):
    connection = get_db_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO topics (topic_name, description) VALUES (?, ?)",
                (topic.topic_name, topic.description)
            )
            topic_id = cursor.lastrowid
        return {**topic.dict(), "id": topic_id}
    finally:
        connection.close()

@app.get("/topics/", response_model=List[TopicResponse])
def get_topics():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM topics")
        topics = cursor.fetchall()
        return [TopicResponse(id=t[0], topic_name=t[1], description=t[2]) for t in topics]
    finally:
        connection.close()

@app.put("/topics/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: int, topic: TopicCreate):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute(
                "UPDATE topics SET topic_name = ?, description = ? WHERE id = ?",
                (topic.topic_name, topic.description, topic_id)
            )
        return {**topic.dict(), "id": topic_id}
    finally:
        connection.close()

@app.delete("/topics/{topic_id}", response_model=dict)
def delete_topic(topic_id: int):
    connection = get_db_connection()
    try:
        with connection:
            connection.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        return {"message": "Topic deleted successfully"}
    finally:
        connection.close()
