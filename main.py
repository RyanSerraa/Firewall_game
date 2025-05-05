import pygame
import sys
import os

# Estados do jogo
MENU = 'menu'
PLAYING = 'playing'

# Função para compatibilidade com PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # quando empacotado
    except AttributeError:
        base_path = os.path.abspath(".")  # modo normal
    return os.path.join(base_path, relative_path)

def draw_world_map(screen, width, height, mapa_img):
    screen.blit(mapa_img, (0, 0))

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FIREWALL - Menu Principal")

    # Cores
    COLOR_BG_TOP = (30, 0, 60)
    COLOR_BG_BOTTOM = (90, 0, 150)
    COLOR_PRIMARY = (128, 0, 255)
    COLOR_ACCENT = (0, 255, 255)
    COLOR_HIGHLIGHT = (255, 0, 255)
    COLOR_TEXT = (255, 255, 255)

    font = pygame.font.Font(None, 48)

    buttons = ["Iniciar Jogo", "Sair"]
    button_rects = []
    btn_w, btn_h = 300, 60
    spacing = 20
    total_h = len(buttons) * btn_h + (len(buttons) - 1) * spacing
    start_y = (HEIGHT - total_h) // 2

    for i, text in enumerate(buttons):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + spacing)
        rect = pygame.Rect(x, y, btn_w, btn_h)
        button_rects.append((rect, text))

    game_state = MENU

    # Carrega e redimensiona imagem
    mapa_path = resource_path("mapaMundi.png")
    mapa_img = pygame.image.load(mapa_path)
    mapa_img = pygame.transform.scale(mapa_img, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if game_state == MENU:
                for rect, text in button_rects:
                    if rect.collidepoint(mx, my):
                        if text == "Sair":
                            running = False
                        elif text == "Iniciar Jogo":
                            game_state = PLAYING
            elif game_state == PLAYING:
                back_rect = pygame.Rect(20, 20, 100, 40)
                if back_rect.collidepoint(mx, my):
                    game_state = MENU

        if game_state == MENU:
            for i in range(HEIGHT):
                t = i / HEIGHT
                r = int(COLOR_BG_TOP[0] * (1 - t) + COLOR_BG_BOTTOM[0] * t)
                g = int(COLOR_BG_TOP[1] * (1 - t) + COLOR_BG_BOTTOM[1] * t)
                b = int(COLOR_BG_TOP[2] * (1 - t) + COLOR_BG_BOTTOM[2] * t)
                pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

            mx, my = pygame.mouse.get_pos()
            for rect, text in button_rects:
                color = COLOR_HIGHLIGHT if rect.collidepoint(mx, my) else COLOR_PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=12)
                pygame.draw.rect(screen, COLOR_ACCENT, rect, 3, border_radius=12)
                txt_surf = font.render(text, True, COLOR_TEXT)
                txt_rect = txt_surf.get_rect(center=rect.center)
                screen.blit(txt_surf, txt_rect)

        elif game_state == PLAYING:
            draw_world_map(screen, WIDTH, HEIGHT, mapa_img)

            back_rect = pygame.Rect(20, 20, 100, 40)
            pygame.draw.rect(screen, COLOR_PRIMARY, back_rect, border_radius=8)
            pygame.draw.rect(screen, COLOR_ACCENT, back_rect, 2, border_radius=8)
            back_font = pygame.font.Font(None, 30)
            back_text = back_font.render("Voltar", True, COLOR_TEXT)
            back_text_rect = back_text.get_rect(center=back_rect.center)
            screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
