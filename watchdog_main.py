import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pyfiglet
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.learning_path import LearningPath, load_learning_path_from_file


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


if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'

    f = pyfiglet.Figlet(font='slant')
    print(f.renderText('Welcome to pyhtonlings'))
    from pbar import init_progress_bar
    learning_path = load_learning_path_from_file(Path("src/learning_path.yaml"))
    i = 0
    for i, node in enumerate(learning_path.lessons.values()):
        result = subprocess.run(f"pytest {node.test_file_name}", shell=True, capture_output=True)
        if result.returncode != 0:
            break
    else:
        i = len(learning_path.lessons)
    progress = init_progress_bar(len(learning_path.lessons), initial=i)
    print(f"\nNext exercise: {node.file_path}")
    w = Watcher(directory)
    w.run(learning_path)
    print(f.renderText('Congrats! You have just finished pyhtonlings'))


