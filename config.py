game_name = "INFO1110-Cosmic-Warrior"
frame_delay = 0.03  # seconds between each frame (0.03 = ~33 fps)

radius = {"spaceship": 12,
          "bullet": 3,
          "asteroid_small": 16,
          "asteroid_large": 32}

angle_increment = 15

speed = {"spaceship": 10,
          "bullet": 30,
          "asteroid_small": 3,
          "asteroid_large": 3}

bullet_move_count = 5

shoot_small_ast_score = 150
shoot_large_ast_score = 100
collide_score = -100
shoot_fuel_threshold = 10
fuel_warning_threshold = (75, 50, 25)

spaceship_fuel_consumption = 1
bullet_fuel_consumption = 2

            # speed = config.speed["bullet"]
            # bullet_x = new_spaceship_x
            # bullet_y = new_spaceship_y
            # bullet_angle = new_spaceship_angle
            # for i in range(4):
            #     bullet_x += speed * math.cos(math.radians(bullet_angle))
            #     bullet_y -= speed * math.sin(math.radians(bullet_angle))
            #     bullet_x %= spaceship.width
            #     bullet_y %= spaceship.height
            #     d = math.sqrt((bullet_x - asteroid_x)**2 + (bullet_y - asteroid_y)**2)
            #     d_x = math.sqrt((spaceship.width - abs(bullet_x - asteroid_x))**2 
            #             + (bullet_y - asteroid_y)**2)
            #     d_y = math.sqrt((bullet_x - asteroid_x)**2
            #             + (spaceship.height- abs(bullet_y - asteroid_y))**2)
            #     d_xy = math.sqrt((spaceship.width - abs(bullet_x - asteroid_x))**2
            #             + (spaceship.height - abs(bullet_y - asteroid_y))**2)
            #     r = config.radius[closest_asteroid.obj_type] + config.radius["bullet"]
            #     if d <= r or d_x <= r or d_y <= r or d_xy <= r:
            #         self.moves = [turn] * turn_steps + ["thrust"] * thrust_steps
            #         return

