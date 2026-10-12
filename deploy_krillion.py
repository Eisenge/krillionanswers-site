#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KrillionAnswers deploy script — uploads local site to Hostinger via FTPS.
Usage: python3 deploy_krillion.py [--dry-run]
Excludes: build_*.py, .secrets, __pycache__, .DS_Store

Credentials come from environment variables (never hard-code secrets):
  FTP_HOST, FTP_USER, FTP_PASS, FTP_ROOT (default /public_html)
"""
import ftplib
import os
import sys

LOCAL_ROOT = os.path.dirname(os.path.abspath(__file__))
HOST = os.environ.get("FTP_HOST", "")
USER = os.environ.get("FTP_USER", "")
PASS = os.environ.get("FTP_PASS", "")
REMOTE_ROOT = os.environ.get("FTP_ROOT", "/public_html")
EXCLUDE_DIRS = {".secrets", "__pycache__", ".git"}
EXCLUDE_FILES = {"build_krillion.py", "build_daily.py", "deploy_krillion.py"}


def should_skip_rel(rel):
    parts = rel.split("/")
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
    base = parts[-1]
    return base in EXCLUDE_FILES or base.endswith(".pyc") or base == ".DS_Store"


def walk_local():
    files = []
    for dirpath, dirnames, filenames in os.walk(LOCAL_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, LOCAL_ROOT)
            if not should_skip_rel(rel):
                files.append((full, rel.replace(os.sep, "/")))
    return files


def ensure_dir(ftp, path):
    """Recursively mkdir remote path if missing."""
    parts = [p for p in path.split("/") if p]
    cur = ""
    for p in parts:
        cur += "/" + p
        try:
            ftp.mkd(cur)
        except ftplib.error_perm as e:
            # 550 already exists is fine
            if "550" not in str(e):
                raise


def main():
    if not (HOST and USER and PASS):
        print("Missing FTP credentials (set FTP_HOST/FTP_USER/FTP_PASS env vars)")
        sys.exit(2)
    dry = "--dry-run" in sys.argv
    files = walk_local()
    print(f"Total files to deploy: {len(files)}")
    if dry:
        for _, rel in sorted(files, key=lambda x: x[1]):
            print("  " + rel)
        return

    ftp = ftplib.FTP_TLS()
    ftp.connect(HOST, 21, timeout=30)
    ftp.login(USER, PASS)
    ftp.prot_p()
    print("FTP login OK")

    ok, fail = 0, 0
    for full, rel in sorted(files, key=lambda x: x[1]):
        remote = REMOTE_ROOT + "/" + rel
        dirpath = os.path.dirname(remote)
        try:
            ensure_dir(ftp, dirpath)
            with open(full, "rb") as fh:
                ftp.storbinary(f"STOR {remote}", fh)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {rel}: {e}")
    ftp.quit()
    print(f"Deployed OK={ok} FAIL={fail}")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
