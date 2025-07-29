#!/usr/bin/env python3
import asyncio
import sys
from printer_guard import PrintGuard


def main() -> None:
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "print_guard_db"
    }

    pg = PrintGuard(config)
    asyncio.run(pg.execute_command(sys.argv[1:]))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOpération annulée par l'utilisateur")
        sys.exit(1)