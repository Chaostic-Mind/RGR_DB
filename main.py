import sys
from controllers.main_controller import run_app

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print("\nПрограму перервано користувачем. Завершення...")
        sys.exit(0)