import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Resistividad")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Variables iniciales
resistividad = 1.0  # Ω·cm
longitud = 10.0     # cm
area = 7.0          # cm²
resistencia = 0.0   # Ω

# Estados del programa
MENU = "menu"
CALCULAR_RESISTENCIA = "calcular_resistencia"

# Fuente
font = pygame.font.SysFont("Arial", 24)

# Clase para representar una carga
class Carga:
    def __init__(self, x, y, velocidad):
        self.x = x
        self.y = y
        self.velocidad = velocidad

    def mover(self, limite_derecho, limite_izquierdo, limite_superior, limite_inferior):
        self.x += self.velocidad
        if self.x > limite_derecho:  # Si sale por la derecha, reaparece a la izquierda
            self.x = limite_izquierdo
            self.y = random.randint(limite_superior, limite_inferior)  # Reposicionar dentro del área
        # Asegurar que la carga esté dentro de los límites verticales
        if self.y < limite_superior or self.y > limite_inferior:
            self.y = random.randint(limite_superior, limite_inferior)

    def dibujar(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# Crear una lista de cargas
cargas = []

def inicializar_cargas(num_cargas, x_inicio, y_inicio, longitud_px, altura_px):
    global cargas
    cargas = []
    limite_superior = y_inicio - altura_px // 2
    limite_inferior = y_inicio + altura_px // 2
    for _ in range(num_cargas):
        x = random.randint(x_inicio, x_inicio + longitud_px)
        y = random.randint(limite_superior, limite_inferior)
        velocidad = random.uniform(1, 3)  # Velocidad aleatoria de las cargas
        cargas.append(Carga(x, y, velocidad))

# Función para calcular la resistencia
def calcular_resistencia(rho, L, A):
    if A <= 0:  # Evitar división por cero
        return 0
    return rho * (L / A)

# Función para dibujar sliders
def draw_slider(x, y, value, label, min_value=0.1, max_value=10.0, unit=""):
    pygame.draw.rect(screen, GRAY, (x, y, 300, 10))  # Línea base
    handle_x = x + int((value - min_value) / (max_value - min_value) * 300)
    pygame.draw.circle(screen, BLUE, (handle_x, y + 5), 10)  # Controlador
    value_text = font.render(f"{label}: {value:.2f} {unit}", True, BLACK)
    screen.blit(value_text, (x, y - 30))
    return handle_x

# Función para dibujar el material cilíndrico con cargas dentro
def dibujar_material_cilindrico(x, y, longitud, area):
    longitud_px = int(20 + longitud * 20)  # Escala para la longitud
    altura_px = int(10 + area * 10)        # Escala para el área

    # Dibujar el cuerpo del cilindro (rectángulo)
    rect = pygame.Rect(x, y - altura_px // 2, longitud_px, altura_px)
    pygame.draw.rect(screen, BROWN, rect)  # Dibujar el cuerpo
    pygame.draw.rect(screen, BLACK, rect, 2)  # Bordes del cuerpo

    # Dibujar los extremos del cilindro (óvalos)
    pygame.draw.ellipse(screen, BROWN, (x - altura_px // 2, y - altura_px // 2, altura_px, altura_px))
    pygame.draw.ellipse(screen, BROWN, (x + longitud_px - altura_px // 2, y - altura_px // 2, altura_px, altura_px))

    # Bordes de los extremos
    pygame.draw.ellipse(screen, BLACK, (x - altura_px // 2, y - altura_px // 2, altura_px, altura_px), 2)
    pygame.draw.ellipse(screen, BLACK, (x + longitud_px - altura_px // 2, y - altura_px // 2, altura_px, altura_px), 2)

    # Dibujar cargas dentro del cilindro
    limite_izquierdo = x
    limite_derecho = x + longitud_px
    limite_superior = y - altura_px // 2
    limite_inferior = y + altura_px // 2

    for carga in cargas:
        carga.mover(limite_derecho, limite_izquierdo, limite_superior, limite_inferior)  # Limitar cargas al interior
        carga.dibujar()

# Pantalla de calcular resistencia
def calcular_resistencia_interfaz():
    global resistividad, longitud, area
    screen.fill(WHITE)

    # Título
    titulo = font.render("Cálculo de la Resistencia", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))

    # Fórmula gráfica
    formula_text = font.render("R = ρ * L / A", True, BLACK)
    screen.blit(formula_text, (WIDTH // 2 - 100, 100))

    # Dibujar sliders interactivos
    resistividad_x = draw_slider(50, 150, resistividad, "Resistividad (ρ)", 0.1, 10.0, "Ω·cm")
    longitud_x = draw_slider(50, 250, longitud, "Longitud (L)", 0.1, 20.0, "cm")
    area_x = draw_slider(50, 350, area, "Área (A)", 0.1, 15.0, "cm²")

    # Calcular resistencia
    resistencia_local = calcular_resistencia(resistividad, longitud, area)

    # Mostrar resistencia dinámica
    resistencia_label = font.render(f"Resistencia = {resistencia_local:.2f} Ω", True, BLACK)
    screen.blit(resistencia_label, (50, 450))

    # Dibujar material dinámico como un cilindro con cargas
    dibujar_material_cilindrico(800, 300, longitud, area)

    # Botones
    boton_volver = draw_button(50, 500, 200, 50, "Volver al Menú")
    boton_reset = draw_button(300, 500, 200, 50, "Reiniciar Valores")

    return boton_volver, boton_reset, resistividad_x, longitud_x, area_x

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
    boton_resistencia = draw_button(WIDTH // 2 - 100, 150, 200, 50, "Calcular Resistencia")
    return {"resistencia": boton_resistencia}

# Bucle principal
estado_actual = MENU
running = True
dragging = None

# Inicializar cargas con dimensiones iniciales
inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10))

while running:
    screen.fill(WHITE)
    if estado_actual == MENU:
        botones = mostrar_menu()
    elif estado_actual == CALCULAR_RESISTENCIA:
        boton_volver, boton_reset, resistividad_x, longitud_x, area_x = calcular_resistencia_interfaz()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado_actual == MENU:
                if botones["resistencia"].collidepoint(event.pos):
                    estado_actual = CALCULAR_RESISTENCIA
            elif estado_actual == CALCULAR_RESISTENCIA:
                if boton_volver.collidepoint(event.pos):
                    estado_actual = MENU
                elif boton_reset.collidepoint(event.pos):
                    resistividad, longitud, area = 1.0, 10.0, 7.0
                    inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10))  # Reiniciar cargas
                elif abs(event.pos[0] - resistividad_x) < 15 and abs(event.pos[1] - 150) < 15:
                    dragging = "resistividad"
                elif abs(event.pos[0] - longitud_x) < 15 and abs(event.pos[1] - 250) < 15:
                    dragging = "longitud"
                elif abs(event.pos[0] - area_x) < 15 and abs(event.pos[1] - 350) < 15:
                    dragging = "area"
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    if dragging:
        mouse_x = pygame.mouse.get_pos()[0]
        if dragging == "resistividad":
            resistividad = max(0.1, min(10.0, (mouse_x - 50) / 300 * 10.0))
        elif dragging == "longitud":
            longitud = max(0.1, min(20.0, (mouse_x - 50) / 300 * 20.0))
            inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10))  # Actualizar cargas
        elif dragging == "area":
            area = max(0.1, min(15.0, (mouse_x - 50) / 300 * 15.0))
            inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10))  # Actualizar cargas

    pygame.display.flip()

pygame.quit()
sys.exit()
