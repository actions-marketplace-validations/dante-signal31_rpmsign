"""" Library to deal with gpg operations.

I'm not going to implement every possible gpg operation. For rpmsign purposes only secret key import is needed.
"""""
from typing import Union

import gnupg


class GPGKeyNotFoundError(Exception):
    def __init__(self, fingerprint: str):
        self.fingerprint = fingerprint

    def __str__(self):
        return f"I didnt find GPG key with fingerprint: {self.name}"


class GPGKeyring:
    """ Class representing a GPG keyring. """
    def __init__(self, gpg_home=None):
        """
        :param gpg_home: If kept to None then default keyring location is used, but you can set an alternate keyring store path.
        """
        self.gpg = gnupg.GPG(gnupghome=gpg_home)

    def get_key_fingerprint(self, name: str) -> Union[str, None]:
        """ Get GPG fingerprint of the key with given fingerprint. """
        key_list = self.gpg.list_keys()
        for index, uid in enumerate(key_list.uids):
            if name in uid:
                return key_list.fingerprints[index]
        return None

    def remove_private_key(self, fingerprint: str, passphrase: str) -> None:
        """ Remove key from keyring using its fingerprint.

        :raise: mygpg.GPGKeyNotFoundError if no key is found with that name.
        """
        key_list = self.gpg.list_keys()
        if fingerprint not in key_list.fingerprints:
            raise GPGKeyNotFoundError(fingerprint)

        self.gpg.delete_keys(fingerprints=fingerprint, secret=True, passphrase=passphrase)
        self.gpg.delete_keys(fingerprints=fingerprint)

    def import_private_key(self, private_key: str, passphrase: str) -> None:
        """ Import given private key into keyring.

        :param private_key: Private key in ASCII armored format.
        :param passphrase: Passphrase to access to private key.
        :return: None
        """
        self.gpg.import_keys(key_data=private_key, passphrase=passphrase)
