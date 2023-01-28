import os
import subprocess
import time
from datetime import datetime, timedelta

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, _directory):
        self.observer = Observer()
        self.directory = _directory

    def run(self, _learning_path):
        event_handler = Handler(_learning_path, self.observer)
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception:
            self.observer.stop()
            print("Stop. Exiting...")
        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, _learning_path: LearningPath, observer: Observer):
        self.last_modified = datetime.now()
        self.learning_path = _learning_path
        self.observer = observer

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
            node = self.learning_path.lessons[filename]
            result = subprocess.run(f"pytest {node.test_file_name}", shell=True)
            if result.returncode == 0:
                if node.next_node is not None:
                    progress.update(1)
                    progress.display()
                    print(f"\nGo to the next stage: {node.next_node.file_path}")
                else:
                    print("Hooray!")
                    exit(0)

            else:
                print("There is still something missing here. Try again.\n")
                print(node.hint)
                progress.display()



