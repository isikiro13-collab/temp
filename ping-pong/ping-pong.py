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
background = transform.scale(image.load('phon.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('jizneradostnyiy-priliv-bodrosti.ogg')
mixer.music.play()

# Загружаем звуки победы для каждого игрока
victory_sound_right = mixer.Sound('pam-pam-pammm.ogg')  # Звук для правого игрока
victory_sound_left = mixer.Sound('siiii-ronaldo.ogg')   # Звук для левого игрока (СИИИИ РОНАЛДО)

'''Вспомогательные переменные и шрифты'''
game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()
font = font.Font(None, 36)
pL_lose = font.render('ИГРОК СЛЕВА ПРОИГРАЛ!', True, (200, 25, 30))
pR_lose = font.render('ИГРОК СПРАВА ПРОИГРАЛ!', True, (50, 200, 100))

# Счетчики отбитий
score_left = 0
score_right = 0
score_font = font.__class__(None, 48)


speed_increased = False

# Переменные для картинки победителя
winner_image_timer = 0
winner = None  # 'left' или 'right'

'''Игровые объекты'''
player_L = Player('сахуралдо.jpg', 60, 344, 5, 40, 150)
player_R = Player('goofy ahh messi.jpg', win_width - 50, win_height / 2 - 40, 5, 40, 150)
ball = GameSprite('Birb.jpg', win_width / 2 - 15, win_height / 2 - 15, 5, 30, 30)

# Загружаем картинки победителей
winner_left_img = transform.scale(image.load('сахуралдо.jpg'), (300, 300))
winner_right_img = transform.scale(image.load('goofy ahh messi.jpg'), (300, 300))

speed_x = 6
speed_y = 6

last_hit_by_left = False
last_hit_by_right = False

'''Игровой цикл'''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        # Нажатие пробела для перезапуска игры
        if e.type == KEYDOWN and e.key == K_SPACE and finish:
            # Сброс всех переменных
            finish = False
            score_left = 0
            score_right = 0
            speed_increased = False
            speed_x = 6
            speed_y = 6
            winner = None
            winner_image_timer = 0
            ball.rect.x = win_width / 2 - 15
            ball.rect.y = win_height / 2 - 15
            player_L.rect.y = 344
            player_R.rect.y = win_height / 2 - 40
            last_hit_by_left = False
            last_hit_by_right = False
            # Включаем фоновую музыку заново
            mixer.music.play()
    
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
        if sprite.collide_rect(player_L, ball) and not last_hit_by_left:
            speed_x *= -1
            score_left += 1
            last_hit_by_left = True
            last_hit_by_right = False
        
        if sprite.collide_rect(player_R, ball) and not last_hit_by_right:
            speed_x *= -1
            score_right += 1
            last_hit_by_right = True
            last_hit_by_left = False
        
        if not sprite.collide_rect(player_L, ball):
            last_hit_by_left = False
        if not sprite.collide_rect(player_R, ball):
            last_hit_by_right = False
            
        # Увеличение скорости, когда оба игрока набрали более 10 отбитий
        if score_left > 10 and score_right > 10 and not speed_increased:
            speed_x += 7 if speed_x > 0 else -7
            speed_y += 7 if speed_y > 0 else -7
            speed_increased = True
            
        '''Проверка, что мяч ушел за край экрана (кто-то из игроков проиграл)'''
        if ball.rect.x <= 0:
            finish = True
            winner = 'right'  # Победил правый игрок
            window.blit(pR_lose, (550, 350))
            mixer.music.stop()  # Останавливаем фоновую музыку
            victory_sound_right.play()  # Воспроизводим звук победы для правого игрока
            
        if ball.rect.x >= win_width - 30:
            finish = True
            winner = 'left'  # Победил левый игрок
            window.blit(pL_lose, (550, 350))
            mixer.music.stop()  # Останавливаем фоновую музыку
            victory_sound_left.play()  # Воспроизводим звук победы для левого игрока (СИИИИ РОНАЛДО)

        window.blit(background, (0, 0))
 # обновление позиции игроков
        player_L.reset()
        player_R.reset()
        ball.reset()
        
        # Отображение счетчиков
        score_text_left = score_font.render(str(score_left), True, (255, 255, 255))
        score_text_right = score_font.render(str(score_right), True, (255, 255, 255))
        window.blit(score_text_left, (50, 20))
        window.blit(score_text_right, (win_width - 80, 20))
    
    else:  # Если игра закончена (finish == True)
        window.blit(background, (0, 0))
        player_L.reset()
        player_R.reset()
        ball.reset()
        
        # Отображаем сообщение о победителе
        if winner == 'left':
            window.blit(pL_lose, (550, 350))
            # Показываем картинку победителя по центру
            if winner_image_timer < 120:  # Показываем 2 секунды (60 FPS * 2)
                img_x = win_width // 2 - winner_left_img.get_width() // 2
                img_y = win_height // 2 - 100
                window.blit(winner_left_img, (img_x, img_y))
                winner_image_timer += 1
        elif winner == 'right':
            window.blit(pR_lose, (550, 350))
            if winner_image_timer < 120:
                img_x = win_width // 2 - winner_right_img.get_width() // 2
                img_y = win_height // 2 - 100
                window.blit(winner_right_img, (img_x, img_y))
                winner_image_timer += 1
        
        # Отображаем финальные счета
        score_text_left = score_font.render(str(score_left), True, (255, 255, 255))
        score_text_right = score_font.render(str(score_right), True, (255, 255, 255))
        window.blit(score_text_left, (50, 20))
        window.blit(score_text_right, (win_width - 80, 20))
        
        # Текст для перезапуска
        restart_text = font.render('Нажмите ПРОБЕЛ для перезапуска', True, (255, 255, 0))
        window.blit(restart_text, (win_width // 2 - 200, win_height - 100))

    display.update()
    clock.tick(FPS)