import pygame
import sys
import random
import math

# Inicialización de Pygame
pygame.init()

pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.QUIT])

# Configuración de la ventana
WIDTH, HEIGHT = 1300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Resistividad")

# Forzar el enfoque en la ventana de Pygame
pygame.event.set_grab(True)

# Colores
WHITE = (255, 255, 255)     
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

#DATOS DE SIMULADOR

# Variables iniciales
resistividad = 1.0  # Ω·cm
longitud = 10.0     # cm
area = 7.0          # cm²
resistencia = 0.0   # Ω

material_seleccionado = "Cobre"
#Materiales
materiales = {
    "Cobre": {"resistividad": 1.71e-8, "resistencia": 0.5, "color": (184, 115, 51)},  # Color cobrizo
    "Aluminio": {"resistividad": 2.82e-8, "resistencia": 0.6, "color": (211, 211, 211)},  # Color plateado
    "Oro": {"resistividad": 2.35e-8, "resistencia": 0.7, "color": (255, 215, 0)},  # Color dorado
    "Plata": {"resistividad": 1.59e-8, "resistencia": 0.4, "color": (192, 192, 192)}  # Color gris plateado
}

#DATOS DE GUIA

#Datos de la tabla  
datos_tabla = []
selected_cell = None  # Celda seleccionada
input_text = ""  # Texto temporal para entrada

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
CALCULAR_RESISTIVIDAD = "calcular_resistividad"
GUIA = "guia"

# Variable global para el diámetro y estado de la caja de texto
diametro = 0.01  # Valor inicial en metros
diametro_input = ""  # Texto de entrada para el diámetro
diametro_activo = False  # Estado de la caja de texto (si está activa)


# Fuente
font = pygame.font.SysFont("Arial", 24)

# Clase para representar una carga
class Carga:
    def __init__(self, x, y, velocidad):
        self.x = x
        self.y = y
        self.velocidad = velocidad
    
    def actualizar_velocidad(self, resistividad):
        # Ajusta la velocidad en función de la resistividad (a mayor resistividad, menor velocidad)
        self.velocidad = max(0.1, 1.0 / (resistividad * 1e8))  # Normalización para ajustar la escala


    def mover(self, limite_derecho, limite_izquierdo, limite_superior, limite_inferior):
        self.x += self.velocidad
        if self.x > limite_derecho:  # Si sale por la derecha, reaparece a la izquierda
            self.x = limite_izquierdo
            
        # Asegurar que la carga esté dentro de los límites verticales
        if self.y < limite_superior or self.y > limite_inferior:
            self.y = random.randint(limite_superior, limite_inferior)

    def dibujar(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# Crear una lista de cargas
cargas = []
     
# Función para dibujar sliders
def draw_slider(x, y, value, label, min_value=0.1, max_value=10.0, unit=""):
    pygame.draw.rect(screen, GRAY, (x, y, 300, 10))  # Línea base
    handle_x = x + int((value - min_value) / (max_value - min_value) * 300)
    pygame.draw.circle(screen, BLUE, (handle_x, y + 5), 10)  # Controlador
    value_text = font.render(f"{label}: {value:.2f} {unit}", True, BLACK)
    screen.blit(value_text, (x, y - 30))
    return handle_x
# Función para dibujar el material cilíndrico con cargas dentro
def dibujar_material_cilindrico(x, y, longitud, area,color):
    longitud_px = int(20 + longitud * 20)  # Escala para la longitud
    altura_px = int(10 + area * 10)        # Escala para el área

    # Dibujar el cuerpo del cilindro (rectángulo)
    rect = pygame.Rect(x, y - altura_px // 2, longitud_px, altura_px)
    pygame.draw.rect(screen, color, rect)  # Dibujar el cuerpo
    pygame.draw.rect(screen, BLACK, rect, 2)  # Bordes del cuerpo

    # Dibujar los extremos del cilindro (óvalos)
    pygame.draw.ellipse(screen, color, (x - altura_px // 2, y - altura_px // 2, altura_px, altura_px))
    pygame.draw.ellipse(screen, color, (x + longitud_px - altura_px // 2, y - altura_px // 2, altura_px, altura_px))

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

def draw_material_selector(x, y, materiales, material_seleccionado):
    pygame.draw.rect(screen, GRAY, (x, y, 200, 40))  # Fondo del selector
    pygame.draw.rect(screen, BLACK, (x, y, 200, 40), 2)  # Borde del selector
    
    # Texto del material seleccionado
    texto_material = font.render(f"Material: {material_seleccionado}", True, BLACK)
    screen.blit(texto_material, (x + 10, y + 10))

    # Dibujar una lista desplegable cuando se haga clic (opcional, puede ser interactivo)
    return pygame.Rect(x, y, 200, 40)  # Retorna el rectángulo del selector

# Pantalla de calcular resistencia
def calcular_resistividad_interfaz():
    global resistividad, longitud, area
    screen.fill(WHITE)

    # Título
    titulo = font.render("Calular Resistividad", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))

    # Fórmula gráfica
    formula_text = font.render("ρ = R * A / L", True, BLACK)
    screen.blit(formula_text, (WIDTH // 2 - 100, 100))

    # Dibujar sliders interactivos
    longitud_x = draw_slider(50, 250, longitud, "Longitud (L)", 0.1, 20.0, "cm")
    area_x = draw_slider(50, 350, area, "Área (A)", 0.1, 15, "cm²")
    
    # Dibujar el selector de materiales
    selector_rect = draw_material_selector(50, 100, materiales, material_seleccionado)
    
    # Obtener la resistividad teórica del material seleccionado
    resistividad_teorica = materiales[material_seleccionado]
    
    # Obtener datos del material seleccionado
    datos_material = materiales[material_seleccionado]
    resistividad_teorica = datos_material["resistividad"]  # Resistividad teórica del material
    resistencia_material = datos_material["resistencia"]  # Resistencia característica del material
    color_material = datos_material["color"]

    # Convertir unidades de longitud y área
    longitud_metros = longitud / 100  # Convertir de cm a m
    area_metros = area / 10000        # Convertir de cm² a m²

    # Calcular resistividad experimental
    if longitud_metros > 0:
        resistividad_experimental = resistencia_material * (area_metros / longitud_metros)
    else:
        resistividad_experimental = 0
        
    # Mostrar resistividad teórica y experimental
    resistividad_teorica_label = font.render(f"Resistividad Teórica: {resistividad_teorica:.2e} Ω·m", True, BLACK)
    resistividad_experimental_label = font.render(f"Resistividad Experimental: {resistividad_experimental:.2e} Ω·m", True, BLACK)

    screen.blit(resistividad_teorica_label, (700, 430))
    screen.blit(resistividad_experimental_label, (700, 470))
    
    # Actualizar velocidades de las cargas
    for carga in cargas:
        carga.actualizar_velocidad(resistividad_teorica)

    # Dibujar material dinámico como un cilindro con cargas
    dibujar_material_cilindrico(800, 300, longitud, area,color_material)

    # Botones
    boton_volver = draw_button(50, 500, 200, 50, "Volver al Menú")
    boton_reset = draw_button(300, 500, 200, 50, "Reiniciar Valores")

    return boton_volver, boton_reset, longitud_x, area_x, selector_rect      

def inicializar_cargas(num_cargas, x_inicio, y_inicio, longitud_px, altura_px,resistividad):
    global cargas
    cargas = []
    y_centro = y_inicio  # Mantener las cargas centradas verticalmente
    for _ in range(num_cargas):
        x = random.randint(x_inicio, x_inicio + longitud_px)  # Posición horizontal aleatoria
        velocidad = max(0.2, 1.0 / (resistividad * 1e8))  # Velocidad basada en la resistividad
        cargas.append(Carga(x, y_centro, velocidad))

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
x_inicio, y_inicio = 50, 100
ancho_celda, alto_celda = 200, 40
def mostrar_guia():
    global datos_tabla, pendiente, resistividad_exp, error_porcentual,selected_cell, input_text

    screen.fill(WHITE)

    # Título
    titulo = font.render("Guía: Tablas y Cálculos", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 20))
    
    # Dibujar una tabla estructurada
    encabezados = ["L(m)", "R(Ohmios)"]
    x_inicio, y_inicio = 50, 100
    ancho_celda, alto_celda = 200, 40
    
    # Dibujar encabezados
    for i, encabezado in enumerate(encabezados):
        pygame.draw.rect(screen, BLACK, (x_inicio + i * ancho_celda, y_inicio, ancho_celda, alto_celda), 2)
        texto = font.render(encabezado, True, BLACK)
        screen.blit(texto, (x_inicio + i * ancho_celda + 10, y_inicio + 10))
        
    # Dibujar filas de la tabla
    for fila_idx, fila in enumerate(datos_tabla):
        for col_idx, key in enumerate(encabezados):
            celda_x = x_inicio + col_idx * ancho_celda
            celda_y = y_inicio + (fila_idx + 1) * alto_celda

            # Dibujar la celda
            pygame.draw.rect(screen, BLACK, (celda_x, celda_y, ancho_celda, alto_celda), 2)
        
            # Mostrar `input_text` dinámicamente si la celda está seleccionada
            if selected_cell == (fila_idx, col_idx):
                texto = font.render(input_text, True, BLUE)
            else:
                valor = fila[key]
                texto = font.render(f"{valor:.3f}" if isinstance(valor, float) else str(valor), True, BLACK)
            
            screen.blit(texto, (celda_x + 10, celda_y + 10))

            # Resaltar la celda seleccionada
            if selected_cell == (fila_idx, col_idx):
                pygame.draw.rect(screen, BLUE, (celda_x, celda_y, ancho_celda, alto_celda), 3)



    # Botón para añadir filas
    boton_añadir = draw_button(x_inicio, y_inicio + 40 + len(datos_tabla) * 40, 200, 40, "Añadir Fila")
    
    # Botón para eliminar filas
    boton_eliminar = draw_button(x_inicio + ancho_celda + 10, y_inicio + (len(datos_tabla) + 1) * alto_celda, ancho_celda, alto_celda, "Eliminar Fila")

    # Dibujar caja de texto para el diámetro
    diametro_caja = pygame.Rect(1000, 200, 200, 40)
    pygame.draw.rect(screen, GRAY if not diametro_activo else WHITE, diametro_caja)
    pygame.draw.rect(screen, BLACK, diametro_caja, 2)
    texto_diametro = font.render(diametro_input if diametro_activo else f"{diametro:.2f}", True, BLACK)
    screen.blit(texto_diametro, (diametro_caja.x + 10, diametro_caja.y + 10))

    # Etiqueta para la caja de texto
    etiqueta_diametro = font.render("Diámetro (d) en metros:", True, BLACK)
    screen.blit(etiqueta_diametro, (1000, 170))

    # Calcular el área basada en el diámetro
    area = math.pi * (diametro ** 2) / 4

    # Calcular valores dinámicos
    pendiente = calcular_pendiente(datos_tabla)
    resistividad_exp, error_porcentual = calcular_resistividad_y_error(area, pendiente, valor_teorico)
    
    # Dibujar caja de resultados
    resultados_x = x_inicio + len(encabezados) * ancho_celda + 50
    resultados_y = y_inicio
    ancho_resultados = 400
    alto_resultados = 200
    
    # Fondo de la caja de resultados
    pygame.draw.rect(screen, GRAY, (resultados_x, resultados_y, ancho_resultados, alto_resultados))
    pygame.draw.rect(screen, BLACK, (resultados_x, resultados_y, ancho_resultados, alto_resultados), 2)

    # Mostrar resultados dentro de la caja
    resultados = [
        f"Área (A): {area:.6e} m²",
        f"Pendiente: {pendiente:.3f}",
        f"Resistividad Experimental: {resistividad_exp:.6e} Ω·m",
        f"Error %: {error_porcentual:.2f}%",
    ]
    for i, resultado in enumerate(resultados):
        texto = font.render(resultado, True, BLACK)
        screen.blit(texto, (resultados_x + 10, resultados_y + 10 + i * 40))

    # Botón para volver al menú
    boton_volver = draw_button(WIDTH - 250, HEIGHT - 100, 200, 50, "Volver al Menú")

    return {"añadir": boton_añadir,"eliminar": boton_eliminar,"volver": boton_volver,"diametro_caja": diametro_caja}, x_inicio, y_inicio, ancho_celda, alto_celda

# Pantalla de menú
def mostrar_menu():
    screen.fill(WHITE)
    titulo = font.render("Simulador de Resistividad", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
    boton_resistencia = draw_button(WIDTH // 2 - 100, 150, 200, 50, "Calcular Resistividad")
    boton_guia = draw_button(WIDTH // 2 - 100, 250, 200, 50, "Guía de Programación")
    return {"resistencia": boton_resistencia,"guia":boton_guia}

# Bucle principal
estado_actual = MENU
running = True
dragging = None

# Obtén los datos del material seleccionado
datos_material = materiales[material_seleccionado]
resistencia_material = datos_material["resistencia"]  # Resistencia característica del material

if longitud > 0:
    resistividad_experimental = resistencia_material * (area / longitud)
else:
    resistividad_experimental = 0  # Manejo de longitud cero para evitar división por cero

inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10), resistividad_experimental)



running=True
while running:
    pygame.event.set_grab(True)
    screen.fill(WHITE)
    if estado_actual == MENU:
        botones = mostrar_menu()
    elif estado_actual == CALCULAR_RESISTIVIDAD:
        boton_volver, boton_reset, longitud_x, area_x, selector_rect = calcular_resistividad_interfaz()
    elif estado_actual == GUIA:
        botones, x_inicio, y_inicio, ancho_celda, alto_celda = mostrar_guia()

    #Mnaejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Evento de click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if estado_actual == MENU:
                if botones["resistencia"].collidepoint(event.pos):
                    estado_actual = CALCULAR_RESISTIVIDAD
                elif botones["guia"].collidepoint(event.pos):
                    estado_actual = GUIA
                    
            elif estado_actual == CALCULAR_RESISTIVIDAD:
                if boton_volver.collidepoint(event.pos):
                    estado_actual = MENU
                elif boton_reset.collidepoint(event.pos):
                    #Reiniciar valores  
                    resistividad, longitud, area = 1.0, 10.0, 7.0
                    inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10), resistividad_experimental)
                elif abs(event.pos[0] - longitud_x) < 15 and abs(event.pos[1] - 250) < 15:
                    dragging = "longitud"
                elif abs(event.pos[0] - area_x) < 15 and abs(event.pos[1] - 350) < 15:
                    dragging = "area"
                elif selector_rect.collidepoint(event.pos):
                    # Cambiar material seleccionado (rotar entre opciones como ejemplo)
                    material_keys = list(materiales.keys())
                    current_index = material_keys.index(material_seleccionado)
                    material_seleccionado = material_keys[(current_index + 1) % len(material_keys)]
                    
                    # Actualizar resistividad y reinicializar cargas
                    datos_material = materiales[material_seleccionado]
                    resistividad_teorica = datos_material["resistividad"]
                    inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10), resistividad_experimental)
            elif estado_actual == GUIA:
                #Activar/desactivar la caja de texto del diámetro
                if botones["diametro_caja"].collidepoint(event.pos):
                    diametro_activo = not diametro_activo
                    print(f"Celda seleccionada: {diametro_activo}")
                else:
                    diametro_activo = False
                #Detectar click dentro de la tabla  
                # Detectar clic dentro de la tabla (solo si la caja de texto no está activa)
                if not diametro_activo and len(datos_tabla) > 0:
                    if x_inicio <= mouse_x <= x_inicio + len(datos_tabla[0]) * ancho_celda:
                        if y_inicio + alto_celda <= mouse_y <= y_inicio + (len(datos_tabla) + 1) * alto_celda:
                            col_idx = (mouse_x - x_inicio) // ancho_celda
                            fila_idx = (mouse_y - y_inicio - alto_celda) // alto_celda
                            selected_cell = (fila_idx, col_idx)
                            input_text = ""  # Limpiar texto previo
                            print(f"Celda seleccionada: {selected_cell}")
                elif not diametro_activo and len(datos_tabla) == 0:
                    print("La tabla está vacía, añade una fila para interactuar.")
                # Verificar botones en la guía
                if botones["volver"].collidepoint(event.pos):
                    estado_actual = MENU
                elif botones["añadir"].collidepoint(event.pos):
                    datos_tabla.append({"L(m)": 0.0, "R(Ohmios)": 0.0})
                elif botones["eliminar"].collidepoint(event.pos):
                    if len(datos_tabla) > 0:  # Verificar que haya filas antes de eliminar
                        datos_tabla.pop()  # Eliminar la última fila     
                               
        #Eventos de teclado         
        elif event.type == pygame.KEYDOWN:
            # Manejar entrada en la caja de texto del diámetro
            if diametro_activo:
                if event.key == pygame.K_RETURN:  # Finalizar entrada
                    try:
                        diametro = float(diametro_input)  # Convertir texto a número
                        print(f"Nuevo diámetro ingresado: {diametro}")
                    except ValueError:
                        print("Entrada inválida, ingrese un número válido.")
                    diametro_input = ""  # Limpiar entrada
                    diametro_activo = False
                elif event.key == pygame.K_BACKSPACE:
                    diametro_input = diametro_input[:-1]  # Borrar último carácter
                else:
                    diametro_input += event.unicode  # Agregar carácter
            elif selected_cell is not None:
                print(f"Tecla presionada: {event.unicode}")
                fila, col = selected_cell
                encabezado = ["L(m)", "R(Ohmios)"][col]
                if event.key == pygame.K_RETURN:  # Guardar valor al presionar Enter
                    try:
                        datos_tabla[fila][encabezado] = float(input_text)  # Convierte y guarda
                    except ValueError:
                        print(f"Valor no válido: {input_text}")
                    selected_cell = None  # Deseleccionar celda
                    input_text = ""  # Limpiar texto
                elif event.key == pygame.K_BACKSPACE:  # Borrar último carácter
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # Agregar carácter
                    print(f"Texto actual: {input_text}")
           
            
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    if dragging:
        mouse_x = pygame.mouse.get_pos()[0]
        if dragging == "longitud":
            longitud = max(0.1, min(20.0, (mouse_x - 50) / 300 * 20.0))
            inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10), resistividad_experimental)
        elif dragging == "area":
            area = max(0.1, min(15.0, (mouse_x - 50) / 300 * 15.0))
            inicializar_cargas(20, 800, 300, int(20 + longitud * 20), int(10 + area * 10), resistividad_experimental)

    pygame.display.flip()

pygame.quit()
sys.exit()
