"""Configuration: JSON params + Windows Credential Manager for password."""

import json
import sys
from pathlib import Path

try:
    import keyring
except ImportError:
    keyring = None

KEYRING_SERVICE = "SMT_Agentic"

DEFAULT_CONFIG = {
    "exe_path": r"D:\QMSApp\MainMenu_CSharp\Mainmenu.exe",
    "uid": "",
    "line": "C20",
    "station": "Monitor",
    "dt1_date": "",
    "dt1_time": "0800",
    "dt2_date": "",
    "dt2_time": "2000",
    "model": "",
    "wo": "",
    "fixno": "",
    "group_by": "ByModel",
    "show_pass_detail": False,
    "shift": "Day Shift",
    "auto_click_report": True,
    "keep_excel_open": True,
    "remember_settings": True,
}


def _config_path() -> Path:
    """Return path to smt_config.json next to the .exe (or CWD in dev)."""
    base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path.cwd()
    return base / "smt_config.json"


def load_config() -> dict:
    cfg_path = _config_path()
    if not cfg_path.exists():
        return dict(DEFAULT_CONFIG)
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)
    merged = dict(DEFAULT_CONFIG)
    merged.update(data)
    # If the stored exe_path no longer exists on disk, fall back to default
    # so the user sees the suggested path in the dialog instead of a dead one.
    import os
    if merged.get("exe_path") and not os.path.isfile(merged["exe_path"]):
        merged["exe_path"] = DEFAULT_CONFIG["exe_path"]
    return merged


def save_config(cfg: dict) -> None:
    cfg = {k: v for k, v in cfg.items() if k != "password"}
    _config_path().write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def get_password(uid: str) -> str | None:
    if not keyring or not uid:
        return None
    try:
        return keyring.get_password(KEYRING_SERVICE, uid)
    except Exception:
        return None


def set_password(uid: str, password: str) -> None:
    if not keyring or not uid or not password:
        return
    try:
        keyring.set_password(KEYRING_SERVICE, uid, password)
    except Exception:
        pass
