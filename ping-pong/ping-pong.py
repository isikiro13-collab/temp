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
player_L = Player('сахуралдо.jpg', 50, 344, 5, 15, 80)
player_R = Player('goofy ahh messi.jpg', win_width - 50, win_height / 2 - 40, 5, 15, 80)
ball = GameSprite('Birb.jpg', win_width / 2 - 15, win_height / 2 - 15, 5, 26, 26)

speed_x = 6
speed_y = 6




'''Игровой цикл'''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish == False:
        window.fill(win_background)
        player_L.update_l()
        player_R.update_r()
        '''Перемещение мяча'''
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        '''Отскоки мяча от стен сверху и снизу'''
        if ball.rect.y <= 0 or ball.rect.y >= win_height - 30:
            speed_y *= -1

        '''Отскоки мяча от ракеток'''
        if sprite.collide_rect(player_L, ball) or sprite.collide_rect(player_R, ball):
            speed_x *= -1
            
        '''Проверка, что мяч ушел за край экрана (кто-то из игроков проиграл)'''
        if ball.rect.x <= 0:
            finish = True
            window.blit(pL_lose, (550, 350))
            
        if ball.rect.x >= win_width - 30:
            finish = True
            window.blit(pR_lose, (550, 350))

        player_L.reset()
        player_R.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)