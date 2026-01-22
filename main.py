import pygame
import json

pygame.init()

width = 800
height = 800
game_over = 0
score = 0

tile_size = 40

clock = pygame.time.Clock()
fps = 30

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Platformer')

bg_image = pygame.image.load('images/bg7.png')
bg_rect = bg_image.get_rect()

player_image = pygame.image.load('images/player2.png').convert_alpha()
dead_image = pygame.image.load('images/ghost.png').convert_alpha()

bloque_image = pygame.image.load('images/bloque.png')
nieve_image = pygame.image.load('images/snow.png')
puerta_image = pygame.image.load('images/door.png')
lava_image = pygame.image.load('images/lava.png').convert_alpha()
restart_image = pygame.image.load('images/reinicio.png')
start_image = pygame.image.load('images/start.png')
exit_image = pygame.image.load('images/exit.png')
coin_image = pygame.image.load('images/coin.png')

HEART_HUD_IMAGE = pygame.image.load('images/corazon.png').convert_alpha()
HEART_HUD_IMAGE = pygame.transform.scale(HEART_HUD_IMAGE, (30, 30))

moneda_sonido = pygame.mixer.Sound('sonidos/coin.wav')
lost_sonido = pygame.mixer.Sound ('sonidos/game_over.wav')
salto_sonido = pygame.mixer.Sound ('sonidos/jump.wav')
suspenso_sonido = pygame.mixer.Sound ('sonidos/suspenso.mp3')


with open('levels/level1.json', 'r') as file:
    world_data = json.load(file)

with open('levels/level2.json', 'r') as file:
    second_world_data = json.load(file)

with open('levels/level3.json', 'r') as file:
    third_world_data = json.load(file)

with open('levels/level4.json', 'r') as file:
    four_world_data = json.load(file)


level = 1
max_level = 4
player_lives = 3

def reset_level():
    global world_data, player, game_over, level
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    with open(f'levels/level{level}.json', 'r') as file:
        world_data = json.load(file)
    world = World(world_data, bloque_image, nieve_image, lava_image, exit_group, lava_group)
    player = Player(player_image, dead_image)
    game_over = 0
    return world, player


def draw_text (text, color, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

class Player:
    def __init__(self, player_image, dead_image):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(4):
            img_right = pygame.transform.scale(player_image, (35, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 40 - 70
        self.gravity = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dead_image = dead_image
        self.jumped = False
        self.direction = 1
        self.on_ground = False  # variable de estado
        # se usa para saber si el personaje está en el suelo

    def update(self):
        global game_over, player_lives
        x = 0
        y = 0
        walk_speed = 10

        if game_over == 0:
            key = pygame.key.get_pressed()

            # Se permite saltar solo si está en el suelo
            if key[pygame.K_SPACE] and self.on_ground:
                self.gravity = -15
                self.on_ground = False
                salto_sonido.play()#puedo ponerlo o quitarlo para que suenen los otros sonidos

            if key[pygame.K_LEFT]:
                x -= 5
                self.direction = -1
                self.counter += 1
                suspenso_sonido.play()
            if key[pygame.K_RIGHT]:
                x += 5
                self.direction = 1
                self.counter += 1
                suspenso_sonido.play()

            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]

            if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT]):
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]

            # Aplicar gravedad
            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity

            # Restablecer el on_ground
            self.on_ground = False

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y, self.width, self.height):
                    x = 0
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.height):
                    if self.gravity < 0: #techo
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    else:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.on_ground = True
            self.rect.x += x
            self.rect.y += y

            if self.rect.bottom > height:
                self.rect.bottom = height
                self.on_ground = True
                self.gravity = 0

            if pygame.sprite.spritecollide(self, lava_group, False):
                if player_lives > 1:
                    player_lives -= 1
                    game_over = -2

                else:
                    player_lives = 0
                    game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Lava (pygame.sprite.Sprite):
    def __init__ (self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image,(tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
lava_group = pygame.sprite.Group()

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))

    def draw (self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action

restart_button = Button(width //2, height // 2,restart_image)
start_button = Button(width //2 -150, height // 2,start_image)
exit_button =  Button(width //2 +150, height // 2,exit_image )

class Exit (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale (puerta_image,(tile_size, int (tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
exit_group = pygame.sprite.Group()

class Coin (pygame.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.image = pygame.transform.scale (coin_image, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
coin_group = pygame.sprite.Group()

class World():
    def __init__(self, data, bloque_image, nieve_image, lava_image, exit_group, lava_group):
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2 :
                    images = {
                        1: bloque_image,
                        2: nieve_image,
                    }
                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2), lava_image)
                    lava_group.add(lava)
                if tile == 4:
                    exit = Exit(col_count * tile_size, row_count *tile_size - (tile_size //2))
                    exit_group.add(exit)

                elif tile == 5:
                    coin = Coin (col_count * tile_size + (tile_size // 2),
                                 row_count * tile_size + (tile_size // 2),)
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

world = World(world_data, bloque_image, nieve_image, lava_image, exit_group, lava_group)
player = Player(player_image, dead_image)

run = True
main_menu = True

while run:
    clock.tick(fps)
    display.blit(bg_image, bg_rect)

    if main_menu:
        if start_button.draw():
            main_menu = False
            level = 1
            world, player = reset_level()

        if exit_button.draw():
            run = False

    else:

        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)
        coin_group.draw(display)
        heart_x = width - HEART_HUD_IMAGE.get_width() - 20
        heart_y = 10
        display.blit(HEART_HUD_IMAGE, (heart_x, heart_y))
        text_x = heart_x - 30
        text_y = 10
        draw_text(str(player_lives), (255, 255, 255), 30, text_x, text_y)
        draw_text(str(score), (255, 255, 255), 30, 10, 10)

        if game_over == 0:
            player.update()
            player.draw(display)

            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                suspenso_sonido.stop()
                moneda_sonido.play()


        if game_over == 1:
            level += 1
            if level <= max_level:
                world, player = reset_level()  # Carga el nuevo nivel (2)
            else:
                game_over = 2
                main_menu = True

        elif game_over == -2:
            world, player = reset_level()

        elif game_over == -1:
            suspenso_sonido.stop()
            lost_sonido.play()
            player.image = player.dead_image
            if player.rect.y > 0:
                player.rect.y -= 5
            player.draw(display)

            if restart_button.draw():
                world, player = reset_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()