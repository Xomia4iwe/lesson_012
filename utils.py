import os
import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nФункция работала {elapsed} секунд(ы)')
        return result

    return surrogate


def get_file_path(scan_folder):
    file_path = []
    for dirpath, dirnames, filenames in os.walk(scan_folder):
        for file in filenames:
            file_path.append(os.path.join(dirpath, file))
    return file_path


