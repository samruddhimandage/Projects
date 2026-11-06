# Marvellous SmartHire – AI Mock Interview Agent (CLI)

A simple command-line AI mock interview application. It uses a local Ollama
Llama 3 model to generate technical interview questions, evaluate candidate
answers, provide feedback and save a Markdown interview report.

## Features
- Configure job role, experience level, topic and question count.
- Generate one question at a time using an LLM.
- Evaluate answers with a score out of 10.
- Provide correctness feedback, strengths, improvements and an example answer.
- Calculate total and average scores.
- Save a timestamped Markdown report in `reports/`.

## Project structure
```text
Marvellous_SmartHire/
├── app.py
├── requirements.txt
├── README.md
└── reports/                 # Created automatically after an interview
```

## Prerequisites
- Python 3.10 or newer.
- Ollama installed: https://ollama.com/download
- Local machine resources sufficient to run the selected Ollama model.

## Windows setup
Open a terminal in this folder:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Download the model
```powershell
ollama pull llama3
```

Make sure the Ollama service is running. If it is not running automatically,
open the Ollama desktop app or run `ollama serve` in a separate terminal.

## Run
```powershell
python app.py
```

Enter the job role, experience level, topic and number of questions. Answer
each question when prompted. Feedback is shown in the terminal after each answer.
At the end, the report is saved automatically under `reports/`.

## Configuration
The model name is set near the top of `app.py`:
```python
MODEL = "llama3"
```
If you downloaded a different Ollama model, update this value to its exact
local model name (for example, `llama3.2:1b`).

## Limitations
- This is a terminal-based prototype; it does not use Streamlit, Flask or a web UI.
- The model's scores and feedback are generated estimates for practice and
  should not be treated as objective hiring decisions.
- Requires Ollama and the selected model to be available locally.
