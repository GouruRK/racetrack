import colorsys

class Colors:
    
    def __init__(self, r: int, g: int, b: int) -> None:
        self.hsv = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    
    def rgb(self) -> tuple[int, int, int]:
        return tuple(map(lambda e: int(e*255), colorsys.hsv_to_rgb(*self.hsv)))
    
    def hex(self) -> str:
        return "#{:02x}{:02x}{:02x}".format(*map(lambda e: int(e*255), colorsys.hsv_to_rgb(*self.hsv)))

    def gradient(self, color: 'Colors', steps: int) -> list['Colors']:
        r1, g1, b1 = self.rgb()
        r2, g2, b2 = color.rgb()
        rdelta, gdelta, bdelta = (r2-r1)/steps, (g2-g1)/steps, (b2-b1)/steps
        res = []
        for _ in range(steps):
            r1 += rdelta
            g1 += gdelta
            b1 += bdelta
            res.append(Colors(r1, g1, b1))
        # h, _, _ = self.hsv
        # padding = 1/max_iter
        # res = []
        # for _ in range(max_iter):
        #     h += padding
        #     color = Colors(*map(lambda e: int(e*255), colorsys.hsv_to_rgb(h, 1, 1)))
        #     res.append(color)
        return res

    def __str__(self):
        return str(self.rgb())
    
    def __repr__(self):
        return str(self.rgb())

class Color:
    
    RED      = Colors(255, 0, 0)
    GREEN    = Colors(0, 255, 0)
    BLUE     = Colors(0, 0, 255) 
    WHITE    = Colors(255, 255, 255)
    BLACK    = Colors(0, 0, 0)
    GREY     = Colors(128, 128, 128)
    DARKCYAN = Colors(0, 139, 139)
