import math
import config

class Player:
    def __init__(self):
        self.moves = []
        self.i = -1 # track index in the self.moves

    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):
        if len(asteroid_ls) == 0:
            return (False, False, False, False)
        
        thrust = False
        left = False
        right = False
        bullet = False
  
        if self.i == -1:
            # find the closest asteroid to the spaceship
            closest_asteroid = asteroid_ls[0]
            min_distance = math.sqrt((spaceship.x - asteroid_ls[0].x)**2 
                        + (spaceship.y - asteroid_ls[0].y)**2)

            i = 1
            while i < len(asteroid_ls):
                distance = math.sqrt((spaceship.x - asteroid_ls[i].x)**2 
                        + (spaceship.y - asteroid_ls[i].y)**2)

                if distance < min_distance or (distance == min_distance 
                        and asteroid_ls[i].obj_type == "asteroid_small"):
                    min_distance = distance
                    closest_asteroid = asteroid_ls[i]

                i += 1
            
            if min_distance < config.speed["bullet"]:
                return (False, False, False, True)

            self.predict_moves(spaceship, closest_asteroid, bullet_ls)
            self.i = 0
            

        if self.i == len(self.moves) - 1:
            bullet = True
            
        if self.moves[self.i] == "left":
            left = True
            self.i += 1
        elif self.moves[self.i] == "right":
            right = True
            self.i += 1
        else:# self.moves[self.i] = "thrust"
            thrust = True
            self.i += 1
        
        if self.i == len(self.moves):
            self.i = -1

        return (thrust, left, right, bullet)


    def predict_moves(self, spaceship, closest_asteroid, bullet_ls):
        frames = 1
        while True:
            # find position of the asteroid after "frames" forward moves
            ast_speed = config.speed[closest_asteroid.obj_type]
            asteroid_x = closest_asteroid.x
            asteroid_y = closest_asteroid.y
            for i in range(frames):
                asteroid_x += ast_speed * \
                            math.cos(math.radians(closest_asteroid.angle))
                asteroid_y -= ast_speed * \
                            math.sin(math.radians(closest_asteroid.angle))
                asteroid_x %= spaceship.width
                asteroid_y %= spaceship.height

            # calculate angle between vectors Ox and spaceship-asteroid
            v_x = asteroid_x - spaceship.x
            v_y = asteroid_y - spaceship.y
            angle = math.degrees(math.acos(v_x/math.sqrt(v_x**2 + v_y**2)))
            if spaceship.y < closest_asteroid.y:
                angle = 360 - angle

            # identify the spaceship need to turn left or right
            turn = ""
            if abs(angle - spaceship.angle) <= 180:
                turning_angle = abs(angle - spaceship.angle)
                if angle > spaceship.angle:
                    turn = "left"
                if angle < spaceship.angle:
                    turn = "right"
            else:
                turning_angle = 360 - abs(angle - spaceship.angle)
                if angle < spaceship.angle:
                    turn = "left"
                if angle > spaceship.angle:
                    turn = "right"

            # turn_steps + thrust_steps = total frames
            turn_steps = round(turning_angle/config.angle_increment)
            thrust_steps = frames - turn_steps
            if thrust_steps < 0:
                frames += 1
                continue

            # calculating the spaceship's angle after turn_steps turns
            new_spaceship_angle = spaceship.angle
            if turn == "left":
                for i in range(turn_steps):
                    new_spaceship_angle += config.angle_increment
                    new_spaceship_angle %= 360

            elif turn == "right":
                for i in range(turn_steps):
                    new_spaceship_angle -= config.angle_increment
                    new_spaceship_angle %= 360
                
            # find the positions of the spaceship 
            # after thrust_steps forward moves
            speed = config.speed["spaceship"]
            new_spaceship_x = spaceship.x
            new_spaceship_y = spaceship.y
            for i in range(thrust_steps):
                new_spaceship_x += speed * \
                            math.cos(math.radians(new_spaceship_angle))
                new_spaceship_y -= speed * \
                            math.sin(math.radians(new_spaceship_angle))
                new_spaceship_x %= spaceship.width
                new_spaceship_y %= spaceship.height

            # find the distance between the spaceship and asteroid
            new_distance = math.sqrt((new_spaceship_x - asteroid_x)**2
                        + (new_spaceship_y - asteroid_y)**2)

            if closest_asteroid.obj_type == "asteroid_small":
                distance_threshold = 3
            else:
                distance_threshold = 5

            if new_distance < distance_threshold * config.speed["bullet"]:
                self.moves = [turn] * turn_steps + ["thrust"] * thrust_steps
                break

            frames += 1
