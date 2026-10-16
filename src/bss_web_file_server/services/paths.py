"""This module contains helpers for building paths inside a base folder."""

import os
from pathlib import Path

from ..models.folder_name import check_folder_name


def child_path(base: Path, name: str) -> Path:
    """
    This method will return the path of the entry called name directly inside base.
    :param base: the folder the entry has to be in
    :param name: the name of the entry
    :return: the path of the entry
    :raise ValueError: if the name points outside base or isn't a single folder name
    """
    base_path = os.path.normpath(base)
    path = os.path.normpath(os.path.join(base_path, name))
    if not path.startswith(base_path + os.sep):
        raise ValueError(f"{name!r} points outside {base_path}")
    # normpath turns "nested/../url" into a direct child, so check the raw name too
    check_folder_name(name)
    return Path(path)
