import hashlib
import os
import configparser
import requests
import tarfile


def get_config_file():
    config_file_name = "config.conf"
    config_file_path = f"~/.config/compatman"  # Default search location

    XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME")  # see if XDG_CONFIG_HOME is set and use instead of default
    if XDG_CONFIG_HOME is not None:
        XDG_CONFIG_HOME.removesuffix("/")
        config_file_path = f"{XDG_CONFIG_HOME}/compatman"

    return os.path.expanduser(f"{config_file_path}/{config_file_name}")


def get_temp_folder():
    path = "/tmp/compatman"
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_all_config_names():
    config = configparser.ConfigParser()
    config.read(get_config_file())
    return config.sections()


def read_config(config_name: str):
    config = configparser.ConfigParser()
    config.read(get_config_file())
    return {
        "name": config_name,
        "type": config[config_name]["type"],
        "path": os.path.expanduser(config[config_name]["path"].removesuffix("/")),
        "version": config[config_name]["version"]
    }


def get_current_version(path: str):
    version_path = f"{path}/version"
    if os.path.exists(version_path):
        with open(version_path) as file:
            version = file.readline().split(" ")[1].removesuffix("\n")
            return version

    return "Null Version"


def download_to_temp_folder(link: str, file_size: int, name: str):
    folder_path = f"{get_temp_folder()}/{name}"
    response = requests.get(link, stream=True)
    if os.path.exists(folder_path):
        os.remove(folder_path)
    with open(file=folder_path, mode="xb") as file:
        total_downloaded = 0
        for chunk in response.iter_content(chunk_size=1024 ^ 2):
            print(f"Downloading {int((total_downloaded / file_size) * 100)}%", end="\r")
            file.write(chunk)
            total_downloaded += len(chunk)
        print("")


def extract_tar_file_to_temp_folder(tarfile_path: str):
    with tarfile.open(name=tarfile_path) as tar_file:
        tar_file.extractall(get_temp_folder())
        return tar_file.getnames()  # Return member names


def check_checksum(algorithm, file, checksum):
    with open(file, "rb") as file:
        file_checksum = hashlib.new(algorithm, file.read()).hexdigest()
        if checksum == file_checksum:
            return True
        return False
