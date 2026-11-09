<<<<<<< HEAD
<<<<<<< HEAD
# OpsMind AI

**Memory-powered Incident Response Agent** built for Hack with Hyderabad 3.0.

OpsMind helps IT operations teams triage incidents by recalling verified resolutions from previous incidents using Hindsight.

## Features
- Incident intake with service, severity, environment, logs, and impact.
- Hindsight `recall` to retrieve relevant past incidents.
- Hindsight `reflect` to generate context-aware triage guidance.
- Hindsight `retain` to save verified resolutions and postmortems.
- Memory explorer and seeded demo incident.
- Explicit separation between AI recommendations and engineer-verified fixes.

## Architecture
Streamlit UI -> Python incident workflow -> Hindsight Cloud
- `recall`: retrieve similar historical incidents.
- `reflect`: reason over the incident and available memory.
- `retain`: store verified resolution and prevention actions.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add your Hindsight API key. Do not commit `.env`.

```powershell
streamlit run app.py
```

## Hindsight setup
1. Sign in at https://ui.hindsight.vectorize.io
2. Open Connect and create an API key.
3. Add the key to `.env`.
4. The app creates/reuses the `opsmind-incidents` memory bank.

## Demo script
1. Open **Demo data** and seed the database connection incident.
2. Open **Diagnose incident**.
3. Enter a similar incident: database timeout / too many connections / API 500 errors.
4. Show recalled memory and the recommendation informed by the earlier verified fix.
5. Save a new verified resolution.
6. Search the **Memory explorer**.

## Safety
This prototype does not execute infrastructure commands. It provides advisory troubleshooting only. Verify any suggested action with an authorized engineer before applying it.

## Submission checklist
- [ ] Add screenshots and a short architecture diagram.
- [ ] Verify Hindsight recall/retain/reflect against your own cloud bank.
- [ ] Record the demo video.
- [ ] Add the hackathon article, social post, and video deliverables.
=======
# OpsMind-AI
AI-powered incident management using persistent Hindsight memory
>>>>>>> 21871f7b622b9d468fe3bd6ffb1ac974a5f7ce03
=======

# 🧠 OpsMind AI

### Memory-Aware AI Incident Diagnosis and Resolution Assistant

OpsMind AI is an AI-powered IT operations assistant that helps engineers diagnose production incidents using historical incident knowledge.

## 🚀 Key Features

- Incident reporting and classification
- AI-assisted root cause analysis
- Historical incident retrieval using Hindsight
- Reusable resolution knowledge
- Verified fix storage
- Memory-aware incident diagnosis

## 🛠️ Technology Stack

- Python
- Streamlit
- Hindsight AI
- REST API
- Git and GitHub

## 🔄 Workflow

1. Report a production incident.
2. Retrieve relevant historical incidents.
3. Generate diagnosis and recommendations.
4. Engineer verifies the resolution.
5. Save the verified fix to memory.
6. Recall the knowledge during future incidents.

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Environment Variables

Create a `.env` file:

```env
HINDSIGHT_API_KEY=hsk_7ed51910f8b36aeabeb92ac055213de3_f248ddddefc17775
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=opsmind-incidents
```

Never commit your `.env` file or expose API credentials.

## ⚠️ Disclaimer

OpsMind AI provides advisory recommendations. Engineers must verify fixes before applying them.

## 👩‍💻 Author

Emlyn M.
>>>>>>> 5c96cff1dd6769381863393c62ca0882aba7f0cd
