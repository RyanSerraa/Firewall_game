import pygame
import sys
import random
from typing import Dict, Tuple, List, Any, Optional
from abc import ABC, abstractmethod

from domain.enums.tipoAtaque import TipoAtaque
from domain.enums.cor import Cor
from domain.entities.cidade import Cidade
from domain.entities.controladorEpidemia import ControladorEpidemia
from domain.entities.controladorSurto import ControladorSurto
from domain.entities.carta import Carta
from domain.entities.infeccao import Infeccao
from domain.entities.personagem import Personagem

# ------------------------------------------------------------
# CONSTANTES E CLASSES AUXILIARES
# ------------------------------------------------------------
class GameState:
    MENU = "menu"
    SELECT_COUNT = "select_count"
    SELECT_DIFFICULTY = "select_difficulty"
    SELECT_PROFILE = "select_profile"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    SHARING_KNOWLEDGE = "sharing_knowledge"
    DISCOVERING_COUNTERMEASURE = "discovering_countermeasure"

class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BG_TOP = (30, 0, 60)
    BG_BOTTOM = (90, 0, 150)
    PRIMARY = (128, 0, 255)
    HIGHLIGHT = (255, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)

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

# Conexões entre cidades (simplificado)
CITY_CONNECTIONS = {
    "São Paulo": ["Bogotá", "Buenos Aires"],
    "Bogotá": ["São Paulo", "Lima"],
    "Lima": ["Bogotá", "Santiago"],
    "Buenos Aires": ["São Paulo", "Santiago"],
    "Santiago": ["Lima", "Buenos Aires"],
    "Nova York": ["Toronto", "Washington", "Londres"],
    "Toronto": ["Nova York", "Chicago"],
    "Washington": ["Nova York", "Atlanta"],
    "Chicago": ["Toronto", "Atlanta"],
    "Atlanta": ["Washington", "Chicago"],
    "Londres": ["Nova York", "Paris", "Madri"],
    "Paris": ["Londres", "Madri", "Berlim"],
    "Madri": ["Londres", "Paris", "São Paulo"],
    "Berlim": ["Paris", "Roma", "Moscou"],
    "Roma": ["Berlim", "Istambul"],
    "Cairo": ["Istambul", "Bagdá"],
    "Istambul": ["Roma", "Cairo", "Bagdá", "Moscou"],
    "Moscou": ["Berlim", "Istambul", "Teerã"],
    "Bagdá": ["Istambul", "Cairo", "Teerã"],
    "Teerã": ["Moscou", "Bagdá"],
}

# Implementação concreta das cartas
class CartaCidade(Carta):
    def __init__(self, cidade: Cidade):
        super().__init__(cidade.get_nome())
        self.cidade = cidade
    
    def acao(self, parametro: Any) -> None:
        pass

class CartaEpidemia(Carta):
    def acao(self, parametro: Any) -> None:
        # Implementar ação da epidemia
        pass

# ------------------------------------------------------------
# CLASSES PRINCIPAIS
# ------------------------------------------------------------
class Jogador:
    def __init__(self, nome: str, perfil: str, cidade: Cidade):
        self.nome = nome
        self.perfil = perfil
        self.cidade_atual = cidade
        self.cartas: List[Carta] = []
        self.acoes_restantes = 4
        self.poderes_especiais = {
            "Analista": self.contramedida_rapida,
            "Especialista": self.tratar_eficiente,
            "Hacker Ético": self.compartilhar_flexivel,
            "Engenheiro": self.construir_sem_carta
        }
    
    def mover_para(self, nova_cidade: Cidade) -> bool:
        if self.acoes_restantes > 0:
            if nova_cidade in self.cidade_atual.get_cidadesVizinhas():
                self.cidade_atual = nova_cidade
                self.acoes_restantes -= 1
                return True
        return False
    
    def voo_direto(self, cidade_destino: Cidade, carta: CartaCidade) -> bool:
        if self.acoes_restantes > 0 and carta in self.cartas:
            self.cidade_atual = cidade_destino
            self.cartas.remove(carta)
            self.acoes_restantes -= 1
            return True
        return False
    
    def voo_fretado(self, cidade_destino: Cidade, carta: CartaCidade) -> bool:
        if (self.acoes_restantes > 0 and carta in self.cartas and 
            carta.cidade == self.cidade_atual):
            self.cidade_atual = cidade_destino
            self.cartas.remove(carta)
            self.acoes_restantes -= 1
            return True
        return False
    
    def fronte_aerea(self, cidade_destino: Cidade) -> bool:
        if (self.acoes_restantes > 0 and 
            self.cidade_atual.nome in ControladorJogo.centros_pesquisa and 
            cidade_destino.nome in ControladorJogo.centros_pesquisa):
            self.cidade_atual = cidade_destino
            self.acoes_restantes -= 1
            return True
        return False
    
    def tratar_ataque(self, controlador) -> bool:
        if self.acoes_restantes > 0:
            cidade = self.cidade_atual
            if cidade.get_cubosAtaque() > 0:
                if self.perfil == "Especialista":
                    cidade.set_cubosAtaque(-cidade.get_cubosAtaque())
                else:
                    cidade.set_cubosAtaque(-1)
                self.acoes_restantes -= 1
                return True
        return False
    
    def construir_centro(self, controlador) -> bool:
        if self.acoes_restantes > 0:
            cidade = self.cidade_atual
            # Verificar se o jogador tem a carta da cidade ou é engenheiro
            tem_carta = any(isinstance(c, CartaCidade) and c.cidade == cidade for c in self.cartas)
            
            if self.perfil == "Engenheiro" or tem_carta:
                if cidade.__nome not in controlador.centros_pesquisa:
                    controlador.centros_pesquisa.append(cidade.nome)
                
                # Remover a carta se não for engenheiro
                if self.perfil != "Engenheiro":
                    for carta in self.cartas:
                        if isinstance(carta, CartaCidade) and carta.cidade == cidade:
                            self.cartas.remove(carta)
                            break
                
                self.acoes_restantes -= 1
                return True
        return False
    
    def compartilhar_conhecimento(self, outro_jogador: 'Jogador', carta: Carta) -> bool:
        if (self.acoes_restantes > 0 and 
            self.cidade_atual == outro_jogador.cidade_atual and 
            carta in self.cartas):
            self.cartas.remove(carta)
            outro_jogador.cartas.append(carta)
            self.acoes_restantes -= 1
            return True
        return False
    
    def descobrir_contramedida(self, tipo_ataque: TipoAtaque, controlador) -> bool:
        if self.acoes_restantes > 0 and self.cidade_atual.nome in controlador.centros_pesquisa:
            cartas_necessarias = 5
            if self.perfil == "Analista":
                cartas_necessarias = 3
            
            cartas_ataque = [c for c in self.cartas 
                             if isinstance(c, CartaCidade) and 
                             c.cidade.get_tipoAtaque() == tipo_ataque]
            
            if len(cartas_ataque) >= cartas_necessarias:
                # Remover cartas usadas
                for _ in range(cartas_necessarias):
                    carta = cartas_ataque.pop()
                    self.cartas.remove(carta)
                    controlador.baralho_jogador.append(carta)  # Adicionar ao descarte
                
                controlador.contramedidas[tipo_ataque] = True
                self.acoes_restantes -= 1
                return True
        return False
    
    # Poderes especiais
    def contramedida_rapida(self, tipo_ataque: TipoAtaque, controlador) -> bool:
        return self.descobrir_contramedida(tipo_ataque, controlador)
    
    def tratar_eficiente(self, controlador) -> bool:
        return self.tratar_ataque(controlador)
    
    def compartilhar_flexivel(self, outro_jogador: 'Jogador', carta: Carta) -> bool:
        return self.compartilhar_conhecimento(outro_jogador, carta)
    
    def construir_sem_carta(self, controlador) -> bool:
        return self.construir_centro(controlador)

class ControladorJogo:
    def __init__(self, dificuldade: str, player_count: int) -> None:
        self.dificuldade = dificuldade
        self.player_count = player_count
        self.ctrl_epidemia = ControladorEpidemia()
        self.ctrl_surto = ControladorSurto()
        self.cities: Dict[str, Cidade] = {}
        self.jogadores: List[Jogador] = []
        self.baralho_jogador: List[Carta] = []
        self.descarte_jogador: List[Carta] = []
        self.baralho_infeccao: List[Carta] = []
        self.descarte_infeccao: List[Carta] = []
        self.centros_pesquisa = ["São Paulo"]
        self.contramedidas = {tipo: False for tipo in TipoAtaque}
        self.surtos = 0
        self.velocidade_infeccao = 2
        self._init_cidades()
        self._init_baralhos()
        self.infecao_inicial()
    
    def _init_cidades(self) -> None:
        # Criar cidades
        for name, (_, _, cor) in CITY_DATA.items():
            self.cities[name] = Cidade(
                nome=name,
                pais="Desconhecido",
                tipoAtaque=random.choice(list(TipoAtaque)),
                cidadesVizinhas=[],
                cubosAtaque=0,
                cor=cor,
            )
        
        # Configurar conexões
        for cidade_nome, vizinhas in CITY_CONNECTIONS.items():
            cidade = self.cities[cidade_nome]
            cidade.set_cidadesVizinhas([self.cities[v] for v in vizinhas])
    
    def _init_baralhos(self) -> None:
        # Baralho de infecção
        for cidade in self.cities.values():
            self.baralho_infeccao.append(Infeccao(cidade))
        random.shuffle(self.baralho_infeccao)
        
        # Baralho do jogador (cartas de cidade)
        for cidade in self.cities.values():
            self.baralho_jogador.append(CartaCidade(cidade))
        
        # Adicionar cartas de epidemia baseado na dificuldade
        num_epidemias = {"fácil": 4, "médio": 5, "difícil": 6}[self.dificuldade]
        for _ in range(num_epidemias):
            self.baralho_jogador.append(CartaEpidemia("Epidemia"))
        
        # Dividir e embaralhar com epidemias
        partes = []
        tamanho_parte = len(self.baralho_jogador) // num_epidemias
        for i in range(num_epidemias):
            parte = self.baralho_jogador[i*tamanho_parte:(i+1)*tamanho_parte]
            parte.append(CartaEpidemia("Epidemia"))
            random.shuffle(parte)
            partes.append(parte)
        
        self.baralho_jogador = []
        for parte in partes:
            self.baralho_jogador.extend(parte)
        
        # Distribuir cartas iniciais para jogadores
        cartas_por_jogador = {2: 4, 3: 3, 4: 2}[self.player_count]
        for jogador in self.jogadores:
            for _ in range(cartas_por_jogador):
                if self.baralho_jogador:
                    carta = self.baralho_jogador.pop(0)
                    jogador.cartas.append(carta)
    
    def infecao_inicial(self) -> None:
        # Fase de infecção inicial: 3 cartas com 3 cubos, 3 com 2, 3 com 1
        for quantidade in [3, 2, 1]:
            for _ in range(3):
                if self.baralho_infeccao:
                    carta = self.baralho_infeccao.pop(0)
                    cidade = carta.get_cidade()
                    cidade.set_cubosAtaque(quantidade)
                    self.descarte_infeccao.append(carta)
    
    def comprar_cartas_infeccao(self) -> None:
        for _ in range(self.velocidade_infeccao):
            if self.baralho_infeccao:
                carta = self.baralho_infeccao.pop(0)
                cidade = carta.get_cidade()
                cidade.set_cubosAtaque(1)
                
                # Verificar surto
                if cidade.get_cubosAtaque() > 3:
                    self.surtos += 1
                    cidade.set_cubosAtaque(3 - cidade.get_cubosAtaque())  # Reset para 3
                    
                    # Propagação para cidades vizinhas
                    for vizinha in cidade.get_cidadesVizinhas():
                        vizinha.set_cubosAtaque(1)
                        if vizinha.get_cubosAtaque() > 3:
                            self.surtos += 1
                            vizinha.set_cubosAtaque(3 - vizinha.get_cubosAtaque())
                
                self.descarte_infeccao.append(carta)
    
    def verificar_derrota(self) -> bool:
        # Verificar surtos
        if self.surtos >= 8:
            return True
        
        # Verificar falta de cubos (simplificado)
        for cidade in self.cities.values():
            if cidade.get_cubosAtaque() > 3:
                return True
        
        # Verificar baralho do jogador
        if not self.baralho_jogador:
            return True
        
        return False
    
    def verificar_vitoria(self) -> bool:
        return all(self.contramedidas.values())
    
    def proximo_turno(self) -> None:
        # Resetar ações dos jogadores
        for jogador in self.jogadores:
            jogador.acoes_restantes = 4
        
        # Comprar cartas de infecção
        self.comprar_cartas_infeccao()
        
        # Verificar condições de fim de jogo
        if self.verificar_derrota():
            return "derrota"
        if self.verificar_vitoria():
            return "vitoria"
        return "continua"

# ------------------------------------------------------------
# FUNÇÕES DE DESENHO E INTERFACE
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

def create_rects(items: List[str], width: int, height: int, btn_w=300, btn_h=60, spacing=20):
    total_h = len(items) * btn_h + (len(items) - 1) * spacing
    start_y = (height - total_h) // 2
    return [
        (
            pygame.Rect(
                (width - btn_w) // 2, start_y + i * (btn_h + spacing), btn_w, btn_h
            ),
            item,
        )
        for i, item in enumerate(items)
    ]

def draw_text_centered(screen, text: str, font, y_offset=0, color=Colors.WHITE):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(text_surf, text_rect)

def draw_button(screen, rect, text, font, hover=False):
    color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, Colors.WHITE, rect, 2, border_radius=8)
    text_surf = font.render(text, True, Colors.WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect

# ------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------------------------------------
def main():
    pygame.init()
    WIDTH, HEIGHT = 1024, 768  # Tamanho aumentado para 1024x768
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Firewall Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)
    info_font = pygame.font.Font(None, 28)
    card_font = pygame.font.Font(None, 24)

    # Criar os retângulos passando WIDTH e HEIGHT
    menu_rects = create_rects(["Iniciar Jogo", "Sair"], WIDTH, HEIGHT)
    count_rects = create_rects(["2 Jogadores", "3 Jogadores", "4 Jogadores"], WIDTH, HEIGHT)
    difficulty_rects = create_rects(["Fácil", "Médio", "Difícil"], WIDTH, HEIGHT)
    profile_rects = create_rects(["Analista", "Especialista", "Hacker Ético", "Engenheiro"], WIDTH, HEIGHT)
    game_over_rects = create_rects(["Voltar ao Menu"], WIDTH, HEIGHT)

    # Estados e variáveis do jogo
    state = GameState.MENU
    controller: Optional[ControladorJogo] = None
    player_count = 0
    selected_difficulty = ""
    selected_profiles: List[str] = []
    current_player = 1
    jogadores: List[Jogador] = []
    jogador_atual_idx = 0
    game_result = ""
    sharing_knowledge = False
    discovering_countermeasure = False
    selected_card = None
    selected_player = None
    selected_attack = None

    while True:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                            state = GameState.SELECT_DIFFICULTY

                elif state == GameState.SELECT_DIFFICULTY:
                    for rect, diff in difficulty_rects:
                        if rect.collidepoint(mx, my):
                            selected_difficulty = diff.lower()
                            state = GameState.SELECT_PROFILE

                elif state == GameState.SELECT_PROFILE:
                    for rect, p in profile_rects:
                        if rect.collidepoint(mx, my):
                            selected_profiles.append(p)
                            if current_player < player_count:
                                current_player += 1
                            else:
                                # Criar controlador do jogo
                                controller = ControladorJogo(selected_difficulty, player_count)
                                
                                # Criar jogadores
                                for i in range(player_count):
                                    jogador = Jogador(
                                        f"Jogador {i+1}",
                                        selected_profiles[i],
                                        controller.cities["São Paulo"]
                                    )
                                    jogadores.append(jogador)
                                    controller.jogadores.append(jogador)
                                
                                # Distribuir cartas iniciais
                                controller._init_baralhos()
                                jogador_atual_idx = 0
                                state = GameState.PLAYING
                            break

                elif state == GameState.PLAYING and controller:
                    jogador_atual = jogadores[jogador_atual_idx]
                    
                    # Movimento entre cidades
                    for nome, (x, y, _) in CITY_DATA.items():
                        cidade = controller.cities[nome]
                        if (mx - x) ** 2 + (my - y) ** 2 <= 10**2:
                            if jogador_atual.mover_para(cidade):
                                pass  # Movimento realizado
                            break
                    
                    # Botões de ação
                    action_buttons = [
                        pygame.Rect(20, HEIGHT-150, 180, 40),  # Tratar ataque
                        pygame.Rect(220, HEIGHT-150, 230, 40),  # Construir centro
                        pygame.Rect(470, HEIGHT-150, 230, 40),  # Compartilhar
                        pygame.Rect(720, HEIGHT-150, 250, 40),  # Descobrir contramedida
                        pygame.Rect(350, HEIGHT-100, 100, 40),  # Finalizar turno
                    ]
                    
                    for i, rect in enumerate(action_buttons):
                        if rect.collidepoint(mx, my):
                            if i == 0:  # Tratar ataque
                                if jogador_atual.tratar_ataque(controller):
                                    # Atualizar display
                                    pass
                            elif i == 1:  # Construir centro
                                if jogador_atual.construir_centro(controller):
                                    # Atualizar display
                                    pass
                            elif i == 2:  # Compartilhar conhecimento
                                sharing_knowledge = True
                                state = GameState.SHARING_KNOWLEDGE
                            elif i == 3:  # Descobrir contramedida
                                discovering_countermeasure = True
                                state = GameState.DISCOVERING_COUNTERMEASURE
                            elif i == 4:  # Finalizar turno
                                jogador_atual.acoes_restantes = 0
                    
                    # Final de turno
                    if jogador_atual.acoes_restantes == 0:
                        jogador_atual_idx = (jogador_atual_idx + 1) % player_count
                        jogadores[jogador_atual_idx].acoes_restantes = 4
                        
                        # Se todos os jogadores terminaram, próximo turno
                        if jogador_atual_idx == 0:
                            result = controller.proximo_turno()
                            if result == "derrota":
                                state = GameState.GAME_OVER
                                game_result = "DERROTA - Muitos surtos ocorreram!"
                            elif result == "vitoria":
                                state = GameState.VICTORY
                                game_result = "VITÓRIA! Todas as contramedidas foram descobertas!"
                
                elif state == GameState.SHARING_KNOWLEDGE:
                    # Seleção de carta para compartilhar
                    card_buttons = []
                    for i, carta in enumerate(jogador_atual.cartas):
                        rect = pygame.Rect(50 + i*150, HEIGHT-200, 140, 30)
                        if rect.collidepoint(mx, my):
                            selected_card = carta
                    
                    # Seleção de jogador para compartilhar
                    player_buttons = []
                    for i, jogador in enumerate(jogadores):
                        if jogador != jogador_atual:
                            rect = pygame.Rect(50 + i*150, HEIGHT-150, 140, 30)
                            if rect.collidepoint(mx, my):
                                selected_player = jogador
                    
                    # Botão de confirmação
                    confirm_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT-100, 150, 40)
                    if confirm_rect.collidepoint(mx, my):
                        if selected_card and selected_player:
                            if jogador_atual.compartilhar_conhecimento(selected_player, selected_card):
                                sharing_knowledge = False
                                state = GameState.PLAYING
                                selected_card = None
                                selected_player = None
                
                elif state == GameState.DISCOVERING_COUNTERMEASURE:
                    # Seleção de tipo de ataque
                    attack_buttons = []
                    for i, ataque in enumerate(TipoAtaque):
                        rect = pygame.Rect(50 + i*150, HEIGHT-200, 140, 30)
                        if rect.collidepoint(mx, my):
                            selected_attack = ataque
                    
                    # Botão de confirmação
                    confirm_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT-100, 150, 40)
                    if confirm_rect.collidepoint(mx, my):
                        if selected_attack:
                            if jogador_atual.descobrir_contramedida(selected_attack, controller):
                                discovering_countermeasure = False
                                state = GameState.PLAYING
                                selected_attack = None

                elif state in [GameState.GAME_OVER, GameState.VICTORY]:
                    for rect, text in game_over_rects:
                        if rect.collidepoint(mx, my):
                            state = GameState.MENU
                            # Resetar variáveis do jogo
                            controller = None
                            player_count = 0
                            selected_difficulty = ""
                            selected_profiles = []
                            current_player = 1
                            jogadores = []
                            jogador_atual_idx = 0
                            game_result = ""
                            sharing_knowledge = False
                            discovering_countermeasure = False

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

        elif state == GameState.SELECT_DIFFICULTY:
            screen.fill((20, 40, 20))
            header = font.render("Selecione a dificuldade", True, Colors.WHITE)
            screen.blit(header, header.get_rect(center=(WIDTH // 2, 80)))
            for rect, diff in difficulty_rects:
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                surf = font.render(diff, True, Colors.WHITE)
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
            
            # Mostrar jogadores no mapa
            for j, jogador in enumerate(jogadores):
                x, y = CITY_DATA[jogador.cidade_atual.get_nome()][:2]
                cor_jogador = [
                    Colors.YELLOW,
                    Colors.GREEN,
                    Colors.CYAN,
                    Colors.ORANGE
                ][j]
                pygame.draw.circle(screen, cor_jogador, (x, y), 8)
                label = small_font.render(f"P{j+1}", True, Colors.BLACK)
                screen.blit(label, (x - 10, y - 25))
            
            # Mostrar cubos de ataque nas cidades
            for nome, (x, y, _) in CITY_DATA.items():
                cidade = controller.cities[nome]
                cubos = cidade.get_cubosAtaque()
                if cubos > 0:
                    cor_ataque = {
                        TipoAtaque.RANSOMWARE: Colors.RED,
                        TipoAtaque.PHISHING: Colors.BLUE,
                        TipoAtaque.DDOS: Colors.YELLOW,
                        TipoAtaque.SPYWARE: Colors.PURPLE
                    }.get(cidade.get_tipoAtaque(), Colors.WHITE)
                    
                    # Desenhar cubos de ataque
                    for i in range(cubos):
                        pos_x = x + i * 10 - (cubos-1)*5
                        pygame.draw.rect(screen, cor_ataque, (pos_x-5, y-25, 8, 8))
            
            # Informações do jogador atual
            jogador_atual = jogadores[jogador_atual_idx]
            info_turno = font.render(
                f"Vez de {jogador_atual.nome} ({jogador_atual.perfil}) | Ações: {jogador_atual.acoes_restantes}", 
                True, Colors.WHITE
            )
            screen.blit(info_turno, (20, 20))
            
            # Mostrar contadores
            surtos_text = info_font.render(f"Surtos: {controller.surtos}/7", True, Colors.WHITE)
            infeccao_text = info_font.render(f"Velocidade Infecção: {controller.velocidade_infeccao}", True, Colors.WHITE)
            screen.blit(surtos_text, (WIDTH - 200, 20))
            screen.blit(infeccao_text, (WIDTH - 200, 50))
            
            # Mostrar contramedidas
            cm_y = 80
            for ataque, descoberta in controller.contramedidas.items():
                status = "✓" if descoberta else "✗"
                cor = Colors.GREEN if descoberta else Colors.RED
                cm_text = info_font.render(f"{ataque.name}: {status}", True, cor)
                screen.blit(cm_text, (WIDTH - 200, cm_y))
                cm_y += 30
            
            # Mostrar centros de pesquisa
            centros_text = info_font.render("Centros de Pesquisa:", True, Colors.WHITE)
            screen.blit(centros_text, (20, HEIGHT - 180))
            centros_list = ", ".join(controller.centros_pesquisa)
            centros_valor = info_font.render(centros_list, True, Colors.WHITE)
            screen.blit(centros_valor, (20, HEIGHT - 150))
            
            # Botões de ação
            action_labels = [
                "Tratar Ataque (1)",
                "Construir Centro (1)",
                "Compartilhar Conhecimento (1)",
                "Descobrir Contramedida (1)",
                "Finalizar Turno"
            ]
            action_buttons = [
                pygame.Rect(20, HEIGHT-150, 180, 40),
                pygame.Rect(220, HEIGHT-150, 230, 40),
                pygame.Rect(470, HEIGHT-150, 230, 40),
                pygame.Rect(720, HEIGHT-150, 250, 40),
                pygame.Rect(350, HEIGHT-100, 100, 40),
            ]
            
            for i, rect in enumerate(action_buttons):
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                pygame.draw.rect(screen, Colors.WHITE, rect, 2, border_radius=8)
                label = small_font.render(action_labels[i], True, Colors.WHITE)
                screen.blit(label, (rect.x + 10, rect.y + 10))
            
            # Mostrar cartas do jogador
            cartas_text = info_font.render("Suas Cartas:", True, Colors.WHITE)
            screen.blit(cartas_text, (20, 60))
            
            # Exibir cartas em múltiplas linhas
            cartas_list = [c.get_nome() for c in jogador_atual.cartas]
            y_pos = 90
            for i in range(0, len(cartas_list), 5):
                linha = ", ".join(cartas_list[i:i+5])
                cartas_valor = info_font.render(linha, True, Colors.WHITE)
                screen.blit(cartas_valor, (20, y_pos))
                y_pos += 30

        elif state == GameState.SHARING_KNOWLEDGE:
            screen.fill((30, 0, 60))
            title = font.render("Compartilhar Conhecimento", True, Colors.WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH//2, 50)))
            
            # Instruções
            instrucoes = info_font.render("Selecione uma carta para compartilhar e um jogador", True, Colors.WHITE)
            screen.blit(instrucoes, (WIDTH//2 - instrucoes.get_width()//2, 100))
            
            # Seleção de carta
            card_title = info_font.render("Selecione uma carta:", True, Colors.WHITE)
            screen.blit(card_title, (50, 150))
            
            card_buttons = []
            for i, carta in enumerate(jogador_atual.cartas):
                rect = pygame.Rect(50 + i*150, 200, 140, 30)
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=4)
                pygame.draw.rect(screen, Colors.WHITE, rect, 1, border_radius=4)
                card_text = card_font.render(carta.get_nome(), True, Colors.WHITE)
                screen.blit(card_text, (rect.x + 5, rect.y + 5))
                card_buttons.append(rect)
                
                if rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
                    selected_card = carta
            
            # Seleção de jogador
            player_title = info_font.render("Selecione um jogador:", True, Colors.WHITE)
            screen.blit(player_title, (50, 250))
            
            player_buttons = []
            for i, jogador in enumerate(jogadores):
                if jogador != jogador_atual:
                    rect = pygame.Rect(50 + i*150, 300, 140, 30)
                    hover = rect.collidepoint(mx, my)
                    color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                    pygame.draw.rect(screen, color, rect, border_radius=4)
                    pygame.draw.rect(screen, Colors.WHITE, rect, 1, border_radius=4)
                    player_text = card_font.render(jogador.nome, True, Colors.WHITE)
                    screen.blit(player_text, (rect.x + 5, rect.y + 5))
                    player_buttons.append(rect)
                    
                    if rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
                        selected_player = jogador
            
            # Botão de confirmação
            confirm_rect = pygame.Rect(WIDTH//2 - 75, 400, 150, 40)
            hover = confirm_rect.collidepoint(mx, my)
            color = Colors.GREEN if hover else Colors.PRIMARY
            pygame.draw.rect(screen, color, confirm_rect, border_radius=8)
            pygame.draw.rect(screen, Colors.WHITE, confirm_rect, 2, border_radius=8)
            confirm_text = font.render("Confirmar", True, Colors.WHITE)
            screen.blit(confirm_text, (confirm_rect.x + 15, confirm_rect.y + 5))
            
            # Mostrar seleções
            if selected_card:
                card_text = info_font.render(f"Carta selecionada: {selected_card.get_nome()}", True, Colors.WHITE)
                screen.blit(card_text, (WIDTH//2 - card_text.get_width()//2, 350))
            
            if selected_player:
                player_text = info_font.render(f"Jogador selecionado: {selected_player.nome}", True, Colors.WHITE)
                screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, 380))

        elif state == GameState.DISCOVERING_COUNTERMEASURE:
            screen.fill((30, 0, 60))
            title = font.render("Descobrir Contramedida", True, Colors.WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH//2, 50)))
            
            # Instruções
            instrucoes = info_font.render("Selecione um tipo de ataque para desenvolver contramedida", True, Colors.WHITE)
            screen.blit(instrucoes, (WIDTH//2 - instrucoes.get_width()//2, 100))
            
            # Seleção de ataque
            attack_buttons = []
            for i, ataque in enumerate(TipoAtaque):
                rect = pygame.Rect(50 + i*200, 200, 180, 40)
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=8)
                pygame.draw.rect(screen, Colors.WHITE, rect, 2, border_radius=8)
                attack_text = font.render(ataque.name, True, Colors.WHITE)
                screen.blit(attack_text, (rect.x + 10, rect.y + 5))
                attack_buttons.append(rect)
                
                if rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
                    selected_attack = ataque
            
            # Botão de confirmação
            confirm_rect = pygame.Rect(WIDTH//2 - 75, 300, 150, 40)
            hover = confirm_rect.collidepoint(mx, my)
            color = Colors.GREEN if hover else Colors.PRIMARY
            pygame.draw.rect(screen, color, confirm_rect, border_radius=8)
            pygame.draw.rect(screen, Colors.WHITE, confirm_rect, 2, border_radius=8)
            confirm_text = font.render("Confirmar", True, Colors.WHITE)
            screen.blit(confirm_text, (confirm_rect.x + 15, confirm_rect.y + 5))
            
            # Mostrar seleção
            if selected_attack:
                attack_text = info_font.render(f"Ataque selecionado: {selected_attack.name}", True, Colors.WHITE)
                screen.blit(attack_text, (WIDTH//2 - attack_text.get_width()//2, 250))

        elif state == GameState.GAME_OVER:
            screen.fill((40, 0, 0))
            draw_text_centered(screen, "FIM DE JOGO", title_font, -50, Colors.RED)
            draw_text_centered(screen, game_result, font, 0, Colors.WHITE)
            for rect, text in game_over_rects:
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=12)
                pygame.draw.rect(screen, Colors.WHITE, rect, 3, border_radius=12)
                surf = font.render(text, True, Colors.WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))

        elif state == GameState.VICTORY:
            screen.fill((0, 40, 0))
            draw_text_centered(screen, "VITÓRIA!", title_font, -50, Colors.GREEN)
            draw_text_centered(screen, game_result, font, 0, Colors.WHITE)
            for rect, text in game_over_rects:
                hover = rect.collidepoint(mx, my)
                color = Colors.HIGHLIGHT if hover else Colors.PRIMARY
                pygame.draw.rect(screen, color, rect, border_radius=12)
                pygame.draw.rect(screen, Colors.WHITE, rect, 3, border_radius=12)
                surf = font.render(text, True, Colors.WHITE)
                screen.blit(surf, surf.get_rect(center=rect.center))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()