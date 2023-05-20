#!/usr/bin/python3
import argparse
import sys
from typing import List, Dict

DEFAULT_OUTPUT_FOLDER = "signed_packages"

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
    parser.add_argument("-p", "gpg_private_key",
                        type=str,
                        help="GPG private key to be used to sign, in armor protected format.",
                        metavar="GPG_PRIVATE_KEY")
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
    parser.add_argument("-s", "--manpage_section",
                        type=str,
                        default=str(DEFAULT_MANPAGE_SECTION),
                        help=f"Section for resulting manpage. Defaults to "
                             f"{DEFAULT_MANPAGE_SECTION}",
                        metavar="MANPAGE_SECTION")
    parser.add_argument("-t", "--manpage_title",
                        type=str,
                        help="Title for resulting manpage. Defaults to manpage_name.",
                        metavar="MANPAGE_TITLE")
    parser.add_argument("-u", "--uncompressed",
                        action="store_true",
                        default=False,
                        help="Do not compress resulting manpage. Defaults to False")
    parser.add_argument("-f", "--manpage_folder",
                        type=str,
                        help="Folder to place resulting manpage. Defaults to the "
                             "same as markdown file.",
                        metavar="MANPAGE_FOLDER")
    parsed_arguments = vars(parser.parse_args(args))
    filtered_parser_arguments = {key: value
                                 for key, value in parsed_arguments.items()
                                 if value is not None}
    return filtered_parser_arguments


def main(args=sys.argv[1:]) -> None:
    pass


if __name__ == "__main__":
    main()