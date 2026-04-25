import os
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import tyro

ALADHAN_URL = "https://api.aladhan.com/v1/timingsByCity"
TODOIST_URL = "https://api.todoist.com/api/v1/tasks"
PRAYERS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]


@dataclass
class Config:
    city: str = "Melbourne"
    country: str = "Australia"
    method: int = 3  # 3 = Muslim World League. see https://aladhan.com/calculation-methods
    project_id: str | None = None


def fetch_timings(city: str, country: str, method: int) -> tuple[dict[str, str], str]:
    today = datetime.now().strftime("%d-%m-%Y")
    response = requests.get(
        ALADHAN_URL,
        params={"city": city, "country": country, "method": method, "date": today},
    )
    response.raise_for_status()
    data = response.json()["data"]
    return data["timings"], data["meta"]["timezone"]


def create_task(token: str, name: str, due_datetime: str, project_id: str | None) -> None:
    body = {"content": name, "due_datetime": due_datetime}
    if project_id is not None:
        body["project_id"] = project_id
    response = requests.post(
        TODOIST_URL,
        headers={"Authorization": f"Bearer {token}"},
        json=body,
    )
    response.raise_for_status()


def main(config: Config) -> None:
    token = os.environ["TODOIST_API_TOKEN"]
    timings, timezone_name = fetch_timings(config.city, config.country, config.method)
    tz = ZoneInfo(timezone_name)
    today = datetime.now(tz).date()
    for prayer in PRAYERS:
        # aladhan returns "HH:MM" or "HH:MM (TZ)" - take first token
        time_str = timings[prayer].split()[0]
        hour, minute = map(int, time_str.split(":"))
        local_dt = datetime(today.year, today.month, today.day, hour, minute, tzinfo=tz)
        due_datetime = local_dt.isoformat()
        create_task(token, prayer, due_datetime, config.project_id)
        print(f"{prayer}: {due_datetime}")


if __name__ == "__main__":
    main(tyro.cli(Config))
