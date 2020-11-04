import sys
from main import AppManager


class CLIManager:
    def __init__(self):
        self.app = AppManager()

    def run(self):
        while True:
            inp = sys.stdin.readline()
            if inp == 'camera':
                self.app.load_from_camera()
            elif inp == 'auth':
                self.app.authenticate()
            elif inp == 'file':
                self.app.load_from_file()
            elif inp == 'q':
                break


if __name__ == '__main__':
    cli_manager = CLIManager()
    cli_manager.run()