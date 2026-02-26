import sys
from studystats.analytics import show_stats
from studystats.storage import log_session

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py log <duration> <subject>")
        return

    command = sys.argv[1]

    if command == "log":
        duration = int(sys.argv[2])
        subject = sys.argv[3]
        log_session(duration, subject)
    
    elif command == "stats":
        show_stats()

if __name__ == "__main__":
    main()