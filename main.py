# GOAL: create a screen saver with firework effects
import random

import pygame as pg
import pygame.time

pg.init()
screen = pg.display.set_mode()
clock = pg.time.Clock()
running = True
frametime = 0
fireworkgroup = pg.sprite.Group()
sparks = pg.sprite.Group()
pygame.mouse.set_visible(False)


class particle(pg.sprite.Sprite):
    def __init__(self, parent, type):
        super().__init__()
        self.layer = 2
        self.parent = parent
        self.type = type
        self.x = self.parent.rect.x + random.randrange(int(self.parent.width))
        self.y = parent.rect.y + random.randrange(int(self.parent.height))
        self.yacel = self.xacel = 0
        self.add(sparks)
        if type == "streamer":
            self.height = 1.5
            self.width = 2.5
            self.y = parent.rect.y + self.parent.height
            if parent.type == "fountain":
                self.image = pg.Surface((self.width, self.height))
                self.yacel = random.randrange(-5, -2)
                self.xacel = random.randrange(-10, 10)
                self.lifespan = 30

            elif parent.type != "explode":
                self.image = pg.Surface((self.width, self.height))
                self.yacel = random.randrange(2, 5)
                self.xacel = random.randrange(-2, 2)
                self.lifespan = parent.yacel // 3 + ((parent.rect.y - parent.killspace) // 15)

            else:
                self.image = pg.Surface((self.width, self.height))
                self.yacel = random.randrange(10, 50) / 10
                self.xacel = random.randrange(-5, 5) / 2
                while self.xacel == 0:
                    self.xacel = random.randrange(-5, 5) / 2
                self.lifespan = 40
            self.image.fill("orange")
        if type == "explode":
            self.height = 3.5
            self.width = 2
            self.image = pg.Surface((self.width, self.height))
            self.image.fill(self.parent.color)
            self.yacel = random.randrange(-100, 100)
            self.xacel = random.randrange(-100, 100)
            self.lifespan = random.randrange(20, 100)
            if parent.type == "standard":
                self.lifespan /= 1.9
                self.xacel /= 2
                self.yacel /= 2
            elif parent.type == "extra":
                self.lifespan *= 1.5
            elif parent.type == "small":
                self.lifespan /= 4
                self.xacel /= 2.5
                self.yacel /= 2.5
            elif parent.type == "sparkle":
                self.lifespan *= 1.5
                self.xacel /= 10
                self.yacel /= 10
        self.lifespan -= (abs(self.yacel) + abs(self.xacel))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        if self.type == "explode":
            self.lifespan += 0
        if not (1 < self.rect.x < screen.get_width() - 1):
            self.xacel /= -1.5
        self.rect.x += self.xacel
        if not (1 < self.rect.y < screen.get_height() - 1):
            self.yacel /= -1.5
        self.rect.y += self.yacel
        self.lifespan -= 1
        if self.lifespan <= 0:
            if self.parent.type == "sparkle" and self.type == "explode":
                for _ in range(20):
                    particle(self, "streamer")
                    pass
            self.kill()


class firework(pg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.x = random.randrange(0, screen.get_width())
        self.y = screen.get_height() - 10
        if type == "standard":
            self.width = 8
            self.height = 8
            self.color = "yellow"
            self.killspace = screen.get_height() // random.randrange(2, 5)
            self.yacel = random.randrange(5, 7)
            self.xacel = random.randrange(-1, 1)
            if self.x > ((screen.get_width()) * 4 // 5):
                self.xacel = -1.75
            elif self.x < (screen.get_width() // 5):
                self.xacel = 1.5
        elif type == "extra":
            self.width = 10
            self.height = 10
            self.color = "blue"
            self.killspace = screen.get_height() // 6
            self.yacel = 10
            self.xacel = random.randrange(-1, 1)
            if self.x > ((screen.get_width()) * 4 // 5):
                self.xacel = -1.75
            elif self.x < (screen.get_width() // 5):
                self.xacel = 1.5
        elif type == "fountain":
            self.width = 10
            self.height = 10
            self.x = random.randrange((screen.get_width() // 10), screen.get_width() - 100)
            self.color = "brown"
            self.timer = random.randrange(20, 100)
        elif type == "small":
            self.width = 4
            self.height = 4
            self.color = "red"
            self.killspace = screen.get_height() // 1.75
            self.yacel = random.randrange(3, 5)
            self.xacel = random.randrange(-1, 1)
            if self.x > ((screen.get_width()) * 4 // 5):
                self.xacel = -1
            elif self.x < (screen.get_width() // 5):
                self.xacel = 1
        elif type == "sparkle":
            self.width = 20
            self.height = 20
            self.color = "white"
            self.killspace = screen.get_height() // 8
            self.yacel = 1
            self.xacel = 0
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.add(fireworkgroup)

    def update(self):
        if self.type != "fountain":
            self.rect.x += self.xacel
            self.rect.y -= self.yacel
            if self.rect.y < self.killspace:
                for _ in range(random.randrange(400, 600)):
                    particle(self, "explode")
                self.kill()
            for _ in range(random.randrange(1, 3)):
                particle(self, "streamer")
        else:
            if self.timer != 0:
                for _ in range(50):
                    particle(self, "streamer")
                self.timer -= 1
            else:
                self.kill()


def fire():
    for _ in range(random.randrange(2, 4)):
        type = random.randrange(100)

        if type >= 94:
            firework("extra")
        elif type >= 89:
            firework("sparkle")
        elif type >= 59:
            firework("fountain")
        elif type >= 29:
            firework("standard")
        elif type >= 0:
            firework("small")


while running:
    for event in pg.event.get():
        if event.type == 768:
            running = False

    screen.fill("black")
    firecall = random.randrange(99, 300, 3) // 3
    if len(fireworkgroup.sprites()) < 4:
        fire()
    sparks.update()
    sparks.draw(screen)
    fireworkgroup.update()
    fireworkgroup.draw(screen)
    pg.display.flip()

    clock.tick(30)
    frametime += 1
pg.quit()
