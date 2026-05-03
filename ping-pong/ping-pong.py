from pygame import *

'''Описать классы'''
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 85:
            self.rect.y += self.speed
    
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 85:
            self.rect.y += self.speed
'''Окно игры'''
win_width = 1376
win_height = 768
window = display.set_mode((win_width, win_height))
win_background = (128, 128, 128)
window.fill(win_background)


'''Вспомогательные переменные и шрифты'''
game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()
font = font.Font(None, 36)
pL_lose = font.render('ИГРОК СЛЕВА ПРОИГРАЛ!', True, (200, 0, 0))
pR_lose = font.render('ИГРОК СПРАВА ПРОИГРАЛ!', True, (200, 0, 0))

'''Игровые объекты'''
player_L = Player('left_rocket.png', 50, 344, 5, 15, 80)
player_R = Player('right_rocket.png', win_width - 50, win_height / 2 - 40, 5, 15, 80)

'''Игровой цикл'''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish == False:
        window.fill(win_background)
        player_L.update_l()
        player_R.update_r()

        player_L.reset()
        player_R.reset()

    display.update()
    clock.tick(FPS)