#!/usr/bin/env python3

import os


def read_file(directory: str, file_name: str) -> str:
    """Reads file

    Args:
        directory (str): Directory name
        file_name (str): File name

    Returns:
        str: Path to file
    """

    return os.path.join(directory, file_name)
