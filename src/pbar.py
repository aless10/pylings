from tqdm import tqdm


def progress_bar(lessons: int, initial: int = 0) -> tqdm:
    return tqdm(
        total=lessons,
        desc="Progress",
        initial=initial,
        colour='green',
        bar_format="{l_bar}{bar}{n_fmt}/{total_fmt}"
    )
