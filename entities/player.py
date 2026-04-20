import pygame
from settings import GRAVITY, IMAGES


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = IMAGES["cube"]
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(100, 450))

        self.pos_y = float(self.rect.y)
        self.hitbox = pygame.Rect(0, 0, 26, 26)
        self.hitbox.midbottom = (self.rect.centerx, self.rect.bottom - 2)

        self.vel_y = 0
        self.gravity_dir = 1
        self.on_ground = False
        self.mode = "cube"
        self.angle = 0
        self.jump_held = False
        self.trail_timer = 0
        self.portal_cooldown = 0

    def sync_visual(self):
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_blue_hitbox(self):
        return self.hitbox.inflate(6, 6)

    def get_red_hitbox(self):
        return self.hitbox.inflate(-6, -6)

    def update(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        jump_input = keys[pygame.K_SPACE] or keys[pygame.K_UP] or mouse[0]
        just_pressed = jump_input and not self.jump_held

        if self.mode == "cube":
            if self.on_ground and just_pressed:
                self.vel_y = -8 * self.gravity_dir
                self.on_ground = False

            self.vel_y += GRAVITY * self.gravity_dir
            self.pos_y += self.vel_y
            self.hitbox.y = round(self.pos_y)

            if not self.on_ground:
                self.angle -= 5.5 * self.gravity_dir
            else:
                self.angle = round(self.angle / 90) * 90

            self.image = pygame.transform.rotate(self.original_image, self.angle)

        elif self.mode == "ship":
            if jump_input:
                self.vel_y -= 0.5 * self.gravity_dir
            else:
                self.vel_y += 0.3 * self.gravity_dir

            self.vel_y = max(-6, min(6, self.vel_y))
            self.pos_y += self.vel_y
            self.hitbox.y = round(self.pos_y)
            self.angle = -self.vel_y * 4
            self.image = pygame.transform.rotate(IMAGES["ship"], self.angle)

        self.on_ground = False
        self.jump_held = jump_input
        self.trail_timer += 1
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1
        self.sync_visual()
