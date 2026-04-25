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
uv run --env-file .env main.py --city Istanbul --country Turkey
uv run --env-file .env main.py --city "Kuala Lumpur" --country Malaysia --method 2
```

Calculation methods are listed at https://aladhan.com/calculation-methods.
Default is method 3 (Muslim World League). Pass `--project-id <id>` to file
tasks under a specific Todoist project instead of the Inbox.

## Scheduling (macOS launchd)

`install.sh` substitutes your repo path and `uv` location into
`adhan-todoist.plist.template` and loads the agent under the label
`local.adhan-todoist`:

```
./install.sh
```

It runs daily at 01:00 local time. If the laptop is asleep, the job fires on
next wake. Re-running `install.sh` reloads cleanly. To uninstall:

```
launchctl bootout gui/$(id -u)/local.adhan-todoist
rm ~/Library/LaunchAgents/local.adhan-todoist.plist
```

To force a run now (creates a duplicate set of today's tasks):

```
launchctl kickstart gui/$(id -u)/local.adhan-todoist
```

Logs go to `launchd.log` / `launchd.err.log` in the repo root.

Location follows your public IP automatically — fly to a new city and the next
day's run picks it up. Override via `--city` / `--country` in the plist
template if you need to (e.g. behind a foreign-exit VPN).
