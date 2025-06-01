import pygame
import sys
import os

# ------------------------------------------------------------
# CONSTANTES E CONFIGURAÇÕES GLOBAIS
# ------------------------------------------------------------
MENU = "menu"
PLAYING = "playing"
PLAYER_SELECT = "player_select"

# ------------------------------------------------------------
# CORES
# ------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_BG_TOP = (30, 0, 60)
COLOR_BG_BOTTOM = (90, 0, 150)
COLOR_PRIMARY = (128, 0, 255)
COLOR_HIGHLIGHT = (255, 0, 255)


# ------------------------------------------------------------
# FUNÇÃO PARA CARREGAMENTO DE RECURSOS COM PyInstaller
# ------------------------------------------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ------------------------------------------------------------
# DADOS DOS PAÍSES (COORDENADAS PARA DESENHO NO MAPA)
# ------------------------------------------------------------
countries = {
    "Nova York": (200, 150),
    "Londres": (400, 120),
    "Tóquio": (650, 180),
    "São Paulo": (300, 400),
    "Joanesburgo": (500, 450),
    "Berlim": (420, 130),
    "Moscou": (550, 100),
    "Pequim": (700, 140),
    "Sydney": (750, 500),
    "Cairo": (480, 200),
    "Toronto": (180, 100),
    "Paris": (380, 110),
    "Seul": (680, 160),
    "Buenos Aires": (320, 450),
    "Mumbai": (600, 250),
}

# Inicialmente, todos os níveis de infecção são zero, apenas para colorir os marcadores
infection_levels = {country: 0 for country in countries}

# ------------------------------------------------------------
# PERFIS DE JOGADOR (utilizados apenas para seleção, sem lógica posterior)
# ------------------------------------------------------------
player_profiles = {
    "Analista": {"base_treatment_power": 2, "treatment_accuracy": 0.7},
    "Especialista": {"base_treatment_power": 3, "treatment_accuracy": 0.5},
    "Hacker Ético": {"base_treatment_power": 1, "treatment_accuracy": 0.9},
}


# ------------------------------------------------------------
# FUNÇÕES DE DESENHO
# ------------------------------------------------------------
def draw_world_map(screen, mapa_img):
    screen.blit(mapa_img, (0, 0))


def draw_countries(screen, font):
    for country, (x, y) in countries.items():
        level = infection_levels[country]
        if level == 0:
            color = (0, 255, 0)
        elif level <= 2:
            color = (255, 255, 0)
        elif level == 3:
            color = (255, 165, 0)
        else:
            color = (200, 0, 0)
        pygame.draw.circle(screen, color, (x, y), 15)
        label = font.render(country, True, BLACK)
        screen.blit(label, (x - label.get_width() // 2, y + 20))


def draw_profile_selection(screen, button_rects, font):
    title = font.render("Selecione seu perfil de jogador", True, WHITE)
    screen.blit(title, ((screen.get_width() - title.get_width()) // 2, 50))
    for rect, text in button_rects:
        color = (
            COLOR_PRIMARY
            if not rect.collidepoint(pygame.mouse.get_pos())
            else COLOR_HIGHLIGHT
        )
        pygame.draw.rect(screen, color, rect, border_radius=8)
        label = font.render(text, True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))


# ------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------------------------------------
def main():
    global game_state, selected_profile

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Firewall Game Simplificado")

    # Fontes
    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)

    # Botões do menu principal
    buttons_menu = ["Iniciar Jogo", "Sair"]
    button_rects_menu = []
    btn_w, btn_h = 300, 60
    spacing = 20
    total_h = len(buttons_menu) * btn_h + (len(buttons_menu) - 1) * spacing
    start_y = (HEIGHT - total_h) // 2 + 50
    for i, text in enumerate(buttons_menu):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + spacing)
        rect = pygame.Rect(x, y, btn_w, btn_h)
        button_rects_menu.append((rect, text))

    # Botões para seleção de perfil
    buttons_profile = list(player_profiles.keys())
    button_rects_profile = []
    total_h2 = len(buttons_profile) * btn_h + (len(buttons_profile) - 1) * spacing
    start_y2 = (HEIGHT - total_h2) // 2
    for i, text in enumerate(buttons_profile):
        x = (WIDTH - btn_w) // 2
        y = start_y2 + i * (btn_h + spacing)
        rect = pygame.Rect(x, y, btn_w, btn_h)
        button_rects_profile.append((rect, text))

    # Imagem do mapa
    mapa_path = resource_path("mapaMundi.png")
    mapa_img = pygame.image.load(mapa_path)
    mapa_img = pygame.transform.scale(mapa_img, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True
    game_state = MENU
    selected_profile = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # --- MENU PRINCIPAL ---
                if game_state == MENU:
                    for rect, text in button_rects_menu:
                        if rect.collidepoint(mx, my):
                            if text == "Sair":
                                running = False
                            elif text == "Iniciar Jogo":
                                game_state = PLAYER_SELECT

                # --- SELEÇÃO DE PERFIL ---
                elif game_state == PLAYER_SELECT:
                    for rect, profile_name in button_rects_profile:
                        if rect.collidepoint(mx, my):
                            selected_profile = profile_name
                            # Ao selecionar perfil, transita para estado PLAYING
                            game_state = PLAYING

        # --- DESENHO NA TELA ---
        screen.fill((0, 0, 0))  # fundo PRETO para contraste

        if game_state == MENU:
            # Gradiente de fundo
            for i in range(HEIGHT):
                t = i / HEIGHT
                r = int(COLOR_BG_TOP[0] * (1 - t) + COLOR_BG_BOTTOM[0] * t)
                g = int(COLOR_BG_TOP[1] * (1 - t) + COLOR_BG_BOTTOM[1] * t)
                b = int(COLOR_BG_TOP[2] * (1 - t) + COLOR_BG_BOTTOM[2] * t)
                pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

            title_text = title_font.render("FIREWALL GAME", True, WHITE)
            screen.blit(
                title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
            )

            mx, my = pygame.mouse.get_pos()
            for rect, text in button_rects_menu:
                color = COLOR_HIGHLIGHT if rect.collidepoint(mx, my) else COLOR_PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=12)
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=12)
                txt_surf = font.render(text, True, WHITE)
                screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        elif game_state == PLAYER_SELECT:
            screen.fill((20, 20, 40))
            draw_profile_selection(screen, button_rects_profile, font)

        elif game_state == PLAYING:
            # Desenha o mapa e as cidades sem interação
            draw_world_map(screen, mapa_img)
            draw_countries(screen, small_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
