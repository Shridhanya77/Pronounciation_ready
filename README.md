# Livo AI – Pronunciation Assessment Web App

Livo AI is a production-ready web application that lets users upload a short English speech recording and receive pronunciation feedback including a pronunciation score, accuracy, fluency, completeness, transcript, highlighted mistakes, explanations, and improvement suggestions.

## Features

- Upload audio in WAV, MP3, or M4A format
- Validate file type, size, and duration
- Show upload progress and loading states
- Return pronunciation assessment results in a polished UI
- Support Azure Speech SDK when credentials are available
- Fall back to Whisper/GPT-style explanations when configured, otherwise use a transparent local fallback
- Responsive modern UI with support for dark mode

## Architecture Overview

The app uses:

- Frontend: React + Vite + Tailwind CSS + Axios
- Backend: Flask + Flask-CORS
- Speech processing: Azure Speech SDK preferred, fallback to Whisper/OpenAI when configured
- Deployment: Vercel for the frontend and Render for the backend

## Installation

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Frontend

```bash
cd frontend
npm install
```

## Environment Variables

Create a backend environment file with values such as:

```env
FLASK_DEBUG=True
OPENAI_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=
AZURE_SPEECH_ENDPOINT=
MAX_FILE_SIZE_BYTES=20971520
MIN_DURATION_SECONDS=30
MAX_DURATION_SECONDS=45
```

## Run Locally

### Backend

```bash
cd backend
python app.py
```

### Frontend

```bash
cd frontend
npm run dev
```

The frontend should point to the backend at http://localhost:5000.

## API Endpoints

- GET /health
- POST /api/assess

## Folder Structure

```text
backend/
  app.py
  config.py
  requirements.txt
  services/
    audio_validation.py
    speech_service.py
    pronunciation_service.py
    gpt_analysis.py
frontend/
  src/
    components/
    App.jsx
    main.jsx
```

## Deployment

- Frontend: deploy the frontend folder to Vercel
- Backend: deploy the backend folder to Render using the provided render.yaml

## Screenshots

Placeholder: add screenshots of the upload experience and assessment dashboard.

## Future Improvements

- Add waveform visualization
- Add PDF report export
- Add audio playback controls
- Add persistent history for assessments
