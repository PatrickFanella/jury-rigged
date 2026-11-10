# JuryRigged

JuryRigged is a courtroom drama played out live by language models. A judge,
prosecutor, defense, witnesses and a bailiff argue a case in fixed phases while
viewers watch, press witnesses, present evidence and vote on the verdict and
the sentence. It is built to run as a stream with a broadcast overlay and
Twitch chat commands.

It is in development (version `0.1.0`), and much of the art is placeholder.

## Features

- **Courtroom phases:** every session moves forward through
  `case_prompt` → `openings` → `witness_exam` → `evidence_reveal` →
  `closings` → `verdict_vote` → `sentence_vote` → `final_ruling`. The witness
  exam can be skipped straight to closings.
- **Case file:** each session starts with a fixed case context: charges, a
  witness roster and an evidence list.
- **Live stream of events:** each session publishes its dialogue and state over
  Server-Sent Events at `/api/court/sessions/:id/stream`.
- **Audience voting:** verdict and sentence polls with time windows, rate
  limits and duplicate-vote suppression.
- **Audience actions:** press a witness or present evidence through the API or
  Twitch chat.
- **Twitch chat bot:** `!vote`, `!sentence`, `!press`, `!present`,
  `!objection`, `!prompt`, `!case`, `!status` and `!help`. Without Twitch
  credentials the bot stays off.
- **Case queue:** viewers can submit cases from the public app or Twitch. The
  server runs queued cases first and generates new ones when the queue is
  empty.
- **Public app:** live view, broadcast overlay (`/app/?view=overlay`, for an
  OBS browser source), transcripts, case submission and an about page.
- **Courtroom stage:** the overlay shows the characters, a dialogue box and
  effects. The server sends camera, pose and effect cues alongside each line.
- **Operator dashboard** at `/operator`: start sessions, change phases, run the
  case queue, pause or resume automation, and read the model call log.
- **Recording and replay:** live sessions are written to NDJSON files and can
  be replayed at any speed through the same event stream.
- **Storage:** in memory by default, or PostgreSQL when `DATABASE_URL` is set.
  With PostgreSQL, sessions interrupted by a restart resume.
- **OBS adapter (stub):** `BROADCAST_PROVIDER=obs` logs the OBS commands it
  would make; it does not connect to OBS yet.
- **Metrics:** Prometheus metrics at `/api/metrics` (admin only).

## Quick start

You need Node.js 22.

```bash
npm install
cp .env.example .env
npm run build      # compiles the server and builds the public app and dashboard
npm run dev        # API and app on http://localhost:3000
```

To run with no model and no database, set `LLM_PROVIDER=mock` in `.env` and
clear `DATABASE_URL` (the example file points it at the Compose database). The
server then uses mock dialogue and keeps sessions in memory.

- Public app: `http://localhost:3000`
- Operator dashboard: `http://localhost:3000/operator`

For front-end work with hot reload, keep `npm run dev` running and start:

```bash
npm run dev:app        # public app on http://localhost:3002
npm run dev:dashboard  # operator dashboard on http://localhost:3001/operator/
```

`make run` starts the API and dashboard together. `make help` lists every
target.

### Tests

```bash
npm run lint   # TypeScript type check
npm test       # Node test runner
make ci        # lint, build and test
```

### Replay a recording

```bash
npm run dev -- --replay recordings/<SESSION_ID>.ndjson --speed 4
```

`REPLAY_FILE` and `REPLAY_SPEED` do the same through the environment. In
replay mode no new dialogue is generated.

## Configuration

Copy `.env.example` to `.env`. It documents every variable; the main groups:

| Group              | Variables                                                                                                                                                                                                                                                                                       |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Server             | `PORT`, `LOG_LEVEL`, `TRUST_PROXY`, `API_BIND_ADDR`, `API_HOST_PORT`                                                                                                                                                                                                                            |
| Database           | `DATABASE_URL`, `POSTGRES_PASSWORD` (Compose)                                                                                                                                                                                                                                                   |
| Language model     | `LLM_PROVIDER` (`llama-line` for an OpenAI-compatible endpoint, `openrouter` or `mock`), `OPENROUTER_API_KEY`, `LLM_MODEL`, `LLM_MODELS`, `LLM_MOCK`                                                                                                                                            |
| Local model        | `LLAMA_LINE_BASE_URL`, `LLAMA_LINE_API_KEY`, `LLAMA_LINE_MODEL` for any OpenAI-compatible chat endpoint such as Ollama. `OLLAMA_BASE_URL`, `OLLAMA_API_KEY` and `OLLAMA_MODEL` are read only when the matching `LLAMA_LINE_*` variable is unset, so remove those lines from `.env` to use them. |
| Model call log     | `LLM_AUDIT_ENABLED`, `LLM_AUDIT_BODY_PERSISTENCE` (`off`, `metadata`, `full`), `LLM_AUDIT_MAX_BODY_CHARS`, `LLM_AUDIT_RETENTION_DAYS`                                                                                                                                                           |
| Admin              | `ADMIN_PASSWORD` (turns on admin login), `ADMIN_TOKEN_SECRET`, `ADMIN_COOKIE_SECURE`                                                                                                                                                                                                            |
| Voting             | `VERDICT_VOTE_WINDOW_MS`, `SENTENCE_VOTE_WINDOW_MS`, `VOTE_SPAM_*`                                                                                                                                                                                                                              |
| Case automation    | `AUTO_GENERATE_CASES`, `AUTO_CASE_IDLE_DELAY_MS`, `CASE_QUEUE_POLL_MS`, `CASE_QUEUE_SUBMIT_TOKEN`, `SIMULATION_AUTOSTART`                                                                                                                                                                       |
| Public submissions | `TURNSTILE_SECRET_KEY` with `VITE_TURNSTILE_SITE_KEY` at build time, or `PUBLIC_QUEUE_ALLOW_NONCE_SUBMISSIONS=true`. Without one of these the public form reports that verification is not configured. `CASE_QUEUE_SUBMIT_TOKEN` authenticates the Twitch integration's submissions.            |
| Token budgets      | `WITNESS_MAX_TOKENS`, `WITNESS_MAX_SECONDS`, `JUDGE_RECAP_CADENCE`, `ROLE_MAX_TOKENS_*`, `TOKEN_COST_PER_1K_USD`                                                                                                                                                                                |
| Broadcast          | `TTS_PROVIDER` (`noop` or `mock`), `BROADCAST_PROVIDER` (`noop` or `obs`), `OBS_WEBSOCKET_URL`, `OBS_WEBSOCKET_PASSWORD`                                                                                                                                                                        |
| Recording          | `RECORDINGS_DIR`, `REPLAY_FILE`, `REPLAY_SPEED`                                                                                                                                                                                                                                                 |
| Twitch             | `TWITCH_CHANNEL`, `TWITCH_BOT_USERNAME`, `TWITCH_BOT_TOKEN`, `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`, `TWITCH_REFRESH_TOKEN`, `TWITCH_PROMPT_MIN_ROLE`                                                                                                                                       |

Set `ADMIN_PASSWORD` and a long random `ADMIN_TOKEN_SECRET` on any server
other people can reach; without them the operator routes are open.

## Deploy

`docker compose up --build` (or `npm run docker:up`) builds the image and runs
the API with PostgreSQL 16. Migrations run when the container starts. The API
listens on port `3001` inside the container and is published on
`127.0.0.1:3001` by default; change that with `API_BIND_ADDR` and
`API_HOST_PORT`. The Compose file also joins an external Docker network named
`monitoring`, so create it (`docker network create monitoring`) or remove it
from `docker-compose.yml`.

Put a reverse proxy with HTTPS in front, keep `TRUST_PROXY=1` so rate limits
see real client addresses, and set `ADMIN_COOKIE_SECURE=true`.

Without Docker: `npm run build`, `npm run migrate:dist`, then `npm start`.

## Project layout

```text
src/          server, courtroom orchestration, storage, moderation, LLM,
              Twitch, OBS, replay and tests
app/          public React app (live view, overlay, transcripts, submit)
dashboard/    operator dashboard (React + Vite)
public/       older standalone viewer, PixiJS renderer and placeholder
              assets (not served by the current server)
db/migrations SQL migrations
docs/         system overview and guides for contributors, operators,
              streamers and viewers
ops/          alert thresholds and dashboards
```

Start with [docs/01-system-overview.md](docs/01-system-overview.md) and
[docs/02-contributor-guide.md](docs/02-contributor-guide.md). The
[streamer guide](docs/04-streamer-guide.md) covers OBS setup.

## Contributing

- Report bugs and request features in [GitHub issues](https://github.com/subculture-collective/jury-rigged/issues).
- Ask questions and share ideas in [GitHub Discussions](https://github.com/subculture-collective/jury-rigged/discussions).
- Send code as a pull request on GitHub against `main`. CI runs the type
  check, build and tests on every pull request, and they must pass before it
  can merge.

## License

GNU General Public License, version 3 or later (`GPL-3.0-or-later`). See
[LICENSE](LICENSE).
