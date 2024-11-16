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
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Variables iniciales
resistividad = 1.0  # Ω·m
longitud = 1.0  # m
area = 1.0  # m²
resistencia = 0.0  # Ω

# Rango de valores para la barra
MIN_WIDTH = 50
MAX_WIDTH = 400
MAX_RESISTENCIA = 10.0  # Máxima resistencia para normalización
current_width = MIN_WIDTH  # Ancho actual de la barra

# Fuente
font = pygame.font.SysFont("Arial", 24)

# Función para calcular la resistencia
def calcular_resistencia(rho, L, A):
    if A <= 0:  # Evitar división por cero
        return 0
    return rho * (L / A)

# Función para normalizar el ancho de la barra
def calcular_ancho(resistencia):
    """Normaliza el ancho de la barra según la resistencia."""
    resistencia_normalizada = min(resistencia, MAX_RESISTENCIA)
    return MIN_WIDTH + (resistencia_normalizada / MAX_RESISTENCIA) * (MAX_WIDTH - MIN_WIDTH)

# Función para calcular el color dinámico
def calcular_color_dinamico(resistencia):
    """Calcula un color dinámico según el valor de resistencia."""
    # Definir colores extremos
    start_color = (0, 255, 0)  # Verde para resistencia baja
    end_color = (255, 0, 0)    # Rojo para resistencia alta

    # Normalizar resistencia entre 0 y MAX_RESISTENCIA
    t = min(resistencia / MAX_RESISTENCIA, 1)  # Proporción (máximo 1.0)

    # Interpolar colores
    color = (
        int(start_color[0] + (end_color[0] - start_color[0]) * t),
        int(start_color[1] + (end_color[1] - start_color[1]) * t),
        int(start_color[2] + (end_color[2] - start_color[2]) * t),
    )
    return color

# Función para dibujar la barra de resistencia con colores dinámicos
def dibujar_barra_dinamica(x, y, width, height, resistencia):
    """Dibuja una barra con colores dinámicos basados en la resistencia."""
    for i in range(width):
        # Calcular resistencia local según la posición en la barra
        resistencia_local = (i / width) * resistencia
        color = calcular_color_dinamico(resistencia_local)
        pygame.draw.line(screen, color, (x + i, y), (x + i, y + height))

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
arrow_speed = 0.3  # Velocidad base de la flecha

while running:
    screen.fill(WHITE)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - resistividad_x) < 15 and abs(event.pos[1] - 100) < 15:
                dragging = "resistividad"
            elif abs(event.pos[0] - longitud_x) < 15 and abs(event.pos[1] - 200) < 15:
                dragging = "longitud"
            elif abs(event.pos[0] - area_x) < 15 and abs(event.pos[1] - 300) < 15:
                dragging = "area"
            elif reset_button.collidepoint(event.pos):
                resistividad, longitud, area = 1.0, 1.0, 1.0
                current_width = MIN_WIDTH  # Reiniciar barra también
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    # Arrastrar sliders
    if dragging:
        mouse_x = pygame.mouse.get_pos()[0]
        if dragging == "resistividad":
            resistividad = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        elif dragging == "longitud":
            longitud = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        elif dragging == "area":
            area = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))

    # Cálculo de resistencia
    resistencia = calcular_resistencia(resistividad, longitud, area)
    target_width = calcular_ancho(resistencia)

    # Suavizar el cambio de tamaño de la barra
    if abs(current_width - target_width) < 5:
        current_width = target_width
    elif current_width < target_width:
        current_width += 5
    elif current_width > target_width:
        current_width -= 5

    # Ajustar velocidad de la flecha según la resistencia
    arrow_speed = max(0.2, 2.0 - (resistencia / MAX_RESISTENCIA) * 1.8)

    # Dibujar etiquetas
    resistencia_label = font.render(f"Resistencia (R): {resistencia:.2f} Ω", True, BLACK)
    screen.blit(resistencia_label, (50, 400))

    # Dibujar sliders
    resistividad_x = draw_slider(50, 100, resistividad, "Resistividad (ρ)")
    longitud_x = draw_slider(50, 200, longitud, "Longitud (L)")
    area_x = draw_slider(50, 300, area, "Área (A)")

    # Dibujar barra con colores dinámicos
    dibujar_barra_dinamica(500, 250, int(current_width), 50, resistencia)
    pygame.draw.rect(screen, BLACK, (500, 250, int(current_width), 50), 2)

    # Dibujar flechas para simular flujo de corriente
    arrow_x += arrow_speed
    if arrow_x > 505 + current_width:
        arrow_x = 500
    pygame.draw.polygon(screen, BLACK, [(arrow_x, 275), (arrow_x - 10, 265), (arrow_x - 10, 285)])

    # Dibujar botón de reinicio
    reset_button = draw_button(700, 500, 150, 50, "Reiniciar")

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
