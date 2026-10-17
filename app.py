from __future__ import annotations

import csv
import random
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "quizzel-local-development-key"

SCORE_FILE = Path(__file__).resolve().parent / "punteggi" / "punteggi.csv"

# Le capitali sono incorporate per rendere il quiz autonomo anche offline.
QUESTIONS = [
    {"country": "Francia", "answer": "Parigi", "type": "open"},
    {"country": "Italia", "answer": "Roma", "type": "open"},
    {"country": "Grecia", "answer": "Atene", "type": "open"},
    {"country": "Portogallo", "answer": "Lisbona", "type": "open"},
    {"country": "Svezia", "answer": "Stoccolma", "type": "open"},
    {"country": "Germania", "answer": "Berlino", "type": "multiple", "options": ["Berlino", "Bonn", "Amburgo", "Monaco"]},
    {"country": "Spagna", "answer": "Madrid", "type": "multiple", "options": ["Barcellona", "Madrid", "Siviglia", "Valencia"]},
    {"country": "Austria", "answer": "Vienna", "type": "multiple", "options": ["Salisburgo", "Graz", "Vienna", "Linz"]},
    {"country": "Polonia", "answer": "Varsavia", "type": "multiple", "options": ["Cracovia", "Danzica", "Lublino", "Varsavia"]},
    {"country": "Norvegia", "answer": "Oslo", "type": "multiple", "options": ["Bergen", "Oslo", "Trondheim", "Stavanger"]},
]


def normalize(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def start_quiz(username: str) -> None:
    questions = random.sample(QUESTIONS, len(QUESTIONS))
    for question in questions:
        if question["type"] == "multiple":
            question["options"] = random.sample(question["options"], len(question["options"]))
    session.clear()
    session["username"] = username
    session["questions"] = questions
    session["question_index"] = 0
    session["answers"] = []


@app.get("/")
def home():
    session.clear()
    return render_template("home.html", error=None)


@app.post("/start")
def start():
    username = request.form.get("username", "").strip()
    if not username:
        return render_template("home.html", error="Inserisci uno username per iniziare."), 400
    if len(username) > 40:
        return render_template("home.html", error="Lo username può contenere al massimo 40 caratteri."), 400
    start_quiz(username)
    return redirect(url_for("quiz"))


@app.get("/quiz")
def quiz():
    questions = session.get("questions")
    if not questions:
        return redirect(url_for("home"))
    index = session.get("question_index", 0)
    if index >= len(questions):
        return redirect(url_for("results"))
    return render_template("quiz.html", username=session["username"], question=questions[index], index=index, total=len(questions))


@app.post("/submit")
def submit():
    questions = session.get("questions")
    if not questions:
        return redirect(url_for("home"))
    index = session.get("question_index", 0)
    if index >= len(questions):
        return redirect(url_for("results"))
    answers = session.get("answers", [])
    answer = request.form.get("answer", "").strip()
    answers.append(answer)
    session["answers"] = answers

    if index + 1 < len(questions):
        session["question_index"] = index + 1
        return redirect(url_for("quiz"))

    results = []
    score = 0
    for question, user_answer in zip(questions, answers):
        correct = normalize(user_answer) == normalize(question["answer"])
        if correct:
            score += 10
        results.append({**question, "user_answer": user_answer, "correct": correct})

    SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)
    new_file = not SCORE_FILE.exists() or SCORE_FILE.stat().st_size == 0
    with SCORE_FILE.open("a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        if new_file:
            writer.writerow(["username", "punteggio", "data_ora"])
        writer.writerow([session.get("username", ""), score, datetime.now().astimezone().isoformat(timespec="seconds")])

    session["results"] = results
    session["score"] = score
    session.pop("questions", None)
    return redirect(url_for("results"))


@app.get("/results")
def results():
    if "results" not in session:
        return redirect(url_for("home"))
    return render_template("results.html", username=session.get("username", ""), score=session["score"], results=session["results"])


@app.post("/restart")
def restart():
    username = session.get("username", "")
    if not username:
        return redirect(url_for("home"))
    start_quiz(username)
    return redirect(url_for("quiz"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
