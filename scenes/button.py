import pygame

class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

        self.color_idle = (70, 70, 70)
        self.color_hover = (120, 120, 120)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # muda cor se estiver em cima
        if self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_idle

        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # texto centralizado
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # clique esquerdo
                if self.rect.collidepoint(event.pos):
                    return True
        return False