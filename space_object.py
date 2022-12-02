import math
import config

class SpaceObject:
    def __init__(self, x, y, width, height, angle, obj_type, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.obj_type = obj_type
        self.id = id

        # count number of bullet moves to know when bullets expire
        self.move_count = 0

        if "upcoming" in obj_type:
            self.radius = config.radius[self.obj_type[9:]]
        else:
            self.radius = config.radius[self.obj_type]
        

    def turn_left(self):
        if self.obj_type == "spaceship":
            self.angle = (self.angle + config.angle_increment) % 360

    def turn_right(self):
        if self.obj_type == "spaceship":
            self.angle = (self.angle - config.angle_increment) % 360

    def move_forward(self):
        speed = config.speed[self.obj_type]
        self.x += speed * math.cos(math.radians(self.angle))
        self.y -= speed * math.sin(math.radians(self.angle))
        self.x %= self.width
        self.y %= self.height

    def get_xy(self):
        return (self.x, self.y)

    def collide_with(self, other):
        # calculate distance between 2 objects in the map
        # and in the case of wraparound
        # then compare to the sum of radii of 2 objects

        d = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        d_x = math.sqrt((self.width - abs(self.x - other.x))**2 
                        + (self.y - other.y)**2)
        d_y = math.sqrt((self.x - other.x)**2
                        + (self.height- abs(self.y - other.y))**2)
        d_xy = math.sqrt((self.width - abs(self.x - other.x))**2
                        + (self.height - abs(self.y - other.y))**2)

        r = self.radius + other.radius

        return d <= r or d_x <= r or d_y <= r or d_xy <= r

    def __repr__(self):
        return "{} {:.1f},{:.1f},{},{}".format(self.obj_type,
                 self.x, self.y, self.angle, self.id)
