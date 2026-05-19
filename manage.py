"""
Glossa Lab project management entrypoint.

This file exists primarily so that specsmith's project-type auto-detection
correctly identifies this as a backend-frontend project. The actual backend
is in backend/ and is started via the tray or shell.cmd.

Usage:
  python manage.py help      -- show available commands
  python manage.py backend   -- start the backend (non-blocking)
"""
import sys


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "help":
        print(__doc__)
    elif cmd == "backend":
        import subprocess
        root = __file__ and __import__("pathlib").Path(__file__).parent
        subprocess.Popen(  # noqa: S603
            [sys.executable, "-m", "glossa_lab.run"],
            cwd=str(root / "backend"),
        )
    else:
        print(f"Unknown command: {cmd}. Run 'python manage.py help'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
