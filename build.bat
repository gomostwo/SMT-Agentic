@echo off
:: Build portable smt_agent.exe — run this on your Windows machine
:: Requirements: pip install pyinstaller pywinauto pywin32 Pillow

echo [1/3] Installing build dependencies...
pip install pyinstaller pywinauto pywin32 Pillow --quiet

echo [2/3] Building portable .exe...
pyinstaller smt_agent.spec --clean

echo [3/3] Done!
echo.
echo Output: dist\smt_agent.exe
echo Log:    (same folder as .exe) smt_agent.log
echo.
echo Before running, set your credentials once:
echo   setx SMT_UID "T4060033"
echo   setx SMT_PASSWORD "your_password"
echo.
pause
