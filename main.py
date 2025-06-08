import pygame
import sys
import os
import random
from typing import Dict, Tuple, List

# Imports dos módulos de domínio
from domain.enums.tipoAtaque import TipoAtaque
# from domain.enums.cor import Cor
from domain.entities.cidade import Cidade
from domain.entities.controladorEpidemia import ControladorEpidemia
from domain.entities.controladorSurto import ControladorSurto
from domain.entities.infeccao import Infeccao
# from domain.entities.personagem import Personagem
# from domain.entities.cuboAtaque import CuboAtaque

# ------------------------------------------------------------
# CONSTANTES DE ESTADO
# ------------------------------------------------------------
MENU = "menu"
SELECT_COUNT = "select_count"
SELECT_PROFILE = "select_profile"
PLAYING = "playing"

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
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ------------------------------------------------------------
# COORDENADAS SIMPLIFICADAS PARA AS CIDADES
# ------------------------------------------------------------
CITY_COORDS: Dict[str, Tuple[int, int]] = {
    "São Paulo": (300, 400),
    "Nova York": (200, 150),
    "Londres": (400, 120),
    # ... outras cidades conforme domínio
}


# ------------------------------------------------------------
# CONTROLLER DO JOGO (usa as classes do domínio)
# ------------------------------------------------------------
class GameController:
    def __init__(self, player_count: int) -> None:
        self.player_count = player_count
        self.ctrl_epidemia = ControladorEpidemia()
        self.ctrl_surto = ControladorSurto()
        self.cities: Dict[str, Cidade] = {}
        self.infection_deck: List[Infeccao] = []
        self._init_cities()
        self._init_decks()

    def _init_cities(self) -> None:
        for name, coord in CITY_COORDS.items():
            self.cities[name] = Cidade(
                nome=name,
                pais="Brasil",
                tipoAtaque=TipoAtaque.PHISHING,
                cidadesVizinhas=[],
                cubosAtaque=0,
            )
        # TODO: linkar cidades vizinhas a partir de configuração real

    def _init_decks(self) -> None:
        # baralho de infecção
        self.infection_deck = [Infeccao(c) for c in self.cities.values()]
        random.shuffle(self.infection_deck)
        # infecção inicial: 3 cartas de 3, 3 de 2, 3 de 1
        for cubes in [3, 2, 1]:
            for _ in range(3):
                if not self.infection_deck:
                    return
                card = self.infection_deck.pop(0)
                # assinatura acao((qtd, ctrl_surto))
                card.acao((cubes, self.ctrl_surto))


# ------------------------------------------------------------
# FUNÇÕES DE DESENHO
# ------------------------------------------------------------
def draw_gradient_background(screen, width: int, height: int) -> None:
    for i in range(height):
        t = i / height
        r = int(COLOR_BG_TOP[0] * (1 - t) + COLOR_BG_BOTTOM[0] * t)
        g = int(COLOR_BG_TOP[1] * (1 - t) + COLOR_BG_BOTTOM[1] * t)
        b = int(COLOR_BG_TOP[2] * (1 - t) + COLOR_BG_BOTTOM[2] * t)
        pygame.draw.line(screen, (r, g, b), (0, i), (width, i))


def draw_countries(screen, font, cities: Dict[str, Cidade]) -> None:
    for name, city in cities.items():
        x, y = CITY_COORDS.get(name, (0, 0))
        level = (
            city.get_cubosAtaque()
            if hasattr(city, "get_cubosAtaque")
            else getattr(city, "cubos", 0)
        )
        if level == 0:
            color = (0, 255, 0)
        elif level <= 2:
            color = (255, 255, 0)
        elif level == 3:
            color = (255, 165, 0)
        else:
            color = (200, 0, 0)
        pygame.draw.circle(screen, color, (x, y), 10)
        label = font.render(name, True, BLACK)
        screen.blit(label, (x - label.get_width() // 2, y + 15))


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Firewall Game")
    clock = pygame.time.Clock()

    # fontes
    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)

    # botões do menu
    menu_buttons = ["Iniciar Jogo", "Sair"]
    btn_w, btn_h, spacing = 300, 60, 20
    total_h = len(menu_buttons) * btn_h + (len(menu_buttons) - 1) * spacing
    start_y = (HEIGHT - total_h) // 2
    menu_rects = [
        (
            pygame.Rect(
                (WIDTH - btn_w) // 2, start_y + i * (btn_h + spacing), btn_w, btn_h
            ),
            text,
        )
        for i, text in enumerate(menu_buttons)
    ]

    # botões de seleção de player count (2-4)
    counts = ["2 Jogadores", "3 Jogadores", "4 Jogadores"]
    total_h2 = len(counts) * btn_h + (len(counts) - 1) * spacing
    start_y2 = (HEIGHT - total_h2) // 2
    count_rects = [
        (
            pygame.Rect(
                (WIDTH - btn_w) // 2, start_y2 + i * (btn_h + spacing), btn_w, btn_h
            ),
            cnt,
        )
        for i, cnt in enumerate(counts)
    ]

    # perfis disponíveis
    profiles = ["Analista", "Especialista", "Hacker Ético"]
    total_h3 = len(profiles) * btn_h + (len(profiles) - 1) * spacing
    start_y3 = (HEIGHT - total_h3) // 2
    profile_rects = [
        (
            pygame.Rect(
                (WIDTH - btn_w) // 2, start_y3 + i * (btn_h + spacing), btn_w, btn_h
            ),
            p,
        )
        for i, p in enumerate(profiles)
    ]

    state = MENU
    controller = None
    player_count = 0
    selected_profiles: List[str] = []
    current_player = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if state == MENU:
                    for rect, text in menu_rects:
                        if rect.collidepoint(mx, my):
                            if text == "Iniciar Jogo":
                                state = SELECT_COUNT
                            elif text == "Sair":
                                pygame.quit()
                                sys.exit()
                elif state == SELECT_COUNT:
                    for rect, cnt in count_rects:
                        if rect.collidepoint(mx, my):
                            player_count = int(cnt.split()[0])
                            state = SELECT_PROFILE
                elif state == SELECT_PROFILE:
                    for rect, p in profile_rects:
                        if rect.collidepoint(mx, my):
                            selected_profiles.append(p)
                            if current_player < player_count:
                                current_player += 1
                            else:
                                controller = GameController(player_count)
                                state = PLAYING
                            break
        # desenho
        screen.fill(BLACK)
        mx, my = pygame.mouse.get_pos()
        if state == MENU:
            draw_gradient_background(screen, WIDTH, HEIGHT)
            title = title_font.render("FIREWALL GAME", True, WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 6)))
            for rect, text in menu_rects:
                hover = rect.collidepoint(mx, my)
                color = COLOR_HIGHLIGHT if hover else COLOR_PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=12)
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=12)
                surf = font.render(text, True, WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))
        elif state == SELECT_COUNT:
            screen.fill((20, 20, 40))
            header = font.render("Selecione número de jogadores", True, WHITE)
            screen.blit(header, header.get_rect(center=(WIDTH // 2, 80)))
            for rect, cnt in count_rects:
                hover = rect.collidepoint(mx, my)
                color = COLOR_HIGHLIGHT if hover else COLOR_PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                surf = font.render(cnt, True, WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))
        elif state == SELECT_PROFILE:
            screen.fill((40, 20, 20))
            header = font.render(
                f"Jogador {current_player}, escolha seu perfil", True, WHITE
            )
            screen.blit(header, header.get_rect(center=(WIDTH // 2, 80)))
            for rect, p in profile_rects:
                hover = rect.collidepoint(mx, my)
                color = COLOR_HIGHLIGHT if hover else COLOR_PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                surf = font.render(p, True, WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))
        elif state == PLAYING and controller:
            draw_gradient_background(screen, WIDTH, HEIGHT)
            draw_countries(screen, small_font, controller.cities)
            info = small_font.render(
                f'Jogadores: {player_count} | Perfil(s): {", ".join(selected_profiles)}',
                True,
                WHITE,
            )
            screen.blit(info, (20, 20))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
