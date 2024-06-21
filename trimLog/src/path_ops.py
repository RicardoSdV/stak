from pathlib import Path
from typing import List, Generator, Tuple


def find_read_and_write_log_paths(force_retrim: bool, log_dir_path: str) -> List[Tuple[Path, Path]]:

    result = []
    for log_path in Path(log_dir_path).rglob('**/*.log'):

        if not log_path.name.startswith('t_'):
            trimmed_log_path = log_path.with_name('t_' + log_path.name)

            if not trimmed_log_path.exists() or force_retrim:
                result.append((log_path, trimmed_log_path))

    return result