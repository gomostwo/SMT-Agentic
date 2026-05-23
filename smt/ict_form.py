"""Fill ICT Status form, refresh, click Report."""

import time
from pywinauto.keyboard import send_keys


def _select_combo(win, auto_id: str, fallback_title: str, value: str):
    if not value:
        return
    ctrl = win.child_window(auto_id=auto_id, control_type="ComboBox")
    if not ctrl.exists():
        ctrl = win.child_window(title=fallback_title, control_type="ComboBox")
    try:
        ctrl.select(value)
    except Exception:
        ctrl.click_input()
        send_keys(value, with_spaces=True)
        send_keys("{ENTER}")


def _set_edit(win, auto_id: str, value: str, found_index: int | None = None):
    if not value:
        return
    ctrl = win.child_window(auto_id=auto_id, control_type="Edit")
    if not ctrl.exists():
        if found_index is not None:
            ctrl = win.child_window(control_type="Edit", found_index=found_index)
        else:
            return
    try:
        ctrl.set_edit_text(value)
    except Exception:
        ctrl.click_input()
        send_keys("^a{DEL}" + value, with_spaces=True)


def _click_radio(win, title: str):
    try:
        win.child_window(title=title, control_type="RadioButton").click_input()
    except Exception:
        pass


def _set_checkbox(win, title: str, checked: bool):
    try:
        cb = win.child_window(title=title, control_type="CheckBox")
        state = cb.get_toggle_state()  # 0=unchecked, 1=checked
        if (state == 1) != checked:
            cb.click_input()
    except Exception:
        pass


def fill_ict_form(ict_win, params: dict):
    """Fill all ICT Status fields from the params dict."""
    # Dates and times
    _set_edit(ict_win, "dtDT1",  params.get("dt1_date", ""), found_index=0)
    _set_edit(ict_win, "txtT1",  params.get("dt1_time", ""), found_index=1)
    _set_edit(ict_win, "dtDT2",  params.get("dt2_date", ""), found_index=2)
    _set_edit(ict_win, "txtT2",  params.get("dt2_time", ""), found_index=3)

    # Dropdowns
    _select_combo(ict_win, "cboLine",    "Line",    params.get("line", ""))
    _select_combo(ict_win, "cboStation", "Station", params.get("station", ""))
    _select_combo(ict_win, "cboModel",   "Model",   params.get("model", ""))
    _select_combo(ict_win, "cboWO",      "WO",      params.get("wo", ""))
    _select_combo(ict_win, "cboFixNO",   "FixNO",   params.get("fixno", ""))

    # Radios
    _click_radio(ict_win, params.get("group_by", "ByModel"))
    _click_radio(ict_win, params.get("shift", "Day Shift"))

    # Checkbox
    _set_checkbox(ict_win, "ShowPassDetail", bool(params.get("show_pass_detail", False)))


def run_ict_query(ict_win, auto_report: bool = True):
    """Click RefreshStation -> RefreshData -> Report (if auto_report)."""
    ict_win.child_window(title="RefreshStation", control_type="Button").click_input()
    time.sleep(2.5)

    ict_win.child_window(title="RefreshData", control_type="Button").click_input()
    time.sleep(3.0)

    if auto_report:
        ict_win.child_window(title="Report", control_type="Button").click_input()
        time.sleep(2.0)
