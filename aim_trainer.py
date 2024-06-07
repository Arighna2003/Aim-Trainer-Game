import math
import random
import time
import pygame
import os
from os.path import join

pygame.init()

WIDTH, HEIGHT = 1000, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (30, 30, 30)
LIVES = 10
TOP_BAR_HEIGHT = 60

LABEL_FONT = pygame.font.SysFont("arial", 24, bold=True)
BUTTON_FONT = pygame.font.SysFont("arial", 30, bold=True)

# Load target images for all levels
TARGET_IMG_LEVEL1 = pygame.image.load('assets/target/ball1.png')
TARGET_IMG_LEVEL1 = pygame.transform.scale(TARGET_IMG_LEVEL1, (100, 100))

TARGET_IMG_LEVEL2 = pygame.image.load('assets/target/ball2.png')
TARGET_IMG_LEVEL2 = pygame.transform.scale(TARGET_IMG_LEVEL2, (100, 100))

TARGET_IMG_LEVEL3 = pygame.image.load('assets/target/ball3.png')
TARGET_IMG_LEVEL3 = pygame.transform.scale(TARGET_IMG_LEVEL3, (100, 100))

# Load hit sound
HIT_SOUND1 = pygame.mixer.Sound('assets/sounds/hit2.wav')
HIT_SOUND2 = pygame.mixer.Sound('assets/sounds/hit1.wav')
HIT_SOUND3 = pygame.mixer.Sound('assets/sounds/hit3.wav')


class Target:
    MAX_SIZE = 30
    GROWTH_RATE1 = 0.1
    GROWTH_RATE2 = 0.15
    GROWTH_RATE3 = 0.25

    def __init__(self, x, y, img, growth_rate):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        self.img = img
        self.growth_rate = growth_rate

    def update(self):
        if self.size + self.growth_rate >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.growth_rate
        else:
            self.size -= self.growth_rate

    def draw(self, win):
        if self.size > 0:
            target_img = pygame.transform.scale(
                self.img, (int(self.size * 2), int(self.size * 2)))

            win.blit(target_img, (self.x - self.size, self.y - self.size))

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size

    def is_overlapping(self, other):
        dis = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return dis < self.size + other.size + TARGET_PADDING


class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 100)
        self.text = text
        self.action = action
        self.hover_color = (150, 150, 150)

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, self.hover_color, self.rect)
            if click[0] == 1 and self.action is not None:
                self.action()
        else:
            pygame.draw.rect(win, self.color, self.rect)

        text_surface = BUTTON_FONT.render(self.text, True, (255, 255, 255))
        win.blit(text_surface, (self.rect.x + (self.rect.width / 2 - text_surface.get_width() / 2),
                 self.rect.y + (self.rect.height / 2 - text_surface.get_height() / 2)))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            if click[0] == 1:
                return True
        return False


def get_background(name):
    image = pygame.image.load(join("assets", "background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(win, targets, background, bg_image):
    for tile in background:
        win.blit(bg_image, tile)

    for target in targets:
        target.draw(win)


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, (50, 50, 50), (0, 0, WIDTH, TOP_BAR_HEIGHT))
    pygame.draw.line(win, (200, 200, 200), (0, TOP_BAR_HEIGHT),
                     (WIDTH, TOP_BAR_HEIGHT), 2)

    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, (255, 255, 255))

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, (255, 255, 255))

    hits_label = LABEL_FONT.render(
        f"Hits: {targets_pressed}", 1, (255, 255, 255))

    lives_label = LABEL_FONT.render(
        f"Lives: {LIVES - misses}", 1, (255, 255, 255))

    win.blit(time_label, (10, 10))
    win.blit(speed_label, (220, 10))
    win.blit(hits_label, (440, 10))
    win.blit(lives_label, (660, 10))


def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, (255, 255, 255))

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, (255, 255, 255))

    hits_label = LABEL_FONT.render(
        f"Hits: {targets_pressed}", 1, (255, 255, 255))

    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(
        f"Accuracy: {accuracy}%", 1, (255, 255, 255))
    score_label = LABEL_FONT.render(
        f"Score: {(10*targets_pressed)-((clicks-targets_pressed)*5)}", 1, (255, 255, 255))

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    win.blit(score_label, (get_middle(score_label), 200))

    button = Button(WIDTH // 2 - 75, 500, 150, 50, "Next Level", action=None)
    button.draw(win)

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if button.is_clicked():
                return True  # Proceed to the next level

    return False


def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2


def level_one():
    run = True
    targets = []
    clock = pygame.time.Clock()
    background, bg_image = get_background(
        "bkg3.png")  # Level 1 background

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                for _ in range(100):  # Attempt to find a non-overlapping position
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(
                        TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    new_target = Target(
                        x, y, TARGET_IMG_LEVEL1, Target.GROWTH_RATE1)
                    if all(not new_target.is_overlapping(target) for target in targets):
                        targets.append(new_target)
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
                HIT_SOUND1.play()

        if misses >= LIVES:
            run = False

        draw(WIN, targets, background, bg_image)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    return targets_pressed, clicks, time.time() - start_time


def level_two():
    run = True
    targets = []
    clock = pygame.time.Clock()
    background, bg_image = get_background(
        "bkg1.png")  # Level 2 background

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                for _ in range(100):  # Attempt to find a non-overlapping position
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(
                        TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    new_target = Target(
                        x, y, TARGET_IMG_LEVEL2, Target.GROWTH_RATE2)
                    if all(not new_target.is_overlapping(target) for target in targets):
                        targets.append(new_target)
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
                HIT_SOUND2.play()

        if misses >= LIVES:
            run = False

        draw(WIN, targets, background, bg_image)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    return targets_pressed, clicks, time.time() - start_time


def level_three():
    run = True
    targets = []
    clock = pygame.time.Clock()
    background, bg_image = get_background(
        "bkg2.png")  # Level 3 background

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                for _ in range(100):  # Attempt to find a non-overlapping position
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(
                        TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    new_target = Target(
                        x, y, TARGET_IMG_LEVEL3, Target.GROWTH_RATE3)
                    if all(not new_target.is_overlapping(target) for target in targets):
                        targets.append(new_target)
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
                HIT_SOUND3.play()

        if misses >= LIVES:
            run = False

        draw(WIN, targets, background, bg_image)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    end_screen(WIN, elapsed_time, targets_pressed, clicks)
    pygame.quit()


def main():
    targets_pressed, clicks, elapsed_time = level_one()

    # Show the end screen for level one and wait for the button click to proceed to level two
    if end_screen(WIN, elapsed_time, targets_pressed, clicks):
        targets_pressed, clicks, elapsed_time = level_two()

        # Show the end screen for level two and wait for the button click to proceed to level three
        if end_screen(WIN, elapsed_time, targets_pressed, clicks):
            level_three()


if __name__ == "__main__":
    main()
