import pygame
import sys
from player.player import PlayerTank  # Updated import

pygame.init()

# -------------------- Screen --------------------
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Neon Horizon")

# -------------------- Paths --------------------
FONT_PATH = "/Volumes/KwunTing Lee/DCB/guess/ode/ames/Neon Horizon Github/neo_sci_fi/neo_scifi.ttf"

# -------------------- Colors --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_CYAN = (0, 255, 255)
DARK_BLUE = (0, 50, 150)
GRAY = (80, 80, 80)
LIGHT_GRAY = (150, 150, 255)

# -------------------- Fonts --------------------
def get_title_font(height):
    return pygame.font.Font(FONT_PATH, max(height // 10, 40))

def get_button_font(height):
    return pygame.font.Font(FONT_PATH, max(height // 20, 30))

# -------------------- Buttons --------------------
class Button:
    def __init__(self, text, rel_x, rel_y, rel_w, rel_h):
        self.text = text
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.rel_w = rel_w
        self.rel_h = rel_h
        self.rect = pygame.Rect(0,0,0,0)
        self.color = GRAY

    def update_rect(self, screen_width, screen_height):
        self.rect.width = int(self.rel_w * screen_width)
        self.rect.height = int(self.rel_h * screen_height)
        self.rect.centerx = int(self.rel_x * screen_width)
        self.rect.centery = int(self.rel_y * screen_height)

    def draw(self, surface, font):
        rect_to_draw = self.rect
        if self.is_hovered():
            w, h = self.rect.width * 1.1, self.rect.height * 1.1
            rect_to_draw = pygame.Rect(self.rect.centerx - w/2, self.rect.centery - h/2, w, h)
        pygame.draw.rect(surface, self.color, rect_to_draw, border_radius=10)
        label = font.render(self.text, True, WHITE)
        label_rect = label.get_rect(center=rect_to_draw.center)
        surface.blit(label, label_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered()

start_button = Button("Start Game", 0.5, 0.35, 0.25, 0.08)
settings_button = Button("Settings", 0.5, 0.5, 0.25, 0.08)
quit_button = Button("Quit", 0.5, 0.65, 0.25, 0.08)
back_button = Button("Back", 0.1, 0.85, 0.15, 0.08)

menu_active = True
settings_active = False
game_active = False
countdown_active = False
countdown_start_time = 0
countdown_number = 3

bg_offset = 0
clock = pygame.time.Clock()

# -------------------- Main Loop --------------------
player = PlayerTank(start_pos=(WIDTH//2, HEIGHT//2))
running = True
while running:
    dt = clock.tick(60)
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()
    title_font = get_title_font(HEIGHT)
    button_font = get_button_font(HEIGHT)
    for btn in [start_button, settings_button, quit_button, back_button]:
        btn.update_rect(WIDTH, HEIGHT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if menu_active:
            if start_button.is_clicked(event):
                menu_active = False
                countdown_active = True
                countdown_start_time = pygame.time.get_ticks()
            if settings_button.is_clicked(event):
                menu_active = False
                settings_active = True
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        if settings_active:
            if back_button.is_clicked(event):
                settings_active = False
                menu_active = True

    # Countdown
    if countdown_active:
        elapsed = (pygame.time.get_ticks() - countdown_start_time) // 1000
        number = countdown_number - elapsed
        font = pygame.font.Font(FONT_PATH, max(HEIGHT // 5, 80))
        text = str(number) if number > 0 else "GAME STARTED!"
        color = WHITE if number > 0 else NEON_CYAN
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_surf, text_rect)
        if elapsed >= countdown_number:
            countdown_active = False
            game_active = True

    # Background animation
    bg_offset += 2
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, DARK_BLUE, (0, y + bg_offset % 40), (WIDTH, y + bg_offset % 40), 2)

    # Draw screens
    if menu_active:
        title_surface = title_font.render("NEON HORIZON", True, NEON_CYAN)
        screen.blit(title_surface, title_surface.get_rect(center=(WIDTH//2, HEIGHT//6)))
        for button in [start_button, settings_button, quit_button]:
            button.color = LIGHT_GRAY if button.is_hovered() else GRAY
            button.draw(screen, button_font)

    elif settings_active:
        title_surface = title_font.render("SETTINGS", True, NEON_CYAN)
        screen.blit(title_surface, title_surface.get_rect(center=(WIDTH//2, HEIGHT//6)))
        back_button.color = LIGHT_GRAY if back_button.is_hovered() else GRAY
        back_button.draw(screen, button_font)

    elif game_active:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update_turret(pygame.mouse.get_pos())
        player.draw(screen)

    pygame.display.flip()
