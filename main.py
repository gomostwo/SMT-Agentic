"""Entry point for the SMT Agentic automation."""

from smt import login


def main():
    main_win = login(
        line="C20",
        station="Monitor",
        # Reads SMT_UID and SMT_PASSWORD from environment variables
    )
    if main_win:
        print("Logged in. Main window:", main_win.window_text())
    else:
        print("Login completed but main window not detected.")

    # Show me the next screen and I'll add more steps here!


if __name__ == "__main__":
    main()
