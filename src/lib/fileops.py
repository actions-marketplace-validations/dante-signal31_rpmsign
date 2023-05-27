""" Library for basic file operations.

For rpmsign purposes only need to create a temporal folder where files to be signed should be placed while signing.
"""
import contextlib
import os.path
import tempfile
from test_common.fs import ops


@contextlib.contextmanager
def temp_dir() -> str:
    """ Context manager to create a temporal folder on /tmp

    Actually is a wrapper for tempfile.TemporaryDirectory() .

    This wrapper is going to *yield* the object returned by TemporaryDirectory(),
    so you can use it as you would use that object in a context manager.

    As soon as you return from context manager the temporal folder will be lost.

    :returns: Path to created temporal folder
    """
    with tempfile.TemporaryDirectory() as temp_folder:
        yield temp_folder


@contextlib.contextmanager
def place_package_at_signing_folder(package_path: str):
    """ Context manager to create a temp folder to place there the package to sign.

    :param package_path: Package pathname.
    :return: Context manager yields the file pathname at its temporal place.
    """
    with temp_dir() as temp_folder:
        file_name = os.path.basename(package_path)
        temp_file_pathname = os.path.join(temp_folder, file_name)
        ops.copy_file(package_path, temp_file_pathname)
        yield temp_file_pathname


def place_signed_file_at_output_folder(signed_file: str, output_folder: str) -> None:
    """ Copy signed file to output folder.

    If output folder does not exist, then it is created.

    :param signed_file: File pathname to copy.
    :param output_folder: Folder pathname where file should be copied to.
    :return: None
    """
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    file_name = os.path.basename(signed_file)
    new_pathname = os.path.join(output_folder, file_name)
    ops.copy_file(signed_file, new_pathname)


def get_files_with_extension(extension: str, folder: str=".") -> str:
    """ Iterator to get pathnames to files with a given extension.

    :param extension: Extension that must have returned file pathnames
    :param folder: Folder where assessed files are placed.
    :return: An iterator over detected files with that extension.
    """
    if not os.path.isabs(folder):
        folder = os.path.join(os.getcwd(), folder)

    for entry in os.listdir(folder):
        entry_pathname = os.path.join(folder, entry)
        if os.path.isfile(entry_pathname) and os.path.splitext(entry)[1] == f".{extension}":
            yield entry


