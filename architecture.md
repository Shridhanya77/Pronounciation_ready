# Architecture Overview

## System Diagram

```text
User Browser
  -> React/Vite frontend
  -> Axios upload request
  -> Flask API
  -> Audio validation service
  -> Speech engine (Azure preferred, Whisper fallback)
  -> Explanation layer (GPT when configured)
  -> JSON response
  -> Result UI
```

## Request Flow

1. The user uploads an audio file through the React interface.
2. The frontend sends the file to the Flask backend through a multipart upload request.
3. The backend validates the file type, size, and duration.
4. If valid, the audio is processed by the speech engine.
5. The result is enriched with explanation and improvement suggestions.
6. The frontend renders the scorecard, transcript, mistakes, and tips.

## Frontend

The frontend is a Vite React application with Tailwind CSS. It provides a modern upload experience, progress feedback, dark mode support, and a responsive results dashboard. The UI is designed to feel like a polished assessment experience rather than a basic form.

## Backend

The backend is a Flask service with modular services for validation, speech analysis, pronunciation scoring, and explanation generation. The API is stateless and does not require user accounts. Temporary files are created for validation and deleted after assessment.

## Speech Engine

The preferred speech engine is Azure AI Speech Pronunciation Assessment. If Azure credentials are available, the backend uses that path. When Azure is not configured, the app uses an optional Whisper transcription flow if OpenAI credentials are present. If neither is configured, the app uses a transparent local fallback that generates a heuristic assessment and clearly marks it as a fallback. This avoids pretending that the app can produce a high-confidence pronunciation score without a proper speech engine.

## LLM

GPT is used only for explanation and coaching. The app does not rely on GPT to estimate pronunciation from transcript alone; the system uses audio information and confidence signals from the speech stack as its primary signal.

## Deployment

The frontend is ready to deploy to Vercel. The backend is structured for Render using the provided Render configuration. Environment variables should be stored securely and injected at deployment time.

## Scoring Methodology

The application returns a simple scoring model with overall, accuracy, fluency, and completeness values. The exact score is derived from the configured speech engine. In fallback mode, a heuristic score is produced so the workflow remains functional without external services.

## Trade-offs

- Azure provides stronger pronunciation analysis but requires credentials.
- Whisper and GPT provide a flexible fallback but should be treated as an assistive layer rather than a definitive pronunciation judge.
- Local fallback scoring is useful for demos and local testing but should not be used as a production-grade pronunciation benchmark.

## Future Improvements

- Add waveform visualization and playback
- Integrate real-time pronunciation scoring
- Add PDF export and report history
- Improve confidence-based word-level remediation
