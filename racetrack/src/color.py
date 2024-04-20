"""Module to manage colors

"""

import colorsys
from random import randint

___all__ = ["Color"]


class Colors:
    """Contains color data and method to transform it

    Attributes
    ----------
    hsv : tuple[float]
        hsv data
    """

    def __init__(self, r: int, g: int, b: int) -> None:
        """Constructor of the 'Colors' object

        Parameters
        ----------
        r : int
            red component, from 0 to 255
        g : int
            green component, from 0 to 255
        b : int
            blue component, from 0 to 255
        """
        self.hsv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    def rgb(self) -> tuple[int, int, int]:
        """Get color in rgb format

        Returns
        -------
        tuple[int, int, int]
            rgb representation of the color
        """
        return tuple(map(lambda e: int(e * 255), colorsys.hsv_to_rgb(*self.hsv)))

    def hex(self) -> str:
        """Get color in hexadecimal format

        Returns
        -------
        str
            hexadecimal representation of the color
        """
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda e: int(e * 255), colorsys.hsv_to_rgb(*self.hsv))
        )

    def gradient(self, color: "Colors", steps: int) -> list["Colors"]:
        """Get list of colors to another color in `steps` steps

        Returns
        -------
        list[Colors]
            list of colors of length `steps` form the instance color to the
            given one
        """
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
            return self.rgb() == other.rgb()
        return self.rgb() == other

    def __hash__(self) -> int:
        return hash(self.rgb())

    def __str__(self) -> str:
        return str(self.rgb())

    def __repr__(self) -> str:
        return str(self.rgb())


class Color:
    """Color enumeration"""

    RED = Colors(255, 0, 0)
    GREEN = Colors(0, 255, 0)
    BLUE = Colors(0, 0, 255)
    WHITE = Colors(255, 255, 255)
    BLACK = Colors(0, 0, 0)
    GREY = Colors(128, 128, 128)
    DARKCYAN = Colors(0, 128, 128)
