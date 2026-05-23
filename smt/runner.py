"""Orchestrator: glue login -> navigation -> form -> report."""

import logging
from .login import login
from .rtms import navigate_to_ict
from .ict_form import fill_ict_form, run_ict_query


def run(params: dict, password: str) -> None:
    """Run the full automation sequence with the given session parameters."""
    logging.info("Step 1/4: login")
    main_win = login(
        line=params["line"],
        station=params["station"],
        uid=params["uid"],
        password=password,
        exe_path=params.get("exe_path") or None,
    )
    if main_win is None:
        raise RuntimeError("Login completed but RTMS main window not detected.")
    logging.info("  RTMS window: %s", main_win.window_text())

    logging.info("Step 2/4: navigate ICT -> ICTMoniter")
    ict_win = navigate_to_ict(main_win)
    logging.info("  ICT Status window: %s", ict_win.window_text())

    logging.info("Step 3/4: fill ICT Status form")
    fill_ict_form(ict_win, params)

    logging.info("Step 4/4: RefreshStation -> RefreshData -> Report")
    run_ict_query(ict_win, auto_report=bool(params.get("auto_click_report", True)))

    logging.info("Done. Excel should open automatically.")
