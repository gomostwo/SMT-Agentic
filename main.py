"""SMT Agentic — portable entry point.

Shows a config dialog, then runs the full automation in a background thread.
"""

import sys
import logging
import threading
from pathlib import Path

from ui.config_dialog import show_config_dialog
from smt import runner


def _log_path() -> Path:
    base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path.cwd()
    return base / "smt_agent.log"


logging.basicConfig(
    filename=str(_log_path()),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main() -> int:
    logging.info("=== SMT Agentic starting ===")

    selection = show_config_dialog()
    if selection is None:
        logging.info("User cancelled. Exit.")
        return 0

    params, password = selection
    logging.info("Config OK. line=%s station=%s uid=%s",
                 params["line"], params["station"], params["uid"])

    error_holder: dict = {}

    def worker():
        try:
            runner.run(params, password)
        except Exception as exc:  # noqa: BLE001
            logging.exception("Automation failed: %s", exc)
            error_holder["error"] = str(exc)

    thread = threading.Thread(target=worker, daemon=False)
    thread.start()
    thread.join()

    if "error" in error_holder:
        # Surface error via a final messagebox so the user knows it failed
        try:
            import tkinter as tk
            from tkinter import messagebox
            r = tk.Tk(); r.withdraw()
            messagebox.showerror("SMT Agentic — Failed", error_holder["error"])
            r.destroy()
        except Exception:
            pass
        return 1

    logging.info("=== SMT Agentic finished OK ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
