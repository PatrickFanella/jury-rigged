# JuryRigged

[![CI](https://github.com/PatrickFanella/jury-rigged/actions/workflows/ci.yml/badge.svg)](https://github.com/PatrickFanella/jury-rigged/actions/workflows/ci.yml)

JuryRigged is a real-time, multi-agent courtroom simulation built as a full-stack TypeScript portfolio project. It combines LLM-driven role orchestration, live event streaming, jury interaction, and an Ace Attorney–inspired presentation layer to show how I design interactive systems that are both technically ambitious and product-minded.

## Why this project stands out

- **Real-time system design:** orchestrates judge, counsel, witness, and bailiff agents through deterministic trial phases
- **Full-stack delivery:** Express API, React operator dashboard, and a PixiJS-based courtroom renderer
- **Interactive product thinking:** supports live jury voting, audience-triggered actions, and streamed session updates over SSE
- **Operational maturity:** includes Docker workflows, Postgres persistence, health metrics, CI automation, moderation controls, and replay tooling

## Tech stack

- **Backend:** Node.js, TypeScript, Express, Server-Sent Events
- **Frontend:** React, Vite, PixiJS, Tailwind CSS
- **Data & infrastructure:** PostgreSQL, Docker Compose, GitHub Actions
- **AI integration:** OpenRouter-powered agent dialogue with deterministic mock fallback

## What it demonstrates

This project showcases skills that translate directly to production engineering work:

- architecting multi-service, stateful application flows
- building responsive interfaces for both operators and end users
- designing APIs for live updates and user interaction
- balancing experimentation with reliability through testing, replay, and fallback paths

## Quick start

```bash
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:3000` for the main experience.  
Build the operator dashboard with:

```bash
npm run build:dashboard
```

The operator dashboard is then available at `http://localhost:3000/operator`.

If `OPENROUTER_API_KEY` is empty, the app uses deterministic mock dialogue.  
If `DATABASE_URL` is empty, it runs with in-memory storage.

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

- deterministic courtroom phase progression from case prompt through final ruling
- live per-session SSE streaming and jury vote endpoints
- optional Postgres-backed persistence with in-memory fallback
- OBS broadcast hooks and Twitch audience command support
- NDJSON recording and replay for repeatable debugging and demos

## Documentation

- `docs/architecture.md` — system design and phase sequencing
- `docs/api.md` — REST and SSE contracts
- `docs/ADR-001-juryrigged-architecture.md` — architectural decisions
- `docs/operator-runbook.md` / `docs/ops-runbook.md` — operating guidance

JuryRigged was built to demonstrate thoughtful full-stack engineering: real-time backend coordination, polished frontend presentation, and pragmatic operational tooling in one cohesive project.
