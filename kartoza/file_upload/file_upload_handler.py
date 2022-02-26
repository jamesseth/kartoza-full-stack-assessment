"""File chunker implementation."""
from logging import getLogger
from pathlib import Path
from typing import Any

LOG = getLogger(__name__)


def handle_uploaded_file(data: Any, file_path: Path):
    """
    Write data resieved into a file at the parsed file path in chuncks.

    :param data: The file data
    :param file_path: The path to the file that you want to write to
    """
    try:
        with file_path.open('', 'wb+') as fout:
            for chunk in data.chunks():
                fout.write(chunk)
    except Exception as err:
        LOG.exception(err)
        raise err
