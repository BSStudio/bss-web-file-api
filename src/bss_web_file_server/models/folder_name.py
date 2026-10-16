"""A module for validating names that are used as a single folder name."""

from typing import Annotated

from pydantic import AfterValidator

FORBIDDEN_CHARACTERS = ("/", "\\", "\0")
RESERVED_NAMES = ("", ".", "..")


def check_folder_name(name: str) -> str:
    """
    Check that the name can only refer to an entry directly inside a folder.
    :param name: the name to check
    :return: the unchanged name
    :raise ValueError: if the name contains a path separator or is reserved
    """
    if name in RESERVED_NAMES or any(c in name for c in FORBIDDEN_CHARACTERS):
        raise ValueError("must be a single folder name without path separators")
    return name


FolderName = Annotated[str, AfterValidator(check_folder_name)]
