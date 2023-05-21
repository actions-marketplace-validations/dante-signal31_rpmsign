from lib import fileops

TEST_PACKAGES_PATH = "src/tests/resources/packages/"
RPM_PACKAGES = {
    "ConsoleKit-0.3.0-2.fc10.i386.rpm",
    "ImageMagick-perl-6.4.0.10-2.fc10.i386.rpm",
    "MySQL-python-1.2.2-7.fc10.i386.rpm",
}

DEB_PACKAGES = {
    "cups-browsed_1.28.15-0ubuntu1.2_amd64.deb",
    "gedit_41.0-3_amd64.deb",
}


def test_get_files_with_extension():
    """ Assert only RPM packages are detected. """
    detected_packages = {package for package in fileops.get_files_with_extension("rpm", TEST_PACKAGES_PATH)}
    assert detected_packages == RPM_PACKAGES
