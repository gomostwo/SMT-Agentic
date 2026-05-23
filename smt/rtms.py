"""RTMS navigation: click ICT menu -> ICTMoniter, return ICT Status window."""

import time
from pywinauto import Desktop
from pywinauto.keyboard import send_keys


def navigate_to_ict(main_win):
    """Open ICT -> ICTMoniter from the RTMS main window menu bar."""
    try:
        menu = main_win.child_window(control_type="MenuBar")
        ict_menu = menu.child_window(title="ICT", control_type="MenuItem")
        ict_menu.click_input()
        time.sleep(0.4)
    except Exception:
        # Fallback: use Alt+I accelerator
        main_win.set_focus()
        send_keys("%I")
        time.sleep(0.4)

    # Submenu item (the typo "ICTMoniter" is intentional — matches the app)
    try:
        item = Desktop(backend="uia").window(
            title="ICTMoniter", control_type="MenuItem"
        )
        item.wait("visible", timeout=3)
        item.click_input()
    except Exception:
        send_keys("{ENTER}")

    time.sleep(1.5)

    ict_win = _find_ict_status_window()
    if ict_win is None:
        raise RuntimeError("ICT Status window did not appear.")
    return ict_win


def _find_ict_status_window():
    try:
        win = Desktop(backend="uia").window(title_re=".*ICT Status.*")
        win.wait("visible", timeout=10)
        return win
    except Exception:
        return None
