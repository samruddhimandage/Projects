"""
Marvellous SmartHire - AI Mock Interview Agent (Command Line Version)

Requirements:
    pip install -r requirements.txt

Ollama setup (in a separate terminal):
    ollama pull llama3
    ollama serve

Run:
    python app.py
"""

import json
import re
from datetime import datetime
from pathlib import Path

import ollama

MODEL = "llama3"
REPORT_DIR = Path(__file__).resolve().parent / "reports"


def ask_ollama(prompt: str) -> str:
    """Send a prompt to the locally running Ollama model."""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.3}
    )
    return response["message"]["content"].strip()


def generate_question(role: str, level: str, topic: str,
                      question_number: int, previous_questions: list[str]) -> str:
    previous = "\n".join(f"- {q}" for q in previous_questions) or "None"
    prompt = f"""
You are a professional technical interviewer.
Generate exactly ONE clear technical interview question.

Candidate role: {role}
Experience level: {level}
Topic: {topic}
Question number: {question_number}
Questions already asked (do not repeat or closely paraphrase):
{previous}

Return only the question. Do not include an answer, hints, or a question number.
"""
    return ask_ollama(prompt)


def extract_json(text: str) -> dict:
    """Parse JSON even if the model wraps it in Markdown fences."""
    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "").strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("The model did not return valid JSON. Please evaluate again.")
    data = json.loads(match.group())
    score = float(data["score"])
    data["score"] = max(0.0, min(10.0, score))
    for key in ("correctness", "strengths", "improvements", "ideal_answer"):
        data[key] = str(data.get(key, "Not provided."))
    return data


def evaluate_answer(role: str, level: str, topic: str,
                    question: str, answer: str) -> dict:
    prompt = f"""
You are a fair technical interview evaluator. Evaluate only the answer provided.
Do not assume skills that the candidate has not demonstrated.

Role: {role}
Experience level: {level}
Topic: {topic}

Interview question:
{question}

Candidate answer:
{answer}

Assess technical correctness, conceptual understanding, completeness, and clarity.
Give a score from 0 to 10. Be consistent with the experience level.
A blank, irrelevant, or incorrect answer must receive a low score.

Return ONLY one valid JSON object with exactly these keys:
{{
  "score": 0,
  "correctness": "Brief assessment of technical correctness",
  "strengths": "What was done well",
  "improvements": "Specific improvements needed",
  "ideal_answer": "A concise example of a strong answer"
}}
"""
    return extract_json(ask_ollama(prompt))


def get_nonempty_input(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Please enter a value.")


def save_report(role: str, level: str, topic: str, results: list[dict]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    total = sum(item["evaluation"]["score"] for item in results)
    average = total / len(results) if results else 0.0

    lines = [
        "# Marvellous SmartHire - Interview Report",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Job role: {role}",
        f"- Experience level: {level}",
        f"- Topic: {topic}",
        f"- Questions attempted: {len(results)}",
        f"- Total score: {total:.1f}/{len(results) * 10}",
        f"- Average score: {average:.2f}/10",
        "",
        "> Scores and feedback are AI-generated practice guidance, not objective hiring decisions.",
        ""
    ]

    for index, item in enumerate(results, start=1):
        evaluation = item["evaluation"]
        lines.extend([
            f"## Question {index}",
            "",
            f"**Question:** {item['question']}",
            "",
            f"**Candidate answer:** {item['answer']}",
            "",
            f"**Score:** {evaluation['score']:.1f}/10",
            "",
            f"**Technical correctness:** {evaluation['correctness']}",
            "",
            f"**Strengths:** {evaluation['strengths']}",
            "",
            f"**Areas for improvement:** {evaluation['improvements']}",
            "",
            f"**Example strong answer:** {evaluation['ideal_answer']}",
            "",
            "---",
            ""
        ])

    filename = f"SmartHire_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path = REPORT_DIR / filename
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    print("=" * 62)
    print("       MARVELLOUS SMART HIRE - AI MOCK INTERVIEW AGENT")
    print("=" * 62)
    print("This is a command-line application; no Streamlit or web UI is used.\n")

    print("Interview configuration")
    role = get_nonempty_input("Job role (e.g. Python Developer): ")
    level = get_nonempty_input("Experience level (Fresher/Intermediate/Experienced): ")
    topic = get_nonempty_input("Interview topic (e.g. Python, SQL, ML): ")

    while True:
        try:
            total_questions = int(input("Number of questions (1-10): ").strip())
            if 1 <= total_questions <= 10:
                break
            print("Enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid whole number.")

    results = []
    previous_questions = []

    try:
        for number in range(1, total_questions + 1):
            print("\n" + "=" * 62)
            print(f"QUESTION {number} OF {total_questions}")
            print("=" * 62)

            question = generate_question(
                role, level, topic, number, previous_questions
            )
            previous_questions.append(question)
            print("\nAI Interviewer:", question)

            answer = input("\nYour answer (type your response and press Enter): ").strip()
            while not answer:
                print("Answer cannot be empty.")
                answer = input("Your answer: ").strip()

            print("\nEvaluating your answer...")
            evaluation = evaluate_answer(role, level, topic, question, answer)
            results.append({
                "question": question,
                "answer": answer,
                "evaluation": evaluation
            })

            print(f"\nScore: {evaluation['score']:.1f}/10")
            print("Correctness:", evaluation["correctness"])
            print("Strengths:", evaluation["strengths"])
            print("Improvements:", evaluation["improvements"])
            print("Example strong answer:", evaluation["ideal_answer"])

        report_path = save_report(role, level, topic, results)
        total = sum(item["evaluation"]["score"] for item in results)
        average = total / len(results)

        print("\n" + "=" * 62)
        print("                 INTERVIEW SUMMARY")
        print("=" * 62)
        print(f"Questions attempted : {len(results)}")
        print(f"Total score         : {total:.1f}/{len(results) * 10}")
        print(f"Average score       : {average:.2f}/10")
        print(f"Report saved to     : {report_path}")
        print("\nInterview completed. Thank you for using Marvellous SmartHire!")

    except KeyboardInterrupt:
        print("\nInterview cancelled by user.")
    except Exception as exc:
        print(f"\nApplication error: {exc}")
        print("Check that Ollama is running and the configured model is installed.")


if __name__ == "__main__":
    main()
