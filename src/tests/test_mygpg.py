import os
import pathlib

import pytest

import lib.mygpg as mygpg

PRIVATE_KEY_FILE = "src/tests/resources/test_certificate/test_priv.gpg"
PRIVATE_KEY_PASSWORD = "src/tests/resources/test_certificate/test_certificate_password.txt"


def test_import_private_key():
    """ Assert a key can be properly imported and removed afterwards."""
    keyring = mygpg.GPGKeyring()
    found_key = keyring.get_key_fingerprint("dummy_test@gmail.com")
    assert found_key is None
    private_key_data = pathlib.Path(os.path.join(os.getcwd(), PRIVATE_KEY_FILE)).read_text()
    passphrase = pathlib.Path(os.path.join(os.getcwd(), PRIVATE_KEY_PASSWORD)).read_text()
    keyring.import_private_key(private_key=private_key_data, passphrase=passphrase)
    found_key = keyring.get_key_fingerprint("dummy_test@gmail.com")
    assert found_key is not None
    keyring.remove_private_key(fingerprint=found_key, passphrase=passphrase)
    found_key = keyring.get_key_fingerprint("dummy_test@gmail.com")
    assert found_key is None


def test_key_not_found_error():
    """ Assert that a mygpg.GPGKeyNotFoundError is raised when you try to remove a not existent key."""
    keyring = mygpg.GPGKeyring()
    private_key_data = pathlib.Path(os.path.join(os.getcwd(), PRIVATE_KEY_FILE)).read_text()
    passphrase = pathlib.Path(os.path.join(os.getcwd(), PRIVATE_KEY_PASSWORD)).read_text()
    keyring.import_private_key(private_key=private_key_data, passphrase=passphrase)
    found_key = keyring.get_key_fingerprint("dummy_test@gmail.com")
    # Now remove the key.
    keyring.remove_private_key(fingerprint=found_key, passphrase=passphrase)
    # Now try to remove again so an exception should be raised.
    with pytest.raises(mygpg.GPGKeyNotFoundError) as e:
        keyring.remove_private_key(fingerprint=found_key, passphrase=passphrase)


