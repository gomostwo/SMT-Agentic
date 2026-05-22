"""Entry point for the SMT Agentic automation."""

import sys
import logging
from pathlib import Path
from smt import login

# Write log next to the .exe when running as bundled app
log_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(".")
logging.basicConfig(
    filename=str(log_dir / "smt_agent.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main():
    try:
        logging.info("Starting SMT login flow...")
        main_win = login(
            line="C20",
            station="Monitor",
            exe_path=r"C:\Users\T4060033\OneDrive - quantacn.com\Desktop\MainMenu_QMB.exe",
        )
        if main_win:
            logging.info("Login successful. Main window: %s", main_win.window_text())
        else:
            logging.warning("Login completed but main window not detected.")
    except Exception as exc:
        logging.error("Login failed: %s", exc)
        sys.exit(1)

    # Show me the next screen and I'll add more steps here!


if __name__ == "__main__":
    main()
