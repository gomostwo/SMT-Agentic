# SMT Agentic

Portable Windows automation for the **SMT Shop Floor Management System V3.4 PU9** → **RTMS** → **ICT Monitor** → Excel report.

## Run (no install)
1. Download `smt_agent.exe` (from GitHub Actions artifacts, or build it yourself with `build.bat`).
2. Double-click it. A config dialog appears.
3. Fill the session parameters once — they are remembered for next time.
4. Click **▶ Run**.

The agent will:
1. Launch `MainMenu_QMB.exe`
2. Log in (Line / Station, then UID / Password)
3. Navigate **ICT → ICTMoniter**
4. Fill the ICT Status form with your parameters
5. Click **RefreshStation → RefreshData → Report**
6. Excel opens automatically with the data

Logs are written to `smt_agent.log` next to the `.exe`.

## Build from source (Windows)
```cmd
git clone <repo>
cd SMT-Agentic
build.bat
```
Output: `dist\smt_agent.exe`

## Project layout
```
main.py             Entry point
ui/config_dialog.py Session config GUI (tkinter)
smt/
  config.py         JSON params + keyring (Windows Credential Manager)
  login.py          Login dialog 1 + 2
  rtms.py           ICT menu → ICTMoniter
  ict_form.py       Fill ICT Status form + Refresh + Report
  runner.py         Orchestrator
smt_agent.spec      PyInstaller spec
build.bat           One-click build
.github/workflows/  CI auto-build
```
