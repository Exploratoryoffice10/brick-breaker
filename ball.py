from entity import Entity


class Ball(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__chr = 'o'
        self.__vx = 0
        self.__vy = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_vx(self,val):
        return self.__vx

    def get_vy(self,val):
        return self.__vy

    def get_chr(self):
        return self.__chr

    def set_vx(self,val):
        self.__vx = val

    def set_vy(self,val):
        self.__vy = val

    def move_it(self):
        self.x += self.__vx
        self.y += self.__vy

    def move_with_paddle(self, val):
        self.x += val

    def set_xy(self, val_x, val_y):
        self.x = val_x
        self.y = val_y

    def invert_vx(self):
        val = self.__vx
        self.__vx = -val

    def invert_vy(self):
        val = self.__vy
        self.__vy = -val
