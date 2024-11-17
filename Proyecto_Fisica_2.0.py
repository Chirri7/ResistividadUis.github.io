import pygame
import sys

# Inicialización de Pygame
pygame.init()  # pylint: disable=no-member

# Configuración de la ventana
WIDTH, HEIGHT = 1300, 600
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
MIN_BARRA = 50
MAX_BARRA = 400
MAX_RESISTENCIA = 10.0  # Máxima resistencia para normalización

# Estados del programa
MENU = "menu"
CALCULAR_AREA = "calcular_area"
CALCULAR_LONGITUD = "calcular_longitud"
CALCULAR_RESISTIVIDAD = "calcular_resistividad"
CALCULAR_RESISTENCIA = "calcular_resistencia"

estado_actual = MENU  # El programa empieza en el menú

# Fuente
font = pygame.font.SysFont("Arial", 24)  # pylint: disable=no-member

# Función para calcular la resistencia
def calcular_resistencia(rho, L, A):
    if A <= 0:  # Evitar división por cero
        return 0
    return rho * (L / A)

# Función para normalizar el ancho de la barra
def calcular_ancho(resistencia_local):
    resistencia_normalizada = min(resistencia_local, MAX_RESISTENCIA)
    return MIN_BARRA + (resistencia_normalizada / MAX_RESISTENCIA) * (MAX_BARRA - MIN_BARRA)

# Función para calcular el color dinámico
def calcular_color_dinamico(resistencia_local):
    start_color = (0, 255, 0)  # Verde para resistencia baja
    end_color = (255, 0, 0)    # Rojo para resistencia alta
    t = min(resistencia_local / MAX_RESISTENCIA, 1)  # Proporción (máximo 1.0)
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * t),
        int(start_color[1] + (end_color[1] - start_color[1]) * t),
        int(start_color[2] + (end_color[2] - start_color[2]) * t),
    )

# Función para dibujar la barra de resistencia con colores dinámicos
def dibujar_barra_dinamica(x, y, width, height, resistencia_local):
    for i in range(width):
        local_resistencia = (i / width) * resistencia_local
        color = calcular_color_dinamico(local_resistencia)
        pygame.draw.line(screen, color, (x + i, y), (x + i, y + height))

# Función para dibujar sliders
def draw_slider(x, y, value, label, min_value=0.1, max_value=10.0):
    pygame.draw.rect(screen, GRAY, (x, y, 300, 10))  # Línea base
    handle_x = x + int((value - min_value) / (max_value - min_value) * 300)
    pygame.draw.circle(screen, BLUE, (handle_x, y + 5), 10)  # Controlador
    value_text = font.render(f"{label}: {value:.2f}", True, BLACK)
    screen.blit(value_text, (x, y - 30))
    return handle_x

# Función para dibujar botones
def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)  # Borde negro
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)
    return pygame.Rect(x, y, width, height)

# Pantalla de menú
def mostrar_menu():
    screen.fill(WHITE)
    titulo = font.render("Simulador de Resistividad", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
    boton_area = draw_button(WIDTH // 2 - 100, 150, 200, 50, "Calcular Área")
    boton_longitud = draw_button(WIDTH // 2 - 100, 250, 200, 50, "Calcular Longitud")
    boton_resistividad = draw_button(WIDTH // 2 - 100, 350, 200, 50, "Calcular Resistividad")
    boton_resistencia = draw_button(WIDTH // 2 - 100, 450, 200, 50, "Calcular Resistencia")
    return {"area": boton_area, "longitud": boton_longitud, "resistividad": boton_resistividad, "resistencia": boton_resistencia}

# Pantalla de resistividad
def calcular_resistividad():
    global resistividad, longitud, area
    screen.fill(WHITE)
    titulo = font.render("Cálculo de la Resistividad", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
    resistividad_x = draw_slider(50, 100, resistividad, "Resistividad (ρ)")
    longitud_x = draw_slider(50, 200, longitud, "Longitud (L)")
    area_x = draw_slider(50, 300, area, "Área (A)")
    resistencia_local = calcular_resistencia(resistividad, longitud, area)
    target_width = calcular_ancho(resistencia_local)
    dibujar_barra_dinamica(500, 250, int(target_width), 50, resistencia_local)
    pygame.draw.rect(screen, BLACK, (500, 250, int(target_width), 50), 2)
    resistencia_label = font.render(f"Resistencia (R): {resistencia_local:.2f} Ω", True, BLACK)
    screen.blit(resistencia_label, (50, 400))
    boton_volver = draw_button(50, 500, 200, 50, "Volver al Menú")
    return boton_volver, resistividad_x, longitud_x, area_x

# Bucle principal
running = True
dragging = None
while running:
    screen.fill(WHITE)
    if estado_actual == MENU:
        botones = mostrar_menu()
    elif estado_actual == CALCULAR_RESISTIVIDAD:
        boton_volver, resistividad_x, longitud_x, area_x = calcular_resistividad()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
            if estado_actual == MENU:
                if botones["resistividad"].collidepoint(event.pos):
                    estado_actual = CALCULAR_RESISTIVIDAD
            elif estado_actual == CALCULAR_RESISTIVIDAD:
                if boton_volver.collidepoint(event.pos):
                    estado_actual = MENU
                elif abs(event.pos[0] - resistividad_x) < 15 and abs(event.pos[1] - 100) < 15:
                    dragging = "resistividad"
                elif abs(event.pos[0] - longitud_x) < 15 and abs(event.pos[1] - 200) < 15:
                    dragging = "longitud"
                elif abs(event.pos[0] - area_x) < 15 and abs(event.pos[1] - 300) < 15:
                    dragging = "area"
        elif event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
            dragging = None

    if dragging:
        mouse_x = pygame.mouse.get_pos()[0]
        if dragging == "resistividad":
            resistividad = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        elif dragging == "longitud":
            longitud = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        elif dragging == "area":
            area = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))

    pygame.display.flip()

pygame.quit()
sys.exit()
