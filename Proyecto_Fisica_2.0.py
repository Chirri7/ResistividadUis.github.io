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
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Variables iniciales
resistividad = 1.0  # Ω·m
longitud = 1.0  # m
area = 1.0  # m²
resistencia = 0.0  # Ω

# Fuente
font = pygame.font.SysFont("Arial", 24)

# Función para calcular la resistencia
def calcular_resistencia(rho, L, A):
    if A <= 0:  # Evitar división por cero
        return 0
    return rho * (L / A)

# Función para dibujar sliders
def draw_slider(x, y, value, label, min_value=0.1, max_value=10.0):
    pygame.draw.rect(screen, GRAY, (x, y, 300, 10))  # Línea base
    handle_x = x + int((value - min_value) / (max_value - min_value) * 300)
    pygame.draw.circle(screen, BLUE, (handle_x, y + 5), 10)  # Controlador
    value_text = font.render(f"{label}: {value:.2f}", True, BLACK)
    screen.blit(value_text, (x, y - 30))
    return handle_x

# Bucle principal
running = True
dragging = None
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

    # Dibujar etiquetas
    resistencia_label = font.render(f"Resistencia (R): {resistencia:.2f} Ω", True, RED)
    screen.blit(resistencia_label, (50, 400))

    # Dibujar sliders
    resistividad_x = draw_slider(50, 100, resistividad, "Resistividad (ρ)")
    longitud_x = draw_slider(50, 200, longitud, "Longitud (L)")
    area_x = draw_slider(50, 300, area, "Área (A)")

    # Dibujar tubo representando resistencia
    tube_width = int(50 + resistencia * 10)
    pygame.draw.rect(screen, LIGHT_BLUE, (500, 250, tube_width, 50))
    pygame.draw.rect(screen, BLUE, (500, 250, tube_width, 50), 3)  # Borde

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
