from typing import Any
import argparse
from src.solve import SOLVERS
from src.settings import *

from src.settings import DEFAULT_SPACING, DEFAULT_MAP_MODE, DEFAULT_RULE, BLOCK_SIZE

def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacing", "-s", type=int, default=DEFAULT_SPACING,
                        required=False)
    parser.add_argument("--dim", "-d", type=int, default=BLOCK_SIZE,
                        required=False)
    parser.add_argument("--opti", "-o", default=False, action="store_true",
                        required=False)
    parser.add_argument("--mode", "-m", type=str, default=DEFAULT_MAP_MODE,
                        required=False, choices={TEXT_MODE, IMAGE_MODE})
    parser.add_argument("--rule", "-r", type=str, default=DEFAULT_RULE,
                        required=False, choices={STRICT_RULE, LAX_RULE})
    parser.add_argument("--solve", "-S", type=str, default=None,
                        required=False, choices=SOLVERS.keys())
    parser.add_argument("map", type=str)
    
    return vars(parser.parse_args())
