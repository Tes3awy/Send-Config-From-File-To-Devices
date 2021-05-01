#!/usr/bin/env python3

import os


def check_file_status(file_path: str) -> int:
    """Checks file status

    Args:
        file_path (str): Path to a file

    Returns:
        int: Size of the file
    """
    return os.stat(file_path).st_size
