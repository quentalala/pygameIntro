import pygame
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('First Game!')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SPACE = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH, HEIGHT))

BORDER = pygame.Rect((WIDTH//2 - 10), 0, 10, HEIGHT)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60

HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 100)

VELOCITY = 5
BULLET_VELOCITY = 8
MAX_BULLETS = 6
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load('spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                                                  (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load('spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                                               (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), False, WHITE)
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), False, WHITE)

    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x + VELOCITY >= 0 + 10:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VELOCITY <= (WIDTH / 2) - 5 + 10:  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y + VELOCITY >= 0 + 25:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VELOCITY <= HEIGHT - 20:  # DOWN
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x + VELOCITY >= WIDTH/2 + 10:  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VELOCITY <= WIDTH + 10:  # RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y + VELOCITY >= 0 + 25:  # UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VELOCITY <= HEIGHT - 20:  # DOWN
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):  # Checking if yellow bullets hit red spaceship
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):  # Checking if red bullets hit yellow spaceship
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, False, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(740, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 3
    red_health = 3

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Ensures that frame rate is capped
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow Wins!'

        if yellow_health <= 0:
            winner_text = 'Red Wins!'

        if winner_text != '':
            draw_winner(winner_text)  # WINNER WINNER CHICKEN DINNER
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()


if __name__ == "__main__":
    main()
