#!/usr/bin/env python3

import os


def clear_file_contents(path: str):
    """Clear file contents

    Args:
        path (str): Path to a file
    """
    with open(file=path, mode="w", encoding="UTF-8") as f:
        f.truncate(os.stat(path).st_size)
