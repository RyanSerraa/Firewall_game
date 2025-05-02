import pygame
import sys

# Inicialização do Pygame
def main():
    pygame.init()
    
    # Tamanho da janela
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FIREWALL - Menu Principal")

    # Paleta de cores (inspirada nos slides)
    COLOR_BG_TOP = (30, 0, 60)        # Roxo escuro
    COLOR_BG_BOTTOM = (90, 0, 150)    # Roxo mais claro
    COLOR_PRIMARY = (128, 0, 255)     # Roxo vibrante
    COLOR_ACCENT = (0, 255, 255)      # Ciano
    COLOR_HIGHLIGHT = (255, 0, 255)   # Rosa neon
    COLOR_TEXT = (255, 255, 255)      # Branco

    # Fonte
    font = pygame.font.Font(None, 48)

    # Botões do menu
    buttons = ["Iniciar Jogo", "Carregar Jogo", "Sair"]
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

    # Loop principal
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for rect, text in button_rects:
                    if rect.collidepoint(mx, my):
                        if text == "Sair":
                            running = False
                        else:
                            print(f"Botão '{text}' clicado")

        # Desenha gradiente de fundo
        for i in range(HEIGHT):
            # Interpolação linear das cores
            t = i / HEIGHT
            r = int(COLOR_BG_TOP[0] * (1 - t) + COLOR_BG_BOTTOM[0] * t)
            g = int(COLOR_BG_TOP[1] * (1 - t) + COLOR_BG_BOTTOM[1] * t)
            b = int(COLOR_BG_TOP[2] * (1 - t) + COLOR_BG_BOTTOM[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

        # Desenha botões
        mx, my = pygame.mouse.get_pos()
        for rect, text in button_rects:
            # Muda cor ao passar mouse
            if rect.collidepoint(mx, my):
                color = COLOR_HIGHLIGHT
            else:
                color = COLOR_PRIMARY
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, COLOR_ACCENT, rect, 3, border_radius=12)

            # Renderiza texto centralizado
            txt_surf = font.render(text, True, COLOR_TEXT)
            txt_rect = txt_surf.get_rect(center=rect.center)
            screen.blit(txt_surf, txt_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
