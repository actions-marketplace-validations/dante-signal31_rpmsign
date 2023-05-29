import os.path
import pathlib

import lib.fileops as fileops
import lib.mygpg as mygpg
import lib.myrpm as myrpm
import rpmsign

import tests.test_myrpm as test_myrpm
from test_common.fs.temp import temp_dir


NO_SIGNATURE_PACKAGE = "src/tests/resources/packages/package_without_sign/esl-erlang-compat-21.2.6-1.noarch.rpm"
PACKAGES_FOLDER = "src/tests/resources/packages/"
PRIVATE_KEY_FILE = "src/tests/resources/test_certificate/test_priv.gpg"
PRIVATE_KEY_PASSWORD_FILE = "src/tests/resources/test_certificate/test_certificate_password.txt"
PASSWORD = pathlib.Path(PRIVATE_KEY_PASSWORD_FILE).read_text()
TEST_CERTIFICATE_NAME = "Dummy certificate for automated testing (Don\'t use for sign anything important. Use for testing signing in automated workflows.) <dummy_test@gmail.com>"


def test_sign_single_file(temp_dir):
    """ Assert a single rpm file can be signed. """
    # First sign the file.
    arguments = ["-k", pathlib.Path(PRIVATE_KEY_FILE).read_text(),
                 "-p", PASSWORD,
                 "-n", TEST_CERTIFICATE_NAME,
                 "-s", NO_SIGNATURE_PACKAGE,
                 "-o", temp_dir]
    rpmsign.main(arguments)

    # Now assert file is properly signed.
    keyring = mygpg.GPGKeyring()
    fingerprint = keyring.get_key_fingerprint(TEST_CERTIFICATE_NAME)
    signed_file = os.path.basename(NO_SIGNATURE_PACKAGE)
    signed_file_pathname = os.path.join(temp_dir, signed_file)
    with test_myrpm.rpm_keys_loaded(fingerprint):
        assert myrpm.is_valid_signature(signed_file_pathname)


def test_sign_multiple_files(temp_dir):
    """ Assert multiple rpm files can be signed at one go. """
    # First sign the file.
    arguments = ["-k", pathlib.Path(PRIVATE_KEY_FILE).read_text(),
                 "-p", PASSWORD,
                 "-n", TEST_CERTIFICATE_NAME,
                 "-f", PACKAGES_FOLDER,
                 "-o", temp_dir]
    rpmsign.main(arguments)

    # Now assert files are properly signed.
    keyring = mygpg.GPGKeyring()
    fingerprint = keyring.get_key_fingerprint(TEST_CERTIFICATE_NAME)
    with test_myrpm.rpm_keys_loaded(fingerprint):
        for package in fileops.get_files_with_extension("rpm", folder=temp_dir):
            assert myrpm.is_valid_signature(os.path.join(temp_dir, package))
