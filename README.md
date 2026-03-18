# JuryRigged

[![CI](https://github.com/PatrickFanella/jury-rigged/actions/workflows/ci.yml/badge.svg)](https://github.com/PatrickFanella/jury-rigged/actions/workflows/ci.yml)

JuryRigged is a real-time, multi-agent courtroom simulation built as a full-stack TypeScript portfolio project. It combines LLM-driven role orchestration, live event streaming, jury interaction, and an Ace Attorney-inspired presentation layer. The project is designed to showcase how I build interactive systems that balance technical ambition with product usability.

## Why this project stands out

- **Real-time system design:** Orchestrates judge, counsel, witness, and bailiff agents through deterministic trial phases
- **Full-stack delivery:** Combines an Express API, a React/Vite operator dashboard, and a PixiJS-based courtroom renderer
- **Interactive product thinking:** Supports live jury voting, audience-triggered actions, and streamed session updates over SSE
- **Operational maturity:** Includes Docker workflows, Postgres persistence, health metrics, CI automation, moderation controls, and replay tooling

## Tech stack

- **Backend:** Node.js, TypeScript, Express, Server-Sent Events
- **Frontend:** React, Vite, PixiJS, Tailwind CSS
- **Data & infrastructure:** PostgreSQL, Docker Compose, GitHub Actions
- **AI integration:** OpenRouter-powered agent dialogue with a deterministic mock mode for development without API keys

## What it demonstrates

This project showcases skills that translate directly to production engineering work:

- Architecting multi-service, stateful application flows
- Building responsive interfaces for both operators and end users
- Designing APIs for live updates and user interaction
- Balancing experimentation with reliability through testing, replay, and fallback paths

## Quick start

```bash
npm install
cp .env.example .env
npm run dev
```

After copying `.env`, you can leave `OPENROUTER_API_KEY` empty to use deterministic mock dialogue and leave `DATABASE_URL` empty to use in-memory storage.

Open `http://localhost:3000` for the main experience.
Build the operator dashboard with:

```bash
npm run build:dashboard
```

The operator dashboard is then available at `http://localhost:3000/operator`.

## Useful commands

```bash
npm run dev
npm run build
npm test
```

For containerized local development:

```bash
npm run docker:up
```

## Project highlights

- Deterministic courtroom phase progression from case prompt through final ruling
- Live per-session SSE streaming and jury vote endpoints
- Optional Postgres-backed persistence with in-memory fallback
- OBS broadcast hooks and Twitch audience command support
- NDJSON recording and replay for repeatable debugging and demos

## Documentation

- `docs/architecture.md` — system design and phase sequencing
- `docs/api.md` — REST and SSE contracts
- `docs/ADR-001-juryrigged-architecture.md` — architectural decisions
- `docs/operator-runbook.md` / `docs/ops-runbook.md` — operating guidance

JuryRigged demonstrates production-ready full-stack engineering across real-time backend coordination, polished frontend presentation, and operational tooling in one cohesive project.
