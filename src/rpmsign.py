#!/usr/bin/python3
import argparse
import os
import sys
from typing import List, Dict

import lib.mygpg as mygpg
import lib.myrpm as myrpm
import lib.fileops as fileops

DEFAULT_OUTPUT_FOLDER = "signed_packages"


def _check_folder_exists(folder: str) -> str:
    """ Check given folder actually exists.

    :param folder: Folder to check.
    :return: Given string if it is actually a folder.
    """
    if os.path.isdir(folder):
        return folder
    else:
        raise argparse.ArgumentTypeError(f"Given folder {folder} does not exists.")


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
    parser.add_argument("-k", "gpg_private_key",
                        type=str,
                        help="GPG private key to be used to sign, in armor protected format.",
                        metavar="GPG_PRIVATE_KEY")
    parser.add_argument("-p", "gpg_passphrase",
                        type=str,
                        help="GPG passphrase to be used to sign.",
                        metavar="GPG_PASSPHRASE")
    parser.add_argument("-n", "gpg_name",
                        type=str,
                        help="Name to use to sign.",
                        metavar="GPG_NAME")
    parser.add_argument("-f", "rpm_folder",
                        type=_check_folder_exists,
                        help="Folder with rpm files to be signed.",
                        metavar="RPM_FOLDER")
    parser.add_argument("-o", "output_folder",
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

    mygpg.import_private_key(
        private_key=arguments["gpg_private_key"],
        passphrase=arguments["gpg_passphrase"],
    )

    for package in fileops.get_files_with_extension("rpm", folder=arguments["rpm_folder"]):
        with fileops.place_package_at_signing_folder(package_path=package) as package_to_sign:
            myrpm.sign(
                name=arguments["gpg_name"],
                passphrase=arguments["passphrase"],
                file=package_to_sign
            )
            fileops.place_signed_file_at_output_folder(package_to_sign, arguments["output_folder"])


if __name__ == "__main__":
    main()
