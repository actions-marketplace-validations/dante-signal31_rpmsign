#!/usr/bin/python3
import argparse
import os
import pathlib
import sys
import time
from typing import List, Dict

import lib.mygpg as mygpg
import lib.myrpm as myrpm
import lib.fileops as fileops

DEFAULT_OUTPUT_FOLDER = "signed_packages"
NONE_TAG = "_##"


def _check_folder_exists(folder: str) -> str:
    """ Check given folder actually exists.

    :param folder: Folder to check.
    :return: Given string if it is actually a folder.
    """
    if folder == NONE_TAG or os.path.isdir(folder):
        return folder
    else:
        raise argparse.ArgumentTypeError(f"Given folder {folder} does not exists.")


def _check_file_exists(file: str) -> str:
    """ Check given file actually exists.

    :param file: File to check.
    :return: Given string if it is actually a file.
    """
    if file == NONE_TAG or os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"Given file {file} does not exists.")


def parse_args(args: List[str]) -> Dict[str, str]:
    """ Parse given arguments

    :param args: Program arguments.
    :returns: A Dictionary with given arguments as keys and its respective values.
    """
    parser = argparse.ArgumentParser(
        description="Console command to sign RPM packages using passphrase protected GPG keys.",
        epilog="Follow this tool development at: "
               "<https://github.com/dante-signal31/rpmsign"
    )
    parser.add_argument("-k", "--gpg_private_key",
                        type=str,
                        help="GPG private key file to be used to sign, in armor protected format.",
                        metavar="GPG_PRIVATE_KEY")
    parser.add_argument("-p", "--gpg_passphrase",
                        type=str,
                        help="GPG passphrase to be used to sign.",
                        metavar="GPG_PASSPHRASE")
    parser.add_argument("-n", "--gpg_name",
                        type=str,
                        help="Name to use to sign.",
                        metavar="GPG_NAME")
    parser.add_argument("-s", "--rpm_file",
                        # type=_check_file_exists,
                        default=NONE_TAG,
                        help="Rpm file to be signed.",
                        metavar="RPM_FILE")
    parser.add_argument("-f", "--rpm_folder",
                        # type=_check_folder_exists,
                        default=NONE_TAG,
                        help="Folder with rpm files to be signed.",
                        metavar="RPM_FOLDER")
    parser.add_argument("-o", "--output_folder",
                        type=str,
                        default=str(DEFAULT_OUTPUT_FOLDER),
                        help="Folder where signed rpm files must be placed.",
                        metavar="OUTPUT_FOLDER")
    parsed_arguments = vars(parser.parse_args(args))
    filtered_parser_arguments = {key: value
                                 for key, value in parsed_arguments.items()
                                 if value is not None}
    return filtered_parser_arguments


def main(args=sys.argv[1:]) -> None:
    """ Main execution.

        Taken to its own function to ease testing.

        :param args: Application arguments. Only explicitly set at tests. Usually you'll
        leave it empty and it will populated with sys.argv values.
        """
    arguments: Dict[str, str] = parse_args(args)

    keyring = mygpg.GPGKeyring()
    keyring.import_private_key(
        private_key_file=arguments["gpg_private_key"],
        passphrase=arguments["gpg_passphrase"],
    )

    if "rpm_folder" in arguments and not arguments["rpm_folder"] == NONE_TAG:
        for package in fileops.get_files_with_extension("rpm", folder=arguments["rpm_folder"]):
            package_absolute_pathname = os.path.join(arguments["rpm_folder"], package)
            # Time sleep is needed to let gpg-agent cache expire, so gpg ask as a
            # passphrase every time. If you don't let this expiration happen you can
            # expect for a passphrase that is not asked at the end because it is cached
            # after the last file was signed. That problem happened with batch signing of
            # multiple files and with unittests.
            time.sleep(2)
            sign_package(arguments, package_absolute_pathname)
    elif "rpm_file" in arguments and not arguments["rpm_file"] == NONE_TAG:
        time.sleep(2)
        sign_package(arguments, arguments["rpm_file"])


def sign_package(arguments, package):
    """ Copy package to sign to a temporal folder, sign it there and copy signed package to output folder. """
    with fileops.place_package_at_signing_folder(package_path=package) as package_to_sign:
        myrpm.sign(
            name=arguments["gpg_name"],
            passphrase=arguments["gpg_passphrase"],
            file=package_to_sign,
        )
        fileops.place_signed_file_at_output_folder(package_to_sign, arguments["output_folder"])


if __name__ == "__main__":
    main()
