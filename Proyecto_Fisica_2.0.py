import pygame
import sys
import random
import math

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

#Datos de la tabla  
datos_tabla = [
    {"L(m)": 0.04, "R(Ohmios)": 0.5},
    {"L(m)": 0.14, "R(Ohmios)": 0.6},
    {"L(m)": 0.455, "R(Ohmios)": 0.7},
    {"L(m)": 0.632, "R(Ohmios)": 0.8},
    {"L(m)": 1.03, "R(Ohmios)": 0.9},
]

# Parámetros iniciales
diametro = 0.01  # Diámetro en metros
area = (math.pi * (diametro ** 2)) / 4
valor_teorico = 7.66e-8  # Resistividad teórica en Ω·m

# Cálculos dinámicos
pendiente = 0.0
resistividad_exp = 0.0
error_porcentual = 0.0

# Estados del programa
MENU = "menu"
CALCULAR_RESISTENCIA = "calcular_resistencia"
GUIA = "guia"

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



def calcular_pendiente(datos):
    try:
        longitudes = [dato["L(m)"] for dato in datos if dato["L(m)"] != 0.0]
        resistencias = [dato["R(Ohmios)"] for dato in datos if dato["R(Ohmios)"] != 0.0]
        if len(longitudes) > 1:
            return (resistencias[-1] - resistencias[0]) / (longitudes[-1] - longitudes[0])
    except Exception as e:
        print(f"Error al calcular pendiente: {e}")
        return 0.0
    return 0.0

# Función para calcular resistividad experimental y error porcentual
def calcular_resistividad_y_error(area, pendiente, valor_teorico):
    try:
        p_exp = area * pendiente
        error = abs((valor_teorico - p_exp) / valor_teorico) * 100
        return p_exp, error
    except Exception as e:
        print(f"Error al calcular resistividad: {e}")
        return 0.0, 0.0
    
# Función para mostrar la guía con las tablas
def mostrar_guia():
    global datos_tabla, pendiente, resistividad_exp, error_porcentual

    screen.fill(WHITE)

    # Título
    titulo = font.render("Guía: Tablas y Cálculos", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 20))

    # Encabezados de la tabla
    encabezados = ["L(m)", "R(Ohmios)"]
    x_inicio, y_inicio = 50, 100
    for i, encabezado in enumerate(encabezados):
        texto = font.render(encabezado, True, BLACK)
        screen.blit(texto, (x_inicio + i * 200, y_inicio))

    # Mostrar filas de la tabla
    for i, fila in enumerate(datos_tabla):
        for j, key in enumerate(encabezados):
            valor = fila[key]
            cuadro = pygame.Rect(x_inicio + j * 200, y_inicio + 40 + i * 40, 180, 30)
            pygame.draw.rect(screen, GRAY, cuadro)
            pygame.draw.rect(screen, BLACK, cuadro, 2)

            # Texto dentro de la celda
            texto = font.render(f"{valor:.3f}", True, BLACK)
            screen.blit(texto, (cuadro.x + 10, cuadro.y + 5))

    # Botón para añadir filas
    boton_añadir = draw_button(x_inicio, y_inicio + 40 + len(datos_tabla) * 40, 200, 40, "Añadir Fila")

    # Calcular valores dinámicos
    pendiente = calcular_pendiente(datos_tabla)
    resistividad_exp, error_porcentual = calcular_resistividad_y_error(area, pendiente, valor_teorico)

    # Mostrar resultados
    resultados = [
        f"Área (A): {area:.6e} m²",
        f"Pendiente: {pendiente:.3f}",
        f"Resistividad Experimental: {resistividad_exp:.6e} Ω·m",
        f"Error %: {error_porcentual:.2f}%",
    ]
    for i, resultado in enumerate(resultados):
        texto = font.render(resultado, True, BLACK)
        screen.blit(texto, (WIDTH // 2 - 300, 400 + i * 30))

    # Botón para volver al menú
    boton_volver = draw_button(WIDTH - 250, HEIGHT - 100, 200, 50, "Volver al Menú")

    return {"añadir": boton_añadir, "volver": boton_volver}

# Pantalla de menú
def mostrar_menu():
    screen.fill(WHITE)
    titulo = font.render("Simulador de Resistividad", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
    boton_resistencia = draw_button(WIDTH // 2 - 100, 150, 200, 50, "Calcular Resistencia")
    boton_guia = draw_button(WIDTH // 2 - 100, 250, 200, 50, "Guía de Programación")
    return {"resistencia": boton_resistencia,"guia":boton_guia}

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
    elif estado_actual == GUIA:
        botones = mostrar_guia()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado_actual == MENU:
                if botones["resistencia"].collidepoint(event.pos):
                    estado_actual = CALCULAR_RESISTENCIA
                elif botones["guia"].collidepoint(event.pos):
                    estado_actual = GUIA
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
            elif estado_actual == GUIA:
                # Verificar botones en la guía
                if botones["volver"].collidepoint(event.pos):
                    estado_actual = MENU
                elif botones["añadir"].collidepoint(event.pos):
                    datos_tabla.append({"L(m)": 0.0, "R(Ohmios)": 0.0})

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