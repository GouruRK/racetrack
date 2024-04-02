from typing import Any
import argparse

from src.settings import DEFAULT_SPACING, DEFAULT_MAP_MODE

TEXT_MODE = "text"
IMAGE_MODE = "image"

def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacing", "-s", type=int, default=DEFAULT_SPACING,
                        required=False)
    parser.add_argument("--mode", "-m", type=str, default=DEFAULT_MAP_MODE,
                        required=False, choices={TEXT_MODE, IMAGE_MODE})
    parser.add_argument("map", type=str)
    return vars(parser.parse_args())
