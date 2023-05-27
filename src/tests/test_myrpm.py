import contextlib
import os.path
import pathlib
import pytest
from test_common.fs.temp import temp_dir
import test_common.fs.ops as ops

import lib.myrpm as myrpm
import tests.test_mygpg as test_mygpg

UNKNOWN_SIGNATURE_PACKAGE = "src/tests/resources/packages/ImageMagick-perl-6.4.0.10-2.fc10.i386.rpm"
WELL_KNOWN_SIGNATURE_PACKAGE = "src/tests/resources/packages/package_well_signed/ConsoleKit-0.3.0-2.fc10.i386.rpm"
NO_SIGNATURE_PACKAGE = "src/tests/resources/packages/package_without_sign/esl-erlang-compat-21.2.6-1.noarch.rpm"

TEST_CERTIFICATE_FOLDER = "src/tests/resources/test_certificate/"
TEST_CERTIFICATE_NAME = "Dummy certificate for automated testing (Don\'t use for sign anything important. Use for testing signing in automated workflows.) <dummy_test@gmail.com>"
TEST_CERTIFICATE_PASSWORD_PATHNAME = os.path.join(TEST_CERTIFICATE_FOLDER, "test_certificate_password.txt")
TEST_PUB_CERTIFICATE_PATHNAME = os.path.join(TEST_CERTIFICATE_FOLDER, "test_pub.gpg")
TEST_CERTIFICATE_PASSWORD = pathlib.Path(TEST_CERTIFICATE_PASSWORD_PATHNAME).read_text()


@contextlib.contextmanager
def rpm_keys_loaded(fingerprint: str):
    """ Context manager to load test keys temporally in RPM database and remove then after tests. """
    absolute_path_to_pub_certificate = os.path.join(os.getcwd(), TEST_PUB_CERTIFICATE_PATHNAME)
    myrpm.import_public_key(absolute_path_to_pub_certificate)
    yield
    myrpm.remove_public_key(fingerprint)


def test_sign(temp_dir):
    """ Assert a package can be properly signed."""
    with test_mygpg.test_keys_loaded() as fingerprint:
        with rpm_keys_loaded(fingerprint):
            file_to_sign = os.path.basename(NO_SIGNATURE_PACKAGE)
            destination_pathname = os.path.join(temp_dir, file_to_sign)
            ops.copy_file(NO_SIGNATURE_PACKAGE, destination_pathname)
            # Assert this file is not signed yet.
            with pytest.raises(myrpm.UnsignedFileError) as e:
                myrpm.is_valid_signature(destination_pathname)
            # Now sign it.
            myrpm.sign(name=TEST_CERTIFICATE_NAME,
                       passphrase=TEST_CERTIFICATE_PASSWORD,
                       file=destination_pathname)
            # Assert now is properly signed.
            assert myrpm.is_valid_signature(destination_pathname)


def test_is_valid_signature():
    """ Assert that is_valid_signature() can identify a good signature, a bad signature and an absent signature. """
    with test_mygpg.test_keys_loaded() as fingerprint:
        with rpm_keys_loaded(fingerprint):
            assert not myrpm.is_valid_signature(UNKNOWN_SIGNATURE_PACKAGE)
            assert myrpm.is_valid_signature(WELL_KNOWN_SIGNATURE_PACKAGE)
            with pytest.raises(myrpm.UnsignedFileError) as e:
                myrpm.is_valid_signature(NO_SIGNATURE_PACKAGE)
