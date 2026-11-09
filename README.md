
# OpsMind AI 🧠

### Memory-Aware AI Incident Diagnosis and Resolution Assistant

OpsMind AI is an AI-powered IT operations assistant that helps engineers diagnose production incidents using historical incident knowledge.

## Features

- Incident reporting and classification
- AI-assisted root cause analysis
- Historical incident retrieval using Hindsight
- Reusable resolution knowledge
- Verified fix storage
- Memory-aware incident diagnosis

## Technology Stack

- Python
- Streamlit
- Hindsight AI
- REST API
- Git and GitHub

## Workflow

1. Report a production incident.
2. Retrieve relevant historical incidents.
3. Generate diagnosis and recommendations.
4. Engineer verifies the resolution.
5. Save the verified fix to memory.
6. Recall knowledge during future incidents.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Environment Configuration

Create a `.env` file containing:

```env
HINDSIGHT_API_KEY=your_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=opsmind-incidents
```

Never commit API keys or `.env` files.

## Disclaimer

OpsMind AI provides advisory recommendations. Engineers must verify fixes before applying them.

## Author

Emlyn M.
