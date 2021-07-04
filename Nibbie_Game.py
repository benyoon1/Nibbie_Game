import pygame, sys, os
from pygame.math import Vector2
import random


class Fruit:
    def __init__(self):
        self.randomize()
        self.treat1 = pygame.image.load('Nibbie_Graphics/treat_1.png').convert_alpha()
        self.treat2 = pygame.image.load('Nibbie_Graphics/treat_2.png').convert_alpha()
        self.treat3 = pygame.image.load('Nibbie_Graphics/treat_3.png').convert_alpha()
        self.random_treat()

    def random_treat(self):
        self.treat = random.choice([self.treat1, self.treat2, self.treat3])

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(self.treat, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Nibbie:
    def __init__(self):
        self.body = [Vector2(5, 5), Vector2(4, 5)]
        self.direction = Vector2(0, 0)
        self.poop_pos = []
        self.update_poop = False
        self.poop_time = 100

        self.head_up = pygame.image.load('Nibbie_Graphics/nibbie_up.png').convert_alpha()
        self.head_down = pygame.image.load('Nibbie_Graphics/nibbie_down.png').convert_alpha()
        self.head_right = pygame.image.load('Nibbie_Graphics/nibbie_right.png').convert_alpha()
        self.head_left = pygame.image.load('Nibbie_Graphics/nibbie_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Nibbie_Graphics/nibbie_db.png').convert_alpha()
        self.tail_down = pygame.image.load('Nibbie_Graphics/nibbie_ub.png').convert_alpha()
        self.tail_right = pygame.image.load('Nibbie_Graphics/nibbie_rb.png').convert_alpha()
        self.tail_left = pygame.image.load('Nibbie_Graphics/nibbie_lb.png').convert_alpha()

        self.poop_up = pygame.image.load('Nibbie_Graphics/nibbie_db_poop.png').convert_alpha()
        self.poop_down = pygame.image.load('Nibbie_Graphics/nibbie_ub_poop.png').convert_alpha()
        self.poop_right = pygame.image.load('Nibbie_Graphics/nibbie_rb_poop.png').convert_alpha()
        self.poop_left = pygame.image.load('Nibbie_Graphics/nibbie_lb_poop.png').convert_alpha()

        self.poop = pygame.image.load('Nibbie_Graphics/poop.png').convert_alpha()

    def draw_nibbie(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        if self.direction != Vector2(0, 0):
            self.update_poop_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == 1:
                screen.blit(self.tail, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[0] - self.body[1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def update_poop_graphics(self):
        if self.update_poop:
            if self.poop_time > 0:
                tail_relation = self.body[0] - self.body[1]
                if tail_relation == Vector2(1, 0):
                    self.tail = self.poop_right
                elif tail_relation == Vector2(-1, 0):
                    self.tail = self.poop_left
                elif tail_relation == Vector2(0, 1):
                    self.tail = self.poop_up
                elif tail_relation == Vector2(0, -1):
                    self.tail = self.poop_down
                self.poop_time -= 1
            elif self.poop_time == 0:
                self.poop_time = 100
                self.update_poop = False

    def move_nibbie(self):
        if self.direction == Vector2(0, 0):
            self.body = [Vector2(5, 5), Vector2(4, 5)]
        else:
            self.body[0] += self.direction
            self.body[1] = self.body[0] - self.direction

    def draw_nibbie_poop(self):
        if self.direction != Vector2(0, 0):
            for rect in self.poop_pos:
                x_poop = int(rect.x * cell_size)
                y_poop = int(rect.y * cell_size)
                poop_rect = pygame.Rect(x_poop, y_poop, cell_size, cell_size)
                screen.blit(self.poop, poop_rect)
        else:
            pass

    def spawn_nibbie_poop(self):
        self.poop_pos.append(Vector2(self.body[1].x, self.body[1].y))


class Main():
    def __init__(self):
        self.nibbie = Nibbie()
        self.fruit = Fruit()
        pygame.mixer.init()
        self.play_background_music()
        self.score = 0
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        self.speed = 200
        self.reset_poop = False

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.nibbie.draw_nibbie()
        self.draw_score()
        self.nibbie.draw_nibbie_poop()

    def check_collision(self):
        if self.nibbie.body[0] == self.fruit.pos:
            self.fruit.random_treat()
            self.crunch_sound.play()
            self.score += 1
            self.speed -= 10
            self.fruit.randomize()
            self.check_poop_treat_location()

    def check_poop_treat_location(self):
        for i in self.nibbie.poop_pos:
            if self.fruit.pos == i:
                self.fruit.randomize()

    def update(self):
        self.nibbie.move_nibbie()
        self.reset()
        self.check_collision()

    def play_background_music(self):
        pygame.mixer.music.load('Sound/Nibbie Song.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, 0)

    def draw_score(self):
        score_surface = game_font.render(str(self.score), True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 30)
        score_y = int(cell_size * cell_number - 30)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.treat.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, BISQUE, bg_rect, 4)
        screen.blit(score_surface, score_rect)
        screen.blit(self.fruit.treat, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def reset(self):
        if not 0 <= self.nibbie.body[0].x < cell_number or not 0 <= self.nibbie.body[0].y < cell_number:
            self.reset_it()

        else:
            for i in self.nibbie.poop_pos:
                if self.nibbie.body[0] == i:
                    self.reset_it()

    def reset_it(self):
        self.nibbie.body = [Vector2(5, 5), Vector2(4, 5)]
        self.nibbie.direction = Vector2(0, 0)
        self.score = 0
        self.nibbie.poop_pos = []
        self.fruit.randomize()
        self.reset_poop = False


pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()
cell_number = 10
cell_size = 40
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
BISQUE = pygame.Color('bisque')

main_game = Main()

SCREEN_UPDATE = pygame.USEREVENT
NIBBIE_POOP = pygame.USEREVENT + 1
pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
pygame.time.set_timer(NIBBIE_POOP, main_game.speed * 20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == NIBBIE_POOP:
            main_game.nibbie.spawn_nibbie_poop()
            main_game.nibbie.update_poop = True
        if event.type == pygame.KEYDOWN:
            # main_game.reset_poop = True
            if event.key == pygame.K_UP:
               if main_game.nibbie.direction.y != 1:
                    main_game.nibbie.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
               if main_game.nibbie.direction.x != -1:
                    main_game.nibbie.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
               if main_game.nibbie.direction.y != -1:
                    main_game.nibbie.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
               if main_game.nibbie.direction.x != 1:
                    main_game.nibbie.direction = Vector2(-1, 0)
        # if main_game.reset_poop:
        #     main_game.poop_speed = main_game.speed * 10
        #     pygame.time.set_timer(NIBBIE_POOP, main_game.poop_speed)
        # if not main_game.reset_poop:
        #     pygame.time.set_timer(NIBBIE_POOP, 0)

    screen.fill(BISQUE)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)


