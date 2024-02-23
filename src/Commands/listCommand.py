from ..utils import get_all_config_names


def main():
    for name in get_all_config_names():
        print(name)