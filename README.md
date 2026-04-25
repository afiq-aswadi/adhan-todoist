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

By default, location is auto-detected from your public IP via
[ipapi.co](https://ipapi.co/), so just running the script does the right thing
wherever your laptop is:

```
uv run --env-file .env main.py
```

To override (e.g. on a server, or behind a VPN that misreports location):

```
uv run --env-file .env main.py --city Berkeley --country "United States"
uv run --env-file .env main.py --city Perth --country Australia --method 2
```

Calculation methods are listed at https://aladhan.com/calculation-methods.
Default is method 3 (Muslim World League). Pass `--project-id <id>` to file
tasks under a specific Todoist project instead of the Inbox.

## Scheduling (macOS launchd)

The repo includes `com.afiq.adhan-todoist.plist` — edit the paths to match your
machine, copy it into `~/Library/LaunchAgents/`, then load:

```
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.afiq.adhan-todoist.plist
```

It runs daily at 01:00 local time. If the laptop is asleep, the job fires on
next wake. To unload (e.g. before editing the plist):

```
launchctl bootout gui/$(id -u)/com.afiq.adhan-todoist
```

To force a run now (will create a duplicate set of today's tasks):

```
launchctl kickstart gui/$(id -u)/com.afiq.adhan-todoist
```

Logs go to `launchd.log` / `launchd.err.log` in the repo root.

Location follows your public IP automatically — fly to Berkeley and the next
day's run picks up the new city. No plist edits required unless you want to
hard-code an override.
