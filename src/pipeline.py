import logging
import os
import smtplib
import time
from email.message import EmailMessage

import schedule

from src.extract import extract
from src.transform import transform
from src.loader import load

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("pipeline")


def send_email(subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ["ALERT_FROM"]
    msg["To"] = os.environ["ALERT_TO"]
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["ALERT_FROM"], os.environ["GMAIL_APP_PASSWORD"])
        server.send_message(msg)


def run_pipeline() -> None:
    log.info("Pipeline started")
    try:
        raw = extract()
        log.info("Extracted %d rows", len(raw))

        clean = transform(raw)
        log.info("Transformed %d rows", len(clean))

        loaded = load(clean)
        log.info("Loaded %d rows", loaded)

        summary = (
            "Pipeline completed successfully.\n"
            f"Extracted: {len(raw)}\n"
            f"Transformed: {len(clean)}\n"
            f"Loaded: {loaded}"
        )
        log.info("Pipeline finished OK")
        _try_email("ETL Pipeline: SUCCESS", summary)
    except Exception as exc:
        log.exception("Pipeline failed")
        _try_email("ETL Pipeline: FAILED", f"Error: {exc}\nCheck logs/pipeline.log")


def _try_email(subject: str, body: str) -> None:
    """Send email if credentials are set. Never crash the pipeline because of email."""
    if "GMAIL_APP_PASSWORD" not in os.environ:
        log.info("Email skipped (no credentials set)")
        return
    try:
        send_email(subject, body)
        log.info("Email sent: %s", subject)
    except Exception:
        log.exception("Could not send email")


if __name__ == "__main__":
    # Testing ke liye: har 1 minute. Baad mein daily schedule use karein.
           schedule.every().day.at("09:00").do(run_pipeline)
    log.info("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(10)