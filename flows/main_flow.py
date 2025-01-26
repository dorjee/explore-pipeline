import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from prefect import flow, task

sys.path.append(str(Path(__file__).parent.parent))
from utils.email_notifier import send_email_notification

# Load environment variables
load_dotenv()

# Email configuration from environment
EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER"),
    "sender": os.getenv("SENDER_EMAIL"),
    "recipients": os.getenv("RECIPIENT_EMAILS", "").split(","),
}

# Path configuration
PATHS = {
    "raw_data": os.getenv("RAW_DATA_PATH"),
    "result_db": os.getenv("RESULT_DB_PATH"),
    "filtered_db": os.getenv("FILTERED_DB_PATH"),
    "final_csv": os.getenv("FINAL_CSV_PATH"),
}


@task
def run_command(cmd: list) -> None:
    subprocess.run(cmd, check=True)


@flow(name="eXplore Virtual Library Pipeline")
def main_flow(start_from: Optional[str] = None) -> None:
    tasks = {
        "db_scan": lambda: run_command(
            [
                sys.executable,
                "tasks/db_scan.py",
                "-i",
                PATHS["raw_data"],
                "-o",
                PATHS["result_db"],
                "-f",
                "1",
            ]
        ),
        "filter": lambda: run_command(
            [
                sys.executable,
                "tasks/filter.py",
                # "-i",
                # PATHS["result_db"],
                # "-o",
                # PATHS["filtered_db"],
                # "-c",
                # "200",
            ]
        ),
        "enumeration": lambda: run_command(["bash", "tasks/run_enumeration.sh"]),
        "create_csv": lambda: run_command(
            [
                sys.executable,
                "tasks/create_final_csv.py",
                # "-i",
                # PATHS["filtered_db"],
                # "-o",
                # PATHS["final_csv"],
            ]
        ),
    }

    started = False if start_from else True
    for task_name, task_fn in tasks.items():
        if task_name == start_from:
            started = True
        if started:
            task_fn()

    send_email_notification(
        "Workflow Completed",
        "Data processing pipeline completed successfully.",
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-from", choices=["db_scan", "filter", "enumeration", "create_csv"]
    )
    args = parser.parse_args()
    main_flow(args.start_from)
