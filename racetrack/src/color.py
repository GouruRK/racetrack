import colorsys
from random import randint


class Colors:

    def __init__(self, r: int, g: int, b: int) -> None:
        self._rgb = (r, g, b)
        self.hsv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    def rgb(self) -> tuple[int, int, int]:
        return tuple(map(lambda e: int(e * 255), colorsys.hsv_to_rgb(*self.hsv)))

    def hex(self) -> str:
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda e: int(e * 255), colorsys.hsv_to_rgb(*self.hsv))
        )

    def gradient(self, color: "Colors", steps: int) -> list["Colors"]:
        r1, g1, b1 = self.rgb()
        r2, g2, b2 = color.rgb()
        rdelta, gdelta, bdelta = (r2 - r1) / steps, (g2 - g1) / steps, (b2 - b1) / steps
        res = []
        for _ in range(steps):
            r1 += rdelta
            g1 += gdelta
            b1 += bdelta
            res.append(Colors(r1, g1, b1))
        return res

    def __eq__(self, other) -> bool:
        if isinstance(other, Colors):
            return self._rgb == other._rgb
        return self._rgb == other

    def __hash__(self) -> int:
        return hash(self._rgb)

    def __str__(self) -> str:
        return str(self.rgb())

    def __repr__(self) -> str:
        return str(self.rgb())

    @staticmethod
    def random_color() -> "Colors":
        return Colors(randint(0, 255), randint(0, 255), randint(0, 255))


class Color:

    RED = Colors(255, 0, 0)
    GREEN = Colors(0, 255, 0)
    BLUE = Colors(0, 0, 255)
    WHITE = Colors(255, 255, 255)
    BLACK = Colors(0, 0, 0)
    GREY = Colors(128, 128, 128)
    DARKCYAN = Colors(0, 128, 128)
