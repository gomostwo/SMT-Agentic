"""
Windows background service wrapper for SMT Agentic automation.

Install:   python service.py install
Start:     python service.py start
Stop:      python service.py stop
Remove:    python service.py remove
Debug run: python service.py debug
"""

import sys
import time
import logging
import servicemanager
import win32event
import win32service
import win32serviceutil

from smt import login

LOG_FILE = r"C:\SMT-Agentic\smt_agent.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class SMTAgentService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SMTAgentService"
    _svc_display_name_ = "SMT Shop Floor Agent"
    _svc_description_ = "Automates login and monitoring for SMT Shop Floor Management System."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        logging.info("Service stop requested.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        logging.info("SMT Agent service started.")
        self.main()

    def main(self):
        try:
            logging.info("Starting SMT login flow...")
            main_win = login(
                line="C20",
                station="Monitor",
                # Credentials come from environment variables:
                #   SMT_UID and SMT_PASSWORD
                # Set them via: setx SMT_UID "T4060033" /M
                #               setx SMT_PASSWORD "yourpassword" /M
            )
            if main_win:
                logging.info("Login successful. Main window: %s", main_win.window_text())
            else:
                logging.warning("Login completed but main window not detected.")
        except Exception as exc:
            logging.error("Login failed: %s", exc)

        # Keep service alive; extend here with monitoring loop
        while self.running:
            rc = win32event.WaitForSingleObject(self.stop_event, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break

        logging.info("SMT Agent service stopped.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SMTAgentService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SMTAgentService)
