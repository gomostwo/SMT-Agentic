@echo off
:: Build portable smt_agent.exe on Windows
:: One-time:  pip install -r requirements.txt

echo [1/3] Installing dependencies...
pip install -r requirements.txt --quiet

echo [2/3] Building portable .exe...
pyinstaller smt_agent.spec --clean --noconfirm

echo [3/3] Done!
echo.
echo Output: dist\smt_agent.exe
echo Run it: double-click smt_agent.exe (no install needed)
echo Log:    smt_agent.log (created next to the .exe on first run)
echo.
pause
