import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Resistividad")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Variables iniciales
resistividad = 1.0  # Ω·m
longitud = 1.0  # m
area = 1.0  # m²
resistencia = 0.0  # Ω

# Rango de valores para la barra
MIN_WIDTH = 50
MAX_WIDTH = 400
MAX_RESISTENCIA = 10.0  # Máxima resistencia para normalización
current_width = MIN_WIDTH  # Ancho actual de la barra (animado)

# Fuente
font = pygame.font.SysFont("Arial", 24)

# Función para calcular la resistencia
def calcular_resistencia(rho, L, A):
    if A <= 0:  # Evitar división por cero
        return 0
    return rho * (L / A)

# Función para normalizar el ancho de la barra
def calcular_ancho(resistencia):
    resistencia_normalizada = min(resistencia, MAX_RESISTENCIA)  # Limitar R al máximo permitido
    return MIN_WIDTH + (resistencia_normalizada / MAX_RESISTENCIA) * (MAX_WIDTH - MIN_WIDTH)

# Función para determinar el color de la barra según la resistencia
def calcular_color(resistencia):
    if resistencia < 3:
        return LIGHT_BLUE
    elif resistencia < 7:
        return YELLOW
    else:
        return RED

# Función para dibujar sliders
def draw_slider(x, y, value, label, min_value=0.1, max_value=10.0):
    pygame.draw.rect(screen, GRAY, (x, y, 300, 10))  # Línea base
    handle_x = x + int((value - min_value) / (max_value - min_value) * 300)
    pygame.draw.circle(screen, BLUE, (handle_x, y + 5), 10)  # Controlador
    value_text = font.render(f"{label}: {value:.2f}", True, BLACK)
    screen.blit(value_text, (x, y - 30))
    return handle_x

# Función para dibujar el botón de reinicio
def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)  # Borde negro
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)
    return pygame.Rect(x, y, width, height)

# Bucle principal
running = True
dragging = None
arrow_x = 500  # Posición inicial de la flecha
arrow_speed = 0.3  # Velocidad de movimiento de la flecha
while running:
    screen.fill(WHITE)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - resistividad_x) < 15 and abs(event.pos[1] - 100) < 15:
                dragging = "resistividad"
            if abs(event.pos[0] - longitud_x) < 15 and abs(event.pos[1] - 200) < 15:
                dragging = "longitud"
            if abs(event.pos[0] - area_x) < 15 and abs(event.pos[1] - 300) < 15:
                dragging = "area"
            # Detectar clic en el botón de reinicio
            if reset_button.collidepoint(event.pos):
                resistividad = 1.0
                longitud = 1.0
                area = 1.0
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    # Arrastrar sliders
    if dragging:
        mouse_x = pygame.mouse.get_pos()[0]
        if dragging == "resistividad":
            resistividad = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        if dragging == "longitud":
            longitud = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        if dragging == "area":
            area = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))

    # Cálculo de resistencia
    resistencia = calcular_resistencia(resistividad, longitud, area)
    target_width = calcular_ancho(resistencia)

    # Suavizar el cambio de tamaño de la barra
    if current_width < target_width:
        current_width += 1  # Incremento gradual
    elif current_width > target_width:
        current_width -= 1  # Decremento gradual

    # Dibujar etiquetas
    resistencia_label = font.render(f"Resistencia (R): {resistencia:.2f} Ω", True, RED)
    screen.blit(resistencia_label, (50, 400))

    # Dibujar sliders
    resistividad_x = draw_slider(50, 100, resistividad, "Resistividad (ρ)")
    longitud_x = draw_slider(50, 200, longitud, "Longitud (L)")
    area_x = draw_slider(50, 300, area, "Área (A)")

    # Dibujar tubo representando resistencia
    tube_color = calcular_color(resistencia)  # Calcular color según resistencia
    pygame.draw.rect(screen, BLACK, (500 - 5, 250 - 5, current_width + 10, 60), border_radius=10)  # Borde externo
    pygame.draw.rect(screen, tube_color, (500, 250, current_width, 50), border_radius=10)  # Tubo principal

    # Dibujar flechas para simular flujo de corriente
    arrow_x += arrow_speed  # Movimiento de la flecha
    if arrow_x > 500 + current_width:
        arrow_x = 500  # Reiniciar posición
    pygame.draw.polygon(screen, BLACK, [(arrow_x, 275), (arrow_x - 10, 265), (arrow_x - 10, 285)])  # Flecha

    # Dibujar botón de reinicio
    reset_button = draw_button(700, 500, 150, 50, "Reiniciar")

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
