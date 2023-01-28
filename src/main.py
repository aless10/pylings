directory = sys.argv[1] if len(sys.argv) > 1 else '.'

from pbar import init_progress_bar
progress = init_progress_bar(len(learning_path.lessons), initial=i)
w = Watcher(directory)
w.run(learning_path)