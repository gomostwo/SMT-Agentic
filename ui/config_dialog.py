"""tkinter session configuration dialog."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from smt import config as cfg_mod


PAD_X = 12
PAD_Y = 6
ACCENT = "#2D5FA0"
GREEN_BG = "#DCF5DC"
GREEN_FG = "#1E6E1E"


def show_config_dialog() -> tuple[dict, str] | None:
    """
    Show the session config dialog.
    Returns (params_dict, password) when user clicks Run, or None on Cancel.
    """
    root = tk.Tk()
    root.title("SMT Agentic  —  Session Configuration")
    root.configure(bg="#F0F0F5")
    root.geometry("620x780")
    root.resizable(False, False)

    cfg = cfg_mod.load_config()
    stored_pwd = cfg_mod.get_password(cfg.get("uid", "")) or ""
    result = {"submitted": False}

    # ── Build UI ─────────────────────────────────────────────────────────────
    container = tk.Frame(root, bg="#F0F0F5")
    container.pack(fill="both", expand=True, padx=PAD_X, pady=PAD_Y)

    def section(title):
        lbl = tk.Label(container, text=f"  {title}", bg="#D2DCEB", fg=ACCENT,
                       font=("Segoe UI", 9, "bold"), anchor="w")
        lbl.pack(fill="x", pady=(8, 4))

    def row():
        f = tk.Frame(container, bg="#F0F0F5")
        f.pack(fill="x", pady=2)
        return f

    # ── APPLICATION ─────────────────────────────────────────────────────────
    section("APPLICATION")
    r = row()
    tk.Label(r, text="EXE Path", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    exe_var = tk.StringVar(value=cfg.get("exe_path", ""))
    tk.Entry(r, textvariable=exe_var, width=58).pack(side="left", padx=4)

    def browse():
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if path:
            exe_var.set(path)
    tk.Button(r, text="Browse…", command=browse).pack(side="left")

    # ── CREDENTIALS ─────────────────────────────────────────────────────────
    section("CREDENTIALS")
    r = row()
    tk.Label(r, text="UID", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    uid_var = tk.StringVar(value=cfg.get("uid", ""))
    tk.Entry(r, textvariable=uid_var, width=24).pack(side="left", padx=4)
    tk.Label(r, text="Password", bg="#F0F0F5", width=10, anchor="w").pack(side="left", padx=(20,0))
    pwd_var = tk.StringVar(value=stored_pwd)
    tk.Entry(r, textvariable=pwd_var, show="●", width=24).pack(side="left", padx=4)

    # ── LINE SETUP ──────────────────────────────────────────────────────────
    section("LINE SETUP")
    r = row()
    tk.Label(r, text="Line", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    line_var = tk.StringVar(value=cfg.get("line", "C20"))
    tk.Entry(r, textvariable=line_var, width=24).pack(side="left", padx=4)
    tk.Label(r, text="Station", bg="#F0F0F5", width=10, anchor="w").pack(side="left", padx=(20,0))
    station_var = tk.StringVar(value=cfg.get("station", "Monitor"))
    tk.Entry(r, textvariable=station_var, width=24).pack(side="left", padx=4)

    # ── ICT PARAMETERS ──────────────────────────────────────────────────────
    section("ICT PARAMETERS")
    r = row()
    tk.Label(r, text="DT1 (From)", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    dt1_date = tk.StringVar(value=cfg.get("dt1_date", ""))
    dt1_time = tk.StringVar(value=cfg.get("dt1_time", "0800"))
    tk.Entry(r, textvariable=dt1_date, width=14).pack(side="left", padx=4)
    tk.Entry(r, textvariable=dt1_time, width=8).pack(side="left", padx=2)
    tk.Label(r, text="DT2 (To)", bg="#F0F0F5", width=10, anchor="w").pack(side="left", padx=(12,0))
    dt2_date = tk.StringVar(value=cfg.get("dt2_date", ""))
    dt2_time = tk.StringVar(value=cfg.get("dt2_time", "2000"))
    tk.Entry(r, textvariable=dt2_date, width=14).pack(side="left", padx=4)
    tk.Entry(r, textvariable=dt2_time, width=8).pack(side="left", padx=2)

    r = row()
    tk.Label(r, text="Model", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    model_var = tk.StringVar(value=cfg.get("model", ""))
    tk.Entry(r, textvariable=model_var, width=24).pack(side="left", padx=4)
    tk.Label(r, text="WO", bg="#F0F0F5", width=10, anchor="w").pack(side="left", padx=(20,0))
    wo_var = tk.StringVar(value=cfg.get("wo", ""))
    tk.Entry(r, textvariable=wo_var, width=24).pack(side="left", padx=4)

    r = row()
    tk.Label(r, text="FixNO", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    fixno_var = tk.StringVar(value=cfg.get("fixno", ""))
    tk.Entry(r, textvariable=fixno_var, width=24).pack(side="left", padx=4)

    # ── OPTIONS ─────────────────────────────────────────────────────────────
    section("OPTIONS")
    r = row()
    tk.Label(r, text="Group by", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    group_var = tk.StringVar(value=cfg.get("group_by", "ByModel"))
    tk.Radiobutton(r, text="ByModel", variable=group_var, value="ByModel", bg="#F0F0F5").pack(side="left")
    tk.Radiobutton(r, text="ByWO",    variable=group_var, value="ByWO",    bg="#F0F0F5").pack(side="left")
    show_pass = tk.BooleanVar(value=bool(cfg.get("show_pass_detail", False)))
    tk.Checkbutton(r, text="ShowPassDetail", variable=show_pass, bg="#F0F0F5").pack(side="left", padx=20)

    r = row()
    tk.Label(r, text="Shift", bg="#F0F0F5", width=10, anchor="w").pack(side="left")
    shift_var = tk.StringVar(value=cfg.get("shift", "Day Shift"))
    for s in ("Day Shift", "Middle Shift", "Night Shift"):
        tk.Radiobutton(r, text=s, variable=shift_var, value=s, bg="#F0F0F5").pack(side="left")

    # ── OUTPUT ──────────────────────────────────────────────────────────────
    section("OUTPUT")
    info = tk.Frame(container, bg=GREEN_BG, bd=1, relief="solid")
    info.pack(fill="x", pady=4)
    tk.Label(info, text="📊  Report → Excel", bg=GREEN_BG, fg=GREEN_FG,
             font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=8, pady=(4,0))
    tk.Label(info, text="Clicking Report opens Excel automatically with the ICT data.",
             bg=GREEN_BG, fg=GREEN_FG, font=("Segoe UI", 8)).pack(anchor="w", padx=8, pady=(0,4))

    auto_report = tk.BooleanVar(value=bool(cfg.get("auto_click_report", True)))
    keep_excel  = tk.BooleanVar(value=bool(cfg.get("keep_excel_open", True)))
    tk.Checkbutton(container, text="Auto-click Report after RefreshData", variable=auto_report,
                   bg="#F0F0F5").pack(anchor="w")
    tk.Checkbutton(container, text="Keep Excel open after export", variable=keep_excel,
                   bg="#F0F0F5").pack(anchor="w")

    # ── Bottom bar ──────────────────────────────────────────────────────────
    bottom = tk.Frame(root, bg="#E1E4EB", height=58)
    bottom.pack(fill="x", side="bottom")
    remember = tk.BooleanVar(value=bool(cfg.get("remember_settings", True)))
    tk.Checkbutton(bottom, text="Remember settings for next session",
                   variable=remember, bg="#E1E4EB").pack(side="left", padx=14, pady=14)

    def on_run():
        if not exe_var.get().strip():
            messagebox.showerror("Missing field", "EXE Path is required.")
            return
        if not uid_var.get().strip() or not pwd_var.get():
            messagebox.showerror("Missing field", "UID and Password are required.")
            return
        result["submitted"] = True
        root.destroy()

    def on_cancel():
        root.destroy()

    tk.Button(bottom, text="Cancel", command=on_cancel, width=12).pack(side="right", padx=8, pady=12)
    tk.Button(bottom, text="▶  Run", command=on_run, width=14,
              bg="#22AA22", fg="white", font=("Segoe UI", 10, "bold")).pack(side="right", pady=12)

    root.mainloop()

    if not result["submitted"]:
        return None

    params = {
        "exe_path": exe_var.get().strip(),
        "uid": uid_var.get().strip(),
        "line": line_var.get().strip(),
        "station": station_var.get().strip(),
        "dt1_date": dt1_date.get().strip(),
        "dt1_time": dt1_time.get().strip(),
        "dt2_date": dt2_date.get().strip(),
        "dt2_time": dt2_time.get().strip(),
        "model": model_var.get().strip(),
        "wo": wo_var.get().strip(),
        "fixno": fixno_var.get().strip(),
        "group_by": group_var.get(),
        "show_pass_detail": bool(show_pass.get()),
        "shift": shift_var.get(),
        "auto_click_report": bool(auto_report.get()),
        "keep_excel_open": bool(keep_excel.get()),
        "remember_settings": bool(remember.get()),
    }
    password = pwd_var.get()

    if params["remember_settings"]:
        cfg_mod.save_config(params)
        cfg_mod.set_password(params["uid"], password)

    return params, password
