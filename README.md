# adhan-todoist

Push the five daily Islamic prayer times into Todoist as dated, tickable tasks.
Location-aware via the [Aladhan API](https://aladhan.com/prayer-times-api).

## Setup

Requires [`uv`](https://docs.astral.sh/uv/).

```
uv sync
```

Get a Todoist API token from Todoist Settings → Integrations → Developer.
Either export it in your shell:

```
export TODOIST_API_TOKEN="..."
```

…or put it in a `.env` file at the repo root and pass `--env-file .env` to `uv run`:

```
TODOIST_API_TOKEN=...
```

## Usage

Run once per day (before Fajr) for the location you're in:

```
uv run --env-file .env main.py --city Melbourne --country Australia
uv run --env-file .env main.py --city Berkeley --country "United States"
uv run --env-file .env main.py --city Perth --country Australia --method 2
```

Calculation methods are listed at https://aladhan.com/calculation-methods.
Default is method 3 (Muslim World League). Pass `--project-id <id>` to file
tasks under a specific Todoist project instead of the Inbox.

## Scheduling

Either a local cron entry or a GitHub Actions schedule. Switching locations
just means changing the `--city` / `--country` flags in your scheduler.
