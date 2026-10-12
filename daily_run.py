#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Krillion daily auto-update runner.
1. Fetches krillion.io/api/today (resets ~UTC 04:00).
2. If /dive/<N>/ already exists locally -> skip (idempotent).
3. Otherwise: run build_daily.py (generates dive pages + sitemap), then
   deploy_krillion.py (FTPS upload to Hostinger).
Logs to logs/daily.log (rotate by date).
"""
import os
import subprocess
import sys
import datetime
import json
import urllib.request

DEPLOY = os.path.dirname(os.path.abspath(__file__))
API = "https://krillion.io/api/today"
LOG_DIR = os.path.join(DEPLOY, "logs")
LOG_FILE = os.path.join(LOG_DIR, "daily.log")


def log(msg):
    line = f"{datetime.datetime.now().isoformat()} {msg}"
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def fetch_day():
    req = urllib.request.Request(API, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/147.0 Safari/537.36",
        "Referer": "https://krillion.io/",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    try:
        day = fetch_day()
    except Exception as e:
        log(f"ERROR fetch API: {e}")
        sys.exit(1)

    n = day["dayNumber"]
    date = day["date"]
    log(f"API says dive #{n} ({date})")

    # idempotency: en dive dir is deploy/dive/<N>
    en_dir = os.path.join(DEPLOY, "dive", str(n))
    if os.path.isdir(en_dir):
        log(f"dive/{n} already built — skip")
        return

    log(f"building dive/{n} ...")
    r1 = subprocess.run([sys.executable, os.path.join(DEPLOY, "build_daily.py")],
                        capture_output=True, text=True)
    log("build_daily stdout: " + r1.stdout.strip().replace("\n", " | "))
    if r1.stderr.strip():
        log("build_daily stderr: " + r1.stderr.strip()[:500])
    if r1.returncode != 0:
        log("ERROR build_daily failed")
        sys.exit(1)

    log("injecting GA4 ...")
    r3 = subprocess.run([sys.executable, os.path.join(DEPLOY, "inject_ga.py")],
                        capture_output=True, text=True)
    log("inject stdout: " + r3.stdout.strip().replace("\n", " | "))
    if r3.stderr.strip():
        log("inject stderr: " + r3.stderr.strip()[:500])

    log("deploying ...")
    r2 = subprocess.run([sys.executable, os.path.join(DEPLOY, "deploy_krillion.py")],
                        capture_output=True, text=True)
    log("deploy stdout: " + r2.stdout.strip().replace("\n", " | "))
    if r2.stderr.strip():
        log("deploy stderr: " + r2.stderr.strip()[:500])
    if r2.returncode != 0:
        log("ERROR deploy failed")
        sys.exit(1)

    log(f"DONE dive/{n} published")


if __name__ == "__main__":
    main()
