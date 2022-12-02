import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)
        self.added_bullets_count = 0

    def import_state(self, game_state_filename):
        try:
            game_state_file = open(game_state_filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open {}".
                                    format(game_state_filename))
        
        lines = game_state_file.readlines()
        game_state_file.close()

        check_list = ["width", "height", "score", "spaceship", "fuel",
        "asteroids_count", ["asteroid_small", "asteroid_large"], 
        "bullets_count", ["bullet"], "upcoming_asteroids_count", 
        ["upcoming_asteroid_small", "upcoming_asteroid_large"]]
        
        game_state = []
        j = 0 # track check list
        i = 0 # track line number of file
        while i < len(lines) and j < len(check_list):
            if lines[i].rstrip() == "":
                i += 1
                continue
            try:
                key, value = lines[i].rstrip().split(" ")
            except ValueError:
                raise ValueError("Error: expecting a key and value"\
                                " in line {}".format(key, i+1))
            
            if key == check_list[j]:
                if key == "spaceship":
                    try:
                        x, y, angle, id = value.split(",")
                    except ValueError:
                        raise ValueError("Error: invalid data type"\
                                        " in line {}".format(i+1))
                    try:
                        x = float(x)
                        y = float(y)
                        angle = int(angle)
                        id = int(id)
                    except ValueError:
                        raise ValueError("Error: invalid data type"\
                                        " in line {}".format(i+1))

                    space_object = SpaceObject(x, y, game_state[0][1],
                                     game_state[1][1], angle, key, id)
                    game_state.append((key, space_object))

                elif not "count" in key:
                    try:
                        value = int(value)
                    except ValueError:
                        raise ValueError("Error: invalid data type"\
                                        " in line {}".format(i+1))
                    game_state.append((key, value))

                # after this item in the checklist, 
                # there is a list of SpaceObjects
                elif "count" in key:
                    try:
                        # count: length of list of SpaceObjects
                        count = int(value)
                    except ValueError:
                        raise ValueError("Error: invalid data type"\
                                        " in line {}".format(i+1))

                    game_state.append((key, count))
                    
                    j += 1
                    while count > 0 and i + 1 < len(lines):
                        i += 1
                        count -= 1

                        try:
                            key, value = lines[i].rstrip().split(" ")
                        except ValueError:
                            raise ValueError("Error: expecting a key"\
                                " and value in line {}".format(i+1))

                        try:
                            x, y, angle, id = value.split(",")
                        except ValueError:
                            raise ValueError("Error: invalid data type"\
                                        " in line {}".format(i+1))

                        if key in check_list[j]:
                            try:
                                x = float(x)
                                y = float(y)
                                angle = int(angle)
                                id = int(id)
                            except ValueError:
                                raise ValueError("Error: invalid data type"\
                                            " in line {}".format(i+1))

                            space_object = SpaceObject(x, y, game_state[0][1],
                                         game_state[1][1], angle, key, id)
                            game_state.append((key, space_object))

                        else:
                            raise ValueError("Error: unexpected key: {}"\
                                        " in line {}".format(key, i+1))
                        
                    if count > 0:
                        raise ValueError("Error: game state incomplete")
            else:
                raise ValueError("Error: unexpected key: {} in line {}".
                                format(key, i+1))
            j += 1
            i += 1

        # there are data left in the file, but the checklist is finised
        if i < len(lines):
            raise ValueError("Error: unexpected key: {} in line {}".
                            format(key, i+1))

        # check if the game state file is complete
        is_complete = False
        i = len(game_state) - 1
        while i >= 0:
            if game_state[i][0] == "upcoming_asteroids_count":
                if i + game_state[i][1] == len(game_state) - 1:
                    is_complete = True
                break
            i -= 1

        if not is_complete:
            raise ValueError("Error: game state incomplete")

        self.width = game_state[0][1]
        self.height = game_state[1][1]
        self.score = game_state[2][1]
        self.spaceship = game_state[3][1]
        self.fuel = game_state[4][1]
        self.asteroid_ls = []
        self.bullet_ls = []
        self.upcoming_asteroid_ls = []
        self.initial_fuel = self.fuel

        # add all asteroids to the asteroids_ls
        asteroids_count = game_state[5][1]
        for i in range(6, 6 + asteroids_count):
            self.asteroid_ls.append(game_state[i][1])
        
        # add all bullets to the bullets_ls
        bullets_count = game_state[6 + asteroids_count][1]
        for i in range(7 + asteroids_count, 
                    7 + asteroids_count + bullets_count):
            self.bullet_ls.append(game_state[i][1])

        # add all upcoming asteroids to the upcoming_asteroid_ls
        for i in range(8 + asteroids_count + bullets_count,
                     len(game_state)):
            self.upcoming_asteroid_ls.append(game_state[i][1])


    def export_state(self, game_state_filename):
        f = open(game_state_filename, 'w')

        game_state = [("width", self.width), ("height", self.height),
        ("score", self.score), ("spaceship", self.spaceship),
        ("fuel", self.fuel), ("asteroids_count", len(self.asteroid_ls)),
        ("asteroid_ls", self.asteroid_ls),
        ("bullets_count", len(self.bullet_ls)),
        ("bullet_ls", self.bullet_ls),
        ("upcoming_asteroids_count", len(self.upcoming_asteroid_ls)),
        ("upcoming_asteroid_ls", self.upcoming_asteroid_ls)]

        for i in range(len(game_state)):
            if type(game_state[i][1]) == list:
                for j in range(len(game_state[i][1])):
                    f.write("{}\n".format(game_state[i][1][j].__repr__()))

            elif type(game_state[i][1]) == SpaceObject:
                f.write("{}\n".format(game_state[i][1].__repr__()))

            else:
                f.write("{} {}\n".format(game_state[i][0], game_state[i][1]))

        f.close()
    
    
    def run_game(self):
        while True:
            # 1. Receive player input
            thrust, left, right, bullet  = self.player.action(self.spaceship, 
                    self.asteroid_ls, self.bullet_ls, self.fuel, self.score)

            # 2. Process game logic
            if left and right: # not turn
                if thrust:
                    self.spaceship.move_forward()
            else:
                if left:
                    self.spaceship.turn_left()
                elif right:
                    self.spaceship.turn_right()
                if thrust:
                    self.spaceship.move_forward()

            for i in range(len(self.asteroid_ls)):
                self.asteroid_ls[i].move_forward()

            previous_fuel = self.fuel

            # launch a bullet
            if bullet:
                if self.fuel < config.shoot_fuel_threshold:
                    print("Cannot shoot due to low fuel")
                else:
                    new_bullet = SpaceObject(self.spaceship.x, 
                        self.spaceship.y, self.width, self.height, 
                        self.spaceship.angle, "bullet", 
                        self.added_bullets_count)

                    self.added_bullets_count += 1
                    self.bullet_ls.append(new_bullet)
                    print(self.bullet_ls)
                    self.fuel -= config.bullet_fuel_consumption

            # remove expired bullets and 
            # let the remaining move forward
            i = 0
            while i < len(self.bullet_ls):
                if self.bullet_ls[i].move_count == config.bullet_move_count:
                    self.bullet_ls.pop(i)
                else:
                    self.bullet_ls[i].move_forward()
                    self.bullet_ls[i].move_count += 1
                    i += 1                         

            # print out fuel warning
            self.fuel -= config.spaceship_fuel_consumption
            for i in range(len(config.fuel_warning_threshold)):
                threshold = config.fuel_warning_threshold[i] \
                            * self.initial_fuel / 100
                if self.fuel <= threshold and previous_fuel > threshold:
                    print("{}% fuel warning: {} remaining".
                        format(config.fuel_warning_threshold[i], self.fuel))
                    break
            
            num_collided_asteroids = 0

            # check if bullets has shot (collided with) asteroids
            i = 0
            while i < len(self.bullet_ls):
                j = 0
                while j < len(self.asteroid_ls):
                    if self.bullet_ls[i].collide_with(self.asteroid_ls[j]):
                        num_collided_asteroids += 1
                        if "small" in self.asteroid_ls[j].obj_type:
                            self.score += config.shoot_small_ast_score

                        else: # this is a large asteroid
                            self.score += config.shoot_large_ast_score
                        print("Score: {} \t [Bullet {} has shot asteroid {}]".
                            format(self.score, self.bullet_ls[i].id,
                                 self.asteroid_ls[j].id))

                        self.bullet_ls.pop(i)
                        self.asteroid_ls.pop(j)
                        i -= 1
                        break
                    j += 1
                i += 1

            # check if bullets has shot (collided with) asteroids
            i = 0
            while i < len(self.asteroid_ls):
                if self.spaceship.collide_with(self.asteroid_ls[i]):
                    self.score += config.collide_score
                    print("Score: {} \t [Spaceship collided with asteroid {}]"
                        .format(self.score, self.asteroid_ls[i].id))
                    num_collided_asteroids += 1
                    self.asteroid_ls.pop(i)
                    i -= 1
                i += 1

            # add asteroids to the asteroid_ls
            for i in range(num_collided_asteroids):
                if len(self.upcoming_asteroid_ls) > 0:
                    # remove "upcoming_" in the obj_type
                    self.upcoming_asteroid_ls[0].obj_type = \
                        self.upcoming_asteroid_ls[0].obj_type[9:]

                    self.asteroid_ls.append(self.upcoming_asteroid_ls[0])
                    print("Added asteroid {}".
                        format(self.upcoming_asteroid_ls[0].id))
                    self.upcoming_asteroid_ls.pop(0)

                else:
                    print("Error: no more asteroids available")
                    break

            # 3. Draw the game state on screen using the GUI class
            self.GUI.update_frame(self.spaceship, self.asteroid_ls, 
                            self.bullet_ls, self.score, self.fuel)

            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            # - no more asteroids are available
            if self.fuel < 1 or len(self.upcoming_asteroid_ls) == 0:
                break

        # Display final score
        self.GUI.finish(self.score)
