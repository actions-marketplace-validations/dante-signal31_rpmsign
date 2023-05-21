"""" Library to deal with rpm operations.

I'm not going to implement every possible rpm operation. For rpm sign is needed.

Remember to install python3-rpm system package! without it this is not going to work.
"""""


def sign(name: str, passphrase: str, file: str)-> None:
    """ Sign RPM package.

    :param name: Name (usually an email) to use as signer.
    :param passphrase: Passphrase for this private key.
    :param file: RPM file to sign.
    :return: None
    """
    raise NotImplementedError
