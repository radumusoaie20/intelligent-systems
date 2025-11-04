from pathlib import Path

def make_file_dir_if_not_exist(filepath):

    parent_dir = Path(filepath).parent

    if parent_dir.exists():
        return

    parent_dir.mkdir(parents=True, exist_ok=True)