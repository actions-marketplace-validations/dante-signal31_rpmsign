import os.path

import lib.fileops as fileops

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


def test_place_package_at_signing_folder():
    """ Assert that package to sign is properly placed at temporal folder. """
    package_to_move = RPM_PACKAGES.pop()
    with fileops.place_package_at_signing_folder(os.path.join(TEST_PACKAGES_PATH, package_to_move)) as temp_file:
        assert os.path.isfile(temp_file)
        assert os.path.basename(temp_file) == package_to_move
        assert "/tmp/" in temp_file


def test_place_signed_file_at_output_folder():
    """ Assert that package can be properly moved to output folder. """
    package_to_move = RPM_PACKAGES.pop()
    with fileops.temp_dir() as temp_folder:
        temp_file_pathname = os.path.join(temp_folder, package_to_move)
        assert not os.path.isfile(temp_file_pathname)
        fileops.place_signed_file_at_output_folder(os.path.join(TEST_PACKAGES_PATH, package_to_move), temp_folder)
        assert os.path.isfile(temp_file_pathname)
