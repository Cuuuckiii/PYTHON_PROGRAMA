import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

datos = pd.read_csv('Datos21.csv', delimiter=';', encoding='latin1')

class PaginaInicio(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.crear_interfaz()

    def crear_interfaz(self):
        # Logo de la universidad (reemplaza 'upc.png' con la ruta de tu archivo de imagen)
        logo = tk.PhotoImage(file='upc.png')
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo  # Evitar que la imagen sea recolectada por el recolector de basura
        logo_label.pack()

        # Nombre del profesor
        nombre_profesor = tk.Label(self, text="Ramirez Espinoza, Juan Alfonso")
        nombre_profesor.pack()

        # Nombres de los integrantes del grupo
        nombres_integrantes = tk.Label(self, text="Jhon Aquino Ninasivincha (U20231E772), Kevin Tito Santiago Coarita Palacios(U20221C040) y Jhohandri Jhunior Contreras Quijua (U20211D925)")
        nombres_integrantes.pack()

        # Botón de empezar
        boton_empezar = tk.Button(self, text="Empezar", command=self.ir_a_reportes)
        boton_empezar.pack()

    def ir_a_reportes(self):
        # Cerrar la ventana actual
        self.destroy()

        # Crear la instancia de la página de reportes
        pagina_reportes = PaginaReportes(master=self.master)
        pagina_reportes.pack()

class PaginaReportes(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.crear_interfaz()

    def crear_interfaz(self):
        # Botones para los reportes
        reportes = [
            "Cantidad de residuos domiciliarios por año",  # Reporte 1
            "Cantidad de residuos de la población rural por departamento",  # Reporte 2
            "Cantidad de residuos municipales por departamento",  # Reporte 3
            "Cantidad de residuos no domiciliarios por reg_nat"  # Reporte 4
        ]

        for i, nombre_reporte in enumerate(reportes, start=1):
            boton_reporte = tk.Button(self, text=f"Reporte {i}: {nombre_reporte}", command=lambda i=i: self.mostrar_opciones(i))
            boton_reporte.pack()

        # Botón para volver a ver otro reporte
        boton_volver = tk.Button(self, text="Volver a ver otro reporte", command=self.volver_a_reportes)
        boton_volver.pack()

    def mostrar_opciones(self, numero_reporte):
        # Cerrar la ventana actual
        self.destroy()

        # Crear la instancia de la página de opciones
        pagina_opciones = PaginaOpciones(master=self.master, numero_reporte=numero_reporte)
        pagina_opciones.pack()

    def volver_a_reportes(self):
        # Cerrar la ventana actual
        self.destroy()

        # Crear la instancia de la página de reportes
        pagina_reportes = PaginaReportes(master=self.master)
        pagina_reportes.pack()

class PaginaOpciones(tk.Frame):
    def __init__(self, master=None, numero_reporte=None):
        super().__init__(master)
        self.master = master
        self.numero_reporte = numero_reporte
        self.departamentos_seleccionados = []  # Lista para almacenar departamentos seleccionados
        self.departamento_seleccionado = tk.StringVar()
        self.crear_interfaz()

    def ver_datos(self):
        # Obtener datos del departamento seleccionado y la columna correspondiente al número de reporte
        departamento_seleccionado = self.departamento_seleccionado.get()

        # Restringir la selección a un solo departamento si no se están comparando datos
        if not self.departamentos_seleccionados:
            self.departamentos_seleccionados = [departamento_seleccionado]

        for departamento in self.departamentos_seleccionados:
            # Aquí puedes realizar operaciones para cada departamento seleccionado
            datos_departamento = datos[datos['DEPARTAMENTO'] == departamento]

            # Crear un gráfico estadístico
            fig, ax = plt.subplots()
            ax.bar(datos_departamento['DEPARTAMENTO'], datos_departamento[self.get_columna_reporte()])
            ax.set_ylabel(f'Cantidad de {self.get_columna_reporte()}')
            ax.set_title(f'Reporte {self.numero_reporte}: {departamento}')

            # Mostrar el gráfico en la interfaz de Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def comparar_datos(self):
        # Verificar que haya al menos dos departamentos seleccionados para comparar
        if len(self.departamentos_seleccionados) < 2:
            messagebox.showinfo("Error", "Seleccione al menos dos departamentos para comparar.")
            return

        # Crear un gráfico comparativo
        fig, ax = plt.subplots()

        for departamento in self.departamentos_seleccionados:
            datos_departamento = datos[datos['DEPARTAMENTO'] == departamento]
            ax.bar(datos_departamento['DEPARTAMENTO'], datos_departamento[self.get_columna_reporte()], label=departamento)

        ax.set_ylabel(f'Cantidad de {self.get_columna_reporte()}')
        ax.set_title(f'Reporte {self.numero_reporte}: Comparación entre departamentos')
        ax.legend()

        # Mostrar el gráfico en la interfaz de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def get_columna_reporte(self):
        # Mapeo de número de reporte a columna
        columnas_reporte = {
            1: 'QRESIDUOS_DOM',
            2: 'POB_RURAL',  # Cambia esto según la columna correcta para el reporte 2
            3: 'QRESIDUOS_MUN',  # Cambia esto según la columna correcta para el reporte 3
            4: 'QRESIDUOS_NO_DOM'  # Cambia esto según la columna correcta para el reporte 4
        }

        return columnas_reporte[self.numero_reporte]

    def agregar_departamento(self):
        # Obtener el departamento seleccionado
        departamento_seleccionado = self.departamento_seleccionado.get()

        # Verificar si el departamento ya está en la lista
        if departamento_seleccionado not in self.departamentos_seleccionados:
            self.departamentos_seleccionados.append(departamento_seleccionado)
        else:
            messagebox.showinfo("Advertencia", "Este departamento ya ha sido añadido.")

    def crear_interfaz(self):
        # Botones para las opciones
        boton_ver_datos = tk.Button(self, text="Ver datos sobre un departamento", command=self.ver_datos)
        boton_ver_datos.pack()

        # Botón para añadir departamentos
        boton_agregar_departamento = tk.Button(self, text="Añadir departamento", command=self.agregar_departamento)
        boton_agregar_departamento.pack()

        # Botón para comparar datos entre departamentos
        boton_comparar_datos = tk.Button(self, text="Comparar datos entre departamentos", command=self.comparar_datos)
        boton_comparar_datos.pack()

        # Dropdown para seleccionar el departamento
        label_departamento = tk.Label(self, text="Selecciona un departamento:")
        label_departamento.pack()

        dropdown_departamento = tk.OptionMenu(self, self.departamento_seleccionado, *list(datos['DEPARTAMENTO'].unique()))
        dropdown_departamento.pack()

        # Botón para volver a ver otro reporte
        boton_volver = tk.Button(self, text="Volver a ver otro reporte", command=self.volver_a_reportes)
        boton_volver.pack()

    def volver_a_reportes(self):
        # Cerrar la ventana actual
        self.destroy()

        # Crear la instancia de la página de reportes
        pagina_reportes = PaginaReportes(master=self.master)
        pagina_reportes.pack()



# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Reportes")

# Configurar el tamaño de la ventana principal
root.geometry("800x600")

# Crear la instancia de la página de inicio
pagina_inicio = PaginaInicio(master=root)

# Iniciar el bucle de eventos
pagina_inicio.mainloop()
