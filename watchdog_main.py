import os
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, directory):
        self.observer = Observer()
        self.directory = directory

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                print("Observing")
                time.sleep(5)
        except:
            self.observer.stop()
            print("Stop. Exiting...")

        self.observer.join()


from datetime import datetime, timedelta


class Handler(FileSystemEventHandler):

    def __init__(self):
        self.last_modified = datetime.now()

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=2):
            return
        else:
            self.last_modified = datetime.now()
        if event.is_directory:
            return None
        print(f'Event type: {event.event_type}  path : {event.src_path}')
        print("Received modified event - %s." % event.src_path)
        if event.src_path.endswith('.py'):
            base_path, filename = os.path.split(event.src_path)
            result = subprocess.run(f"pytest {base_path}/test_{filename}", shell=True)
            print(result)
            if result.returncode == 0:
                print("Go to the next stage")
            else:
                print("There is still something missing here. Try again.")


if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    w = Watcher(directory)
    w.run()
