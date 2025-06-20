import pygame
import sys
import random
from typing import Dict, Tuple, List

from domain.enums.tipoAtaque import TipoAtaque
from domain.enums.cor import Cor
from domain.entities.cidade import Cidade
from domain.entities.controladorEpidemia import ControladorEpidemia
from domain.entities.controladorSurto import ControladorSurto
from domain.entities.infeccao import Infeccao


# ------------------------------------------------------------
# CONSTANTES
# ------------------------------------------------------------
class GameState:
    MENU = "menu"
    SELECT_COUNT = "select_count"
    SELECT_PROFILE = "select_profile"
    PLAYING = "playing"


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BG_TOP = (30, 0, 60)
    BG_BOTTOM = (90, 0, 150)
    PRIMARY = (128, 0, 255)
    HIGHLIGHT = (255, 0, 255)


CITY_DATA: Dict[str, Tuple[int, int, Cor]] = {
    "São Paulo": (220, 400, Cor.AMARELO),
    "Bogotá": (90, 350, Cor.AMARELO),
    "Lima": (240, 560, Cor.AMARELO),
    "Buenos Aires": (100, 520, Cor.AMARELO),
    "Santiago": (100, 200, Cor.AMARELO),
    "Nova York": (200, 120, Cor.AZUL),
    "Toronto": (130, 90, Cor.AZUL),
    "Washington": (210, 180, Cor.AZUL),
    "Chicago": (150, 210, Cor.AZUL),
    "Atlanta": (180, 250, Cor.AZUL),
    "Londres": (520, 80, Cor.VERMELHO),
    "Paris": (580, 100, Cor.VERMELHO),
    "Madri": (560, 160, Cor.VERMELHO),
    "Berlim": (630, 90, Cor.VERMELHO),
    "Roma": (600, 170, Cor.VERMELHO),
    "Cairo": (480, 300, Cor.PRETO),
    "Istambul": (540, 340, Cor.PRETO),
    "Moscou": (600, 270, Cor.PRETO),
    "Bagdá": (530, 400, Cor.PRETO),
    "Teerã": (600, 430, Cor.PRETO),
}


# ------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------
class Jogador:
    def __init__(self, nome: str, perfil: str, cidade: Cidade):
        self.nome = nome
        self.perfil = perfil
        self.cidade_atual = cidade
        self.acoes_restantes = 4

    def mover_para(self, nova_cidade: Cidade):
        if self.acoes_restantes > 0:
            self.cidade_atual = nova_cidade
            self.acoes_restantes -= 1


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
        for name, (_, _, cor) in CITY_DATA.items():
            self.cities[name] = Cidade(
                nome=name,
                pais="Desconhecido",
                tipoAtaque=TipoAtaque.PHISHING,
                cidadesVizinhas=[],
                cubosAtaque=0,
                cor=cor,
            )

    def _init_decks(self) -> None:
        self.infection_deck = [Infeccao(c) for c in self.cities.values()]
        random.shuffle(self.infection_deck)
        for cubes in [3, 2, 1]:
            for _ in range(3):
                if not self.infection_deck:
                    return
                card = self.infection_deck.pop(0)
                card.acao((cubes, self.ctrl_surto))


# ------------------------------------------------------------
# FUNÇÕES DE DESENHO
# ------------------------------------------------------------
def draw_gradient_background(screen, width: int, height: int) -> None:
    for i in range(height):
        t = i / height
        r = int(Colors.BG_TOP[0] * (1 - t) + Colors.BG_BOTTOM[0] * t)
        g = int(Colors.BG_TOP[1] * (1 - t) + Colors.BG_BOTTOM[1] * t)
        b = int(Colors.BG_TOP[2] * (1 - t) + Colors.BG_BOTTOM[2] * t)
        pygame.draw.line(screen, (r, g, b), (0, i), (width, i))


def draw_countries(screen, font, cities: Dict[str, Cidade]) -> None:
    grouped_by_color: Dict[Cor, List[Tuple[int, int]]] = {}
    for name, city in cities.items():
        x, y = CITY_DATA.get(name, (0, 0, Cor.AMARELO))[:2]
        grouped_by_color.setdefault(city.get_cor(), []).append((x, y))
        try:
            color_rgb = pygame.Color(city.get_cor().value)
        except (ValueError, pygame.error):
            color_rgb = pygame.Color("#888888")
        pygame.draw.circle(screen, color_rgb, (x, y), 10)
        label = font.render(name, True, Colors.BLACK)
        screen.blit(label, (x - label.get_width() // 2, y + 15))

    for cor, pontos in grouped_by_color.items():
        try:
            color_rgb = pygame.Color(cor.value)
        except (ValueError, pygame.error):
            color_rgb = pygame.Color("#888888")
        for i in range(len(pontos)):
            for j in range(i + 1, len(pontos)):
                pygame.draw.line(screen, color_rgb, pontos[i], pontos[j], 2)


# ------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------------------------------------
def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Firewall Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)

    def create_rects(items: List[str], btn_w=300, btn_h=60, spacing=20):
        total_h = len(items) * btn_h + (len(items) - 1) * spacing
        start_y = (HEIGHT - total_h) // 2
        return [
            (
                pygame.Rect(
                    (WIDTH - btn_w) // 2, start_y + i * (btn_h + spacing), btn_w, btn_h
                ),
                item,
            )
            for i, item in enumerate(items)
        ]

    menu_rects = create_rects(["Iniciar Jogo", "Sair"])
    count_rects = create_rects(["2 Jogadores", "3 Jogadores", "4 Jogadores"])
    profile_rects = create_rects(["Analista", "Especialista", "Hacker Ético"])

    state = GameState.MENU
    controller = None
    player_count = 0
    selected_profiles: List[str] = []
    current_player = 1
    jogadores: List[Jogador] = []
    jogador_atual_idx = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if state == GameState.MENU:
                    for rect, text in menu_rects:
                        if rect.collidepoint(mx, my):
                            if text == "Iniciar Jogo":
                                state = GameState.SELECT_COUNT
                            elif text == "Sair":
                                pygame.quit()
                                sys.exit()

                elif state == GameState.SELECT_COUNT:
                    for rect, cnt in count_rects:
                        if rect.collidepoint(mx, my):
                            player_count = int(cnt.split()[0])
                            state = GameState.SELECT_PROFILE

                elif state == GameState.SELECT_PROFILE:
                    for rect, p in profile_rects:
                        if rect.collidepoint(mx, my):
                            selected_profiles.append(p)
                            if current_player < player_count:
                                current_player += 1
                            else:
                                controller = GameController(player_count)
                                jogadores = []
                                for i in range(player_count):
                                    jogador = Jogador(
                                        f"Jogador {i+1}",
                                        selected_profiles[i],
                                        controller.cities["São Paulo"],
                                    )
                                    jogadores.append(jogador)
                                jogador_atual_idx = 0
                                state = GameState.PLAYING
                            break

                elif state == GameState.PLAYING:
                    jogador_atual = jogadores[jogador_atual_idx]
                    for nome, (x, y, _) in CITY_DATA.items():
                        cidade = controller.cities[nome]
                        if (mx - x) ** 2 + (my - y) ** 2 <= 10**2:
                            jogador_atual.mover_para(cidade)
                            break

                    if jogador_atual.acoes_restantes == 0:
                        jogador_atual_idx = (jogador_atual_idx + 1) % player_count
                        jogadores[jogador_atual_idx].acoes_restantes = 4

        screen.fill(Colors.BLACK)
        mx, my = pygame.mouse.get_pos()

        if state == GameState.MENU:
            draw_gradient_background(screen, WIDTH, HEIGHT)
            title = title_font.render("FIREWALL GAME", True, Colors.WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 6)))
            for rect, text in menu_rects:
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=12)
                pygame.draw.rect(screen, Colors.WHITE, rect, 3, border_radius=12)
                surf = font.render(text, True, Colors.WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))

        elif state == GameState.SELECT_COUNT:
            screen.fill((20, 20, 40))
            header = font.render("Selecione número de jogadores", True, Colors.WHITE)
            screen.blit(header, header.get_rect(center=(WIDTH // 2, 80)))
            for rect, cnt in count_rects:
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                surf = font.render(cnt, True, Colors.WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))

        elif state == GameState.SELECT_PROFILE:
            screen.fill((40, 20, 20))
            header = font.render(
                f"Jogador {current_player}, escolha seu perfil", True, Colors.WHITE
            )
            screen.blit(header, header.get_rect(center=(WIDTH // 2, 80)))
            for rect, p in profile_rects:
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                surf = font.render(p, True, Colors.WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))

        elif state == GameState.PLAYING and controller:
            draw_gradient_background(screen, WIDTH, HEIGHT)
            draw_countries(screen, small_font, controller.cities)
            perfil_str = ", ".join(selected_profiles)
            screen.blit(
                small_font.render(
                    f"Jogadores: {player_count} | Perfil(s): {perfil_str}",
                    True,
                    Colors.WHITE,
                ),
                (20, 20),
            )

            # Mostrar jogadores no mapa
            for j, jogador in enumerate(jogadores):
                x, y = CITY_DATA[jogador.cidade_atual.get_nome()][:2]
                cor_jogador = [
                    (255, 255, 0),
                    (0, 255, 0),
                    (0, 255, 255),
                    (255, 128, 0),
                ][j]
                pygame.draw.circle(screen, cor_jogador, (x, y), 6)
                label = small_font.render(f"P{j+1}", True, Colors.BLACK)
                screen.blit(label, (x - 10, y - 25))

            jogador_atual = jogadores[jogador_atual_idx]
            info_turno = small_font.render(
                f"Vez de {jogador_atual.nome} \
                | Ações restantes: {jogador_atual.acoes_restantes}",
                True,
                Colors.WHITE,
            )
            screen.blit(info_turno, (20, 50))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
#teste