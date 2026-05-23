"""Login flow for SMT Shop Floor Management System V3.4 PU9."""

import logging
import subprocess
import time
from pywinauto import Desktop


APP_TITLE = "SMT Shop Floor Management System"
CREDENTIAL_DIALOG_TITLE = "Login"
RTMS_TITLE = "Real Time Monitor"
LAUNCHER_TIMEOUT = 30   # Mainmenu.exe starts directly, no download needed


def find_window(title_re: str, timeout: int = 5):
    try:
        win = Desktop(backend="uia").window(title_re=title_re)
        win.wait("visible", timeout=timeout)
        return win
    except Exception:
        return None


def wait_for_window(title_re: str, timeout: int):
    """Poll for a window every second until it appears or timeout expires."""
    deadline = time.time() + timeout
    last_log = 0.0
    while time.time() < deadline:
        win = find_window(title_re, timeout=1)
        if win is not None:
            return win
        now = time.time()
        if now - last_log >= 5:
            remaining = int(deadline - now)
            logging.info("  waiting for window '%s'... (%ds left)", title_re, remaining)
            last_log = now
    return None


def launch_app(exe_path: str):
    # MainMenu_QMB.exe is a bootstrapper that downloads + extracts the real app
    # to D:\QMSApp\MainMenu_CSharp and then launches it. We fire-and-forget
    # with subprocess.Popen (Application.start() would fail with error 1471
    # because the bootstrapper exits before the real GUI appears).
    logging.info("Launching app: %s", exe_path)
    subprocess.Popen([exe_path], close_fds=True)


def _select_combo(win, auto_id: str, fallback_title: str, value: str):
    ctrl = win.child_window(auto_id=auto_id, control_type="ComboBox")
    if not ctrl.exists():
        ctrl = win.child_window(title=fallback_title, control_type="ComboBox")
    ctrl.select(value)


def step1_select_line_station(line: str, station: str, exe_path: str | None = None):
    """Select Line/Station and click Login on the first SMT dialog."""
    win = find_window(f".*{APP_TITLE}.*")
    if win is None:
        if not exe_path:
            raise RuntimeError("SMT window not found. Provide exe_path.")
        launch_app(exe_path)
        win = wait_for_window(f".*{APP_TITLE}.*", timeout=LAUNCHER_TIMEOUT)
        if win is None:
            raise RuntimeError(
                f"SMT window did not appear within {LAUNCHER_TIMEOUT}s. "
                "The bootstrapper may still be downloading — try again, or "
                "launch MainMenu_QMB.exe manually first and then run this tool."
            )

    _select_combo(win, "cboLine", "Line", line)
    _select_combo(win, "cboStation", "Station", station)

    win.child_window(title="Login", control_type="Button").click_input()
    time.sleep(1.5)


def step2_enter_credentials(uid: str, password: str):
    """Fill UID and Password in the credential dialog and click Login."""
    cred_win = find_window(CREDENTIAL_DIALOG_TITLE, timeout=10)
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
    line: str,
    station: str,
    uid: str,
    password: str,
    exe_path: str | None = None,
):
    """
    Full login flow:
      1. Select Line + Station -> click Login
      2. Enter UID + Password -> click Login
    Returns the RTMS main window handle.
    """
    if not uid or not password:
        raise RuntimeError("UID and password are required.")

    step1_select_line_station(line=line, station=station, exe_path=exe_path)
    step2_enter_credentials(uid=uid, password=password)

    main_win = find_window(f".*{RTMS_TITLE}.*", timeout=15)
    if main_win is None:
        main_win = find_window(f".*{APP_TITLE}.*", timeout=5)
    return main_win
