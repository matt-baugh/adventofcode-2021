from pathlib import Path
def load_file(file_path: Path, skip_empty=False):
    with open(file_path, "r") as file:
        content = file.readlines()
        if skip_empty:
            content = [line.strip() for line in content if line.strip()]
        else:
            content = [line.strip() for line in content]
    return content
