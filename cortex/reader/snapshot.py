class Snapshot:
    """Snapt apt apt"""

    def __init__(self, time):
        self.time = time

    def set_location(self, tx, ty, tz):
        """Sets location, represented by (x,y,z)"""
        self.tx = tx
        self.ty = ty
        self.tz = tz

    def set_rotation(self, rx, ry, rz, rw):
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.rw = rw

    def set_color_image(self, hight, width, image):
        self.chight = hight
        self.cwidth = width
        self.cimage = image

    def set_depth_image(self, hight, width, image):
        self.dhight = hight
        self.dwidth = width
        self.dimage = image

    def set_thoughts(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness
