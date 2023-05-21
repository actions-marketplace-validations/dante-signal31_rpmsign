"""" Library to deal with gpg operations.

I'm not going to implement every possible gpg operation. For rpmsign purposes only secret key import is needed.
"""""


def import_private_key(private_key: str, passphrase: str)-> None:
    """ Import given private key into keyring.

    :param private_key: Private key in ASCII armored format.
    :param passphrase: Passphrase to access to private key.
    :return: None
    """
    raise NotImplementedError

