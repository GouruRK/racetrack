def parse_map(filepath: str) -> list[str]:
    with open(filepath, "r") as file:
        return [line for line in file]