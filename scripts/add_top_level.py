from typing import List, Optional
import sys
import argparse
import zipfile


TOP_LEVEL_PACKAGES: List[str] = [
    "osgeo",
    "osgeo_utils"
]


def get_dist_info_dir(file_name: str) -> str:
    if zipfile.is_zipfile(file_name):
        with zipfile.ZipFile(file_name) as arch:
            names: List[str] = arch.namelist()
            dist_dir: Optional[str] = next((n for n in names if "-" in n), None)
            if not dist_dir:
                print("No dist-info dir inside the ZIP file.")
                sys.exit(1)
                
            dir_name: str = dist_dir.split("/")[0]
            return dir_name
     
    else:
        print("This is not a valid ZIP format file.")
        sys.exit(1)


def add_top_level(file_name: str, dir_name: str):
    with zipfile.ZipFile(file_name, "a") as arch:
        data_path: str = f"{dir_name}/top_level.txt"
        with arch.open(data_path, "w") as data_file:
            for pac in TOP_LEVEL_PACKAGES:
                if not pac.endswith("\n"):
                    pac += "\n"

                pac_bytes = pac.encode("utf-8")
                data_file.write(pac_bytes)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add top_level.txt to wheel")
    # parser.add_argument("dest_dir", type=str, help="Destination directory")
    parser.add_argument("wheel", type=str, help="Python package wheel")
    args: argparse.Namespace = parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    dir_name: str = get_dist_info_dir(args.wheel)
    add_top_level(args.wheel, dir_name)
