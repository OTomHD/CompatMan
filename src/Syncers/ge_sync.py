import os
import shutil
import hashlib
import requests

from ..utils import get_current_version, get_temp_folder, download_to_temp_folder, \
    extract_tar_file_to_temp_folder, check_checksum

baseURL = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
downloaded_archive_name = "downloaded_archive.tar.gz"


def sync(version, path, name, force):
    folder_path = f"{path}/{name}"

    tags = ""
    if version != "latest":  # Add tags to URL if not using latest version otherwise don't
        tags = "tags/"

    request = requests.get(f"{baseURL}/{tags}{version}")
    if request.status_code != 200:
        print(f'Error retrieving data \n status code:{request.status_code}')
        return
    data = request.json()
    download_version = data["tag_name"]

    if not force and check_version_is_installed(version, folder_path, download_version):
        return

    file_data = get_download_data(data["assets"])
    if file_data["file_link"] == "" or file_data["checksum"] == "":
        print("Unable to find download link or checksum")
        return

    print(f"Downloading {download_version}...")
    download_to_temp_folder(file_data["file_link"], file_data["file_size"], downloaded_archive_name)

    # Checksum the file

    if not force and not check_checksum("sha512", f"{get_temp_folder()}/{downloaded_archive_name}",
                                        file_data["checksum"].split(" ")[0]):
        print("checksum does not match exiting...")
        print("Use --force if you want to skip this check")

    print(f"Installing...")
    downloaded_folder = extract_tar_file_to_temp_folder(f"{get_temp_folder()}/{downloaded_archive_name}")[0]

    if os.path.exists(folder_path):  # Install proton-ge to user specified location
        shutil.rmtree(folder_path)
    shutil.move(f"{get_temp_folder()}/{downloaded_folder}", folder_path)


def check_version_is_installed(expected_version, folder_path, new_version):
    if expected_version == "latest" and os.path.exists(folder_path) and new_version == get_current_version(folder_path):
        print("Newest version already installed skipping...")
        return True

    if expected_version != "latest" and os.path.exists(folder_path):
        print("Version already installed use --force to force reinstall")
        return True

    return False


# file_link = Tar File download
# checksum_link = checksum text file download
def get_download_data(assets):
    file_link = ""
    file_size = 0
    checksum = ""
    for asset in assets:
        file_name = asset["name"]
        if file_name.endswith(".tar.gz"):
            file_link = asset["browser_download_url"]
            file_size = asset["size"]
        if file_name.endswith("sha512sum"):
            checksum = requests.get(asset["browser_download_url"]).content.decode()
    return {
        "file_link": file_link,
        "file_size": file_size,
        "checksum": checksum
    }
