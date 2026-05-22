"""Login flow for SMT Shop Floor Management System V3.4 PU9."""

import os
import time
from pywinauto import Application, Desktop


APP_TITLE = "SMT Shop Floor Management System"
CREDENTIAL_DIALOG_TITLE = "Login"


def find_window(title_re: str, timeout: int = 5):
    try:
        win = Desktop(backend="uia").window(title_re=title_re)
        win.wait("visible", timeout=timeout)
        return win
    except Exception:
        return None


def launch_app(exe_path: str):
    app = Application(backend="uia").start(exe_path)
    time.sleep(2)
    return app


def _select_combo(win, auto_id: str, fallback_title: str, value: str):
    ctrl = win.child_window(auto_id=auto_id, control_type="ComboBox")
    if not ctrl.exists():
        ctrl = win.child_window(title=fallback_title, control_type="ComboBox")
    ctrl.select(value)


def step1_select_line_station(
    line: str = "C20",
    station: str = "Monitor",
    exe_path: str | None = None,
):
    """Select Line/Station and click Login on the first SMT dialog."""
    win = find_window(f".*{APP_TITLE}.*")

    if win is None:
        if exe_path is None:
            raise RuntimeError(
                "SMT window not found. Provide exe_path to launch the app."
            )
        launch_app(exe_path)
        win = find_window(f".*{APP_TITLE}.*", timeout=10)
        if win is None:
            raise RuntimeError("SMT window did not appear after launch.")

    _select_combo(win, "cboLine", "Line", line)
    _select_combo(win, "cboStation", "Station", station)

    win.child_window(title="Login", control_type="Button").click_input()
    time.sleep(1.5)


def step2_enter_credentials(uid: str, password: str):
    """Fill UID and Password in the credential dialog and click Login."""
    cred_win = find_window(CREDENTIAL_DIALOG_TITLE, timeout=8)
    if cred_win is None:
        raise RuntimeError("Credential dialog did not appear.")

    uid_field = cred_win.child_window(auto_id="txtUID", control_type="Edit")
    if not uid_field.exists():
        uid_field = cred_win.child_window(control_type="Edit", found_index=0)
    uid_field.set_edit_text(uid)

    pwd_field = cred_win.child_window(auto_id="txtPassword", control_type="Edit")
    if not pwd_field.exists():
        pwd_field = cred_win.child_window(control_type="Edit", found_index=1)
    pwd_field.set_edit_text(password)

    cred_win.child_window(title="Login", control_type="Button").click_input()
    time.sleep(2)


def login(
    line: str = "C20",
    station: str = "Monitor",
    uid: str | None = None,
    password: str | None = None,
    exe_path: str | None = None,
):
    """
    Full login flow:
      1. Select Line + Station → click Login
      2. Enter UID + Password → click Login

    Credentials are read from SMT_UID / SMT_PASSWORD env vars if not passed directly.
    """
    uid = uid or os.environ.get("SMT_UID")
    password = password or os.environ.get("SMT_PASSWORD")

    if not uid or not password:
        raise RuntimeError(
            "UID and password are required. Pass them directly or set "
            "SMT_UID and SMT_PASSWORD environment variables."
        )

    step1_select_line_station(line=line, station=station, exe_path=exe_path)
    step2_enter_credentials(uid=uid, password=password)

    main_win = find_window(f".*{APP_TITLE}.*", timeout=10)
    return main_win
