import os
import shutil
import sys

from ..utils import get_all_config_names
from ..utils import read_config
from ..utils import get_temp_folder
from ..Syncers.ge_sync import sync as ge_sync


def main(configs, force):
    if configs is None:
        configs = get_all_config_names()
    for config in configs:
        compatibility_tool = read_config(config)
        start_sync(compatibility_tool, force)


def start_sync(compatibility_tool: dict, force):
    try:
        match compatibility_tool["type"]:
            case "proton-ge":
                ge_sync(compatibility_tool["version"], compatibility_tool["path"], compatibility_tool["name"], force)
            case _:
                print("Undefined runner type please specify a correct runner type")
    except PermissionError:
        print("You do not have the permission to do this action")
    except KeyboardInterrupt:
        print("\nCanceling operations...")
    finally:
        if os.path.exists(get_temp_folder()):  # Clean up temp folder if exists
            shutil.rmtree(get_temp_folder())


if __name__ == "__main__":
    main(sys.argv, False)
