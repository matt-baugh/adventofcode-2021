from pathlib import Path
from typing import Any, Optional, Union


def load_file(file_path: Path, skip_empty=False):
    with open(file_path, "r") as file:
        content = file.readlines()
        if skip_empty:
            content = [line.strip() for line in content if line.strip()]
        else:
            content = [line.strip() for line in content]
    return content

SplitHierarchy = Union[Optional[str], tuple[Optional[str], tuple['SplitHierarchy', ...]]]

def split_str(input_str: str, split_val):

    if isinstance(split_val, tuple):
        separator, hierarchies = split_val
        return [split_str(s, s_v) for s, s_v in zip(input_str.split(separator), hierarchies)]
    else:
        return input_str.split(split_val)

def parse_file_lines(file_path: Path, split_val: SplitHierarchy = None, skip_empty=False):
    return [split_str(line, split_val) for line in load_file(file_path, skip_empty=skip_empty)]

def chunk_input(input_list: list, chunk_separator: Any, skip_empty=False):
    chunks = []
    curr_chunk = []
    for e in input_list:
        if e == chunk_separator:
            chunks.append(curr_chunk)
            curr_chunk = []
        else:
            curr_chunk.append(e)
    if curr_chunk or not skip_empty:
        chunks.append(curr_chunk)
        
    if skip_empty:
        chunks = [c for c in chunks if c]
        
    return chunks