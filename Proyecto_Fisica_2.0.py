import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def calcular_resistencia():
    try:
        resistividad = float(entry_resistividad.get())
        longitud = float(entry_longitud.get())
        area = float(entry_area.get())

        if area <= 0 or longitud <= 0:
            resultado.set("¡Longitud y área deben ser mayores que 0!")
            return

        resistencia = resistividad * (longitud / area)
        resultado.set(f"Resistencia: {resistencia:.2f} Ω")

        # Generar datos para gráfico
        longitudes = np.linspace(0.1, 2 * longitud, 100)
        resistencias = resistividad * (longitudes / area)

        # Actualizar gráfica
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(longitudes, resistencias, label="R = ρ (L/A)")
        ax.set_xlabel("Longitud (L) [m]")
        ax.set_ylabel("Resistencia (R) [Ω]")
        ax.set_title("Relación Longitud vs Resistencia")
        ax.legend()
        ax.grid()
        canvas.draw()

    except ValueError:
        resultado.set("¡Por favor ingresa valores numéricos válidos!")

# Configurar la ventana principal
root = tk.Tk()
root.title("Simulador de Resistividad")

# Variables de entrada
entry_resistividad = tk.StringVar()
entry_longitud = tk.StringVar()
entry_area = tk.StringVar()
resultado = tk.StringVar()

# Interfaz
ttk.Label(root, text="Resistividad (ρ) [Ω·m]:").grid(column=0, row=0, padx=5, pady=5, sticky="w")
ttk.Entry(root, textvariable=entry_resistividad).grid(column=1, row=0, padx=5, pady=5)

ttk.Label(root, text="Longitud (L) [m]:").grid(column=0, row=1, padx=5, pady=5, sticky="w")
ttk.Entry(root, textvariable=entry_longitud).grid(column=1, row=1, padx=5, pady=5)

ttk.Label(root, text="Área (A) [m²]:").grid(column=0, row=2, padx=5, pady=5, sticky="w")
ttk.Entry(root, textvariable=entry_area).grid(column=1, row=2, padx=5, pady=5)

ttk.Button(root, text="Calcular Resistencia", command=calcular_resistencia).grid(column=0, row=3, columnspan=2, pady=10)

ttk.Label(root, textvariable=resultado, foreground="blue").grid(column=0, row=4, columnspan=2, pady=5)

# Gráfica integrada
fig = Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=0, row=5, columnspan=2)

root.mainloop()
