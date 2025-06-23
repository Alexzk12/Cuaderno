###################################################################################################################################################################
# 1.- ---------------- Encabezado --------------------------------------------------------------------------------------------------------------------------------------
#     Proyecto       : 7.1 Proyecto Final y Aplicacion/Repositorio de evidencia
#     Lenguaje       : Python
#     Herramienta    : https://code.visualstudio.com
#     Compilador     : Visual Studio Code
#     Version        : 3.12.6
#     Fecha/Hora     : 23-06-2025, 03:51 pm
#     Programa en lenguaje Interpretado (Python)
#     by: algunos programas son en base a los del profesor Jorge Anzaldo y modificado por Guzman Morelos Jesus Alejandro
#     Profesor: Jorge Anzaldo
########################################################################################################################################################################
# 2.- ---------------- Importación de Módulos y Bibliotecas Comentarios-------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import serial
import serial.tools.list_ports
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from graphviz import Digraph
from PIL import Image, ImageTk
# 3.- ---------------- Definición de Funciones o clases ----------------------------------------------------------------------------------------------------------------
# Primer Parcial
class Pila:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Pila")
        self.ventana.geometry("400x300+100+100")

        self.pila = []

        tk.Label(self.ventana, text="Prepara tu Hamburguesa").pack()
        tk.Label(self.ventana, text="Ingresa los ingredientes empezando desde abajo de tu hamburguesa").pack()

        self.entry = tk.Entry(self.ventana)
        self.entry.pack()

        tk.Button(self.ventana, text="Agregar ingrediente", command=self.meterDatos).pack()
        tk.Button(self.ventana, text="Quitar el último ingrediente", command=self.sacarDatos).pack()
        tk.Button(self.ventana, text="Ver hamburguesa", command=self.mostrar).pack()

        self.label = tk.Label(self.ventana, text="Ingredientes: []")
        self.label.pack()

    def meterDatos(self):
        self.pila.append(self.entry.get())
        

    def sacarDatos(self):
        if self.pila:
            self.pila.pop()
            

    def mostrar(self):
        self.label.config(text=f"Hamburguesa: {self.pila}")

class Cola:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Cola")
        self.ventana.geometry("400x300+300+300")

        self.cola = []

        tk.Label(self.ventana, text="Cremeria Insurgentes").pack()

        self.entry = tk.Entry(self.ventana)
        self.entry.pack()

        tk.Button(self.ventana, text="Agregar persona", command=self.meterNumeros).pack()
        tk.Button(self.ventana, text="Atender a la primera persona", command=self.sacarNumeros).pack()
        tk.Button(self.ventana, text="Enseñar fila de personas para atender", command=self.mostrar).pack()

        self.label = tk.Label(self.ventana, text="Personas por atender: []")
        self.label.pack()

    def meterNumeros(self):
        self.cola.append(self.entry.get())
        

    def sacarNumeros(self):
        if self.cola:
            self.atendido = self.cola.pop(0)
            

    def mostrar(self):
        self.label.config(text=f"Fila actual: {self.cola}")

#Segundo Parcial

class Grafo:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Grafo: Ruta de Calles")
        self.ventana.geometry("500x600") 
        try:
            self.df = pd.read_csv(r'C:\Users\Alex\Desktop\Evidencias\src\calles.csv')
        except FileNotFoundError:
            return

        self.g = nx.DiGraph()
        for _, row in self.df.iterrows():
            distancia = row['distancia']
            peligrosidad = row['peligrosidad']
            peso_combinado = (distancia + peligrosidad) / 2  
            self.g.add_edge(row['origen'], row['destino'], weight=peso_combinado,
                            distancia=distancia, peligrosidad=peligrosidad)

        self.pos = {
            'PedroMoreno_EsqTorres': (0, 3), 'PedroMoreno_EsqFlores': (1, 3), 'PedroMoreno_Esq1Mayo': (2, 3), 'PedroMoreno_EsqMendoza': (3, 3),
            'DiazMiron_EsqTorres': (0, 2), 'DiazMiron_EsqFlores': (1, 2), 'DiazMiron_Esq1Mayo': (2, 2), 'DiazMiron_EsqMendoza': (3, 2),
            'MiguelHidalgo_EsqTorres': (0, 1), 'MiguelHidalgo_EsqFlores': (1, 1), 'MiguelHidalgo_Esq1Mayo': (2, 1), 'MiguelHidalgo_EsqMendoza': (3, 1),
        }

        tk.Label(self.ventana, text="Intersecciones disponibles:").pack()
        self.intersecciones_text = tk.Text(self.ventana, height=10, width=50, wrap="word")
        self.intersecciones_text.pack(pady=5)
        intersecciones_str = ""
        for nodo in self.g.nodes:
            intersecciones_str += f"- {nodo}\n"
        self.intersecciones_text.insert(tk.END, intersecciones_str)
        self.intersecciones_text.config(state=tk.DISABLED)

        tk.Label(self.ventana, text="Origen:").pack()
        self.entry_origen = tk.Entry(self.ventana)
        self.entry_origen.pack()

        tk.Label(self.ventana, text="Destino:").pack()
        self.entry_destino = tk.Entry(self.ventana)
        self.entry_destino.pack()

        tk.Button(self.ventana, text="Calcular Ruta", command=self.calcular_ruta).pack(pady=10)
        tk.Button(self.ventana, text="Ver Grafo Visual", command=self.visualizar_grafo).pack(pady=5)
        
        self.label_ruta = tk.Label(self.ventana, text="")
        self.label_ruta.pack(pady=5)

    def visualizar_grafo(self):
        plt.figure(figsize=(10, 7))
        nx.draw(self.g, self.pos, with_labels=True, font_color='black', node_color='lightblue',
                node_size=2500, font_size=6, font_weight='bold', arrows=False)
        edge_labels = { (u,v): f"{d['distancia']}m, P:{d['peligrosidad']}" for u,v,d in self.g.edges(data=True) }
        nx.draw_networkx_edge_labels(self.g, self.pos, edge_labels=edge_labels)
        plt.title("Intersecciones con distancia y peligrosidad")
        plt.show(block=False)

    def calcular_ruta(self):
        origen_usuario = self.entry_origen.get()
        destino_usuario = self.entry_destino.get()
        try:
            camino_encontrado = nx.dijkstra_path(self.g, origen_usuario, destino_usuario, weight='weight')
            
            ruta_str = "Ruta encontrada:\n"
            total_distancia = 0
            total_peligrosidad = 0
            total_peso = 0

            for i in range(len(camino_encontrado) - 1):
                nodo1 = camino_encontrado[i]
                nodo2 = camino_encontrado[i + 1]
                datos_arista = self.g[nodo1][nodo2]
                distancia = datos_arista['distancia']
                peligrosidad = datos_arista['peligrosidad']
                peso = datos_arista['weight']
                ruta_str += f"{nodo1} -> {nodo2}: Distancia={distancia}m, Peligrosidad={peligrosidad}, Peso combinado={peso:.2f}\n"
                total_distancia += distancia
                total_peligrosidad += peligrosidad
                total_peso += peso

            ruta_str += f"\nDistancia total: {total_distancia} metros\n"
            ruta_str += f"Peligrosidad total: {total_peligrosidad}\n"
            ruta_str += f"Peso combinado total: {total_peso:.2f}"
            self.label_ruta.config(text=ruta_str)

        except nx.NetworkXNoPath:
            self.label_ruta.config(text="No se encontró una ruta entre esos puntos.")


class NodoEstudiante:
    def __init__(self, boleta, nombre, parcial1, parcial2, parcial3):
        self.boleta = boleta
        self.nombre = nombre
        self.parcial1 = float(parcial1)
        self.parcial2 = float(parcial2)
        self.parcial3 = float(parcial3)
        self.prom = (self.parcial1 + self.parcial2 + self.parcial3) / 3
        self.izq = None
        self.der = None

    def __str__(self):
        return f"{self.boleta} - {self.nombre} - Prom: {self.prom:.2f}"

class ArbolEstudiante:
    def __init__(self):
        self.raiz = None

    def insertar(self, boleta, nombre, parcial1, parcial2, parcial3):
        if self.raiz is None:
            self.raiz = NodoEstudiante(boleta, nombre, parcial1, parcial2, parcial3)
        else:
            self._insertar_recursivo(self.raiz, boleta, nombre, parcial1, parcial2, parcial3)

    def _insertar_recursivo(self, nodo, boleta, nombre, parcial1, parcial2, parcial3):
        if boleta < nodo.boleta:
            if nodo.izq is None:
                nodo.izq = NodoEstudiante(boleta, nombre, parcial1, parcial2, parcial3)
            else:
                self._insertar_recursivo(nodo.izq, boleta, nombre, parcial1, parcial2, parcial3)
        elif boleta > nodo.boleta:
            if nodo.der is None:
                nodo.der = NodoEstudiante(boleta, nombre, parcial1, parcial2, parcial3)
            else:
                self._insertar_recursivo(nodo.der, boleta, nombre, parcial1, parcial2, parcial3)

    def buscar(self, boleta):
        return self._buscar_recursivo(self.raiz, boleta)

    def _buscar_recursivo(self, nodo, boleta):
        if nodo is None:
            return None
        if boleta == nodo.boleta:
            return nodo
        elif boleta < nodo.boleta:
            return self._buscar_recursivo(nodo.izq, boleta)
        else:
            return self._buscar_recursivo(nodo.der, boleta)

    def eliminar(self, boleta):
        self.raiz = self._eliminar_recursivo(self.raiz, boleta)

    def _eliminar_recursivo(self, nodo, boleta):
        if nodo is None:
            return None
        if boleta < nodo.boleta:
            nodo.izq = self._eliminar_recursivo(nodo.izq, boleta)
        elif boleta > nodo.boleta:
            nodo.der = self._eliminar_recursivo(nodo.der, boleta)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq
            min_nodo = self._minimo(nodo.der)
            nodo.boleta = min_nodo.boleta
            nodo.nombre = min_nodo.nombre
            nodo.parcial1 = min_nodo.parcial1
            nodo.parcial2 = min_nodo.parcial2
            nodo.parcial3 = min_nodo.parcial3
            nodo.prom = min_nodo.prom
            nodo.der = self._eliminar_recursivo(nodo.der, min_nodo.boleta)
        return nodo

    def _minimo(self, nodo):
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    def inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return " | ".join(resultado)

    def _inorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorden_recursivo(nodo.izq, resultado)
            resultado.append(str(nodo))
            self._inorden_recursivo(nodo.der, resultado)

    def preorden(self):
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return " | ".join(resultado)

    def _preorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(str(nodo))
            self._preorden_recursivo(nodo.izq, resultado)
            self._preorden_recursivo(nodo.der, resultado)

    def postorden(self):
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return " | ".join(resultado)

    def _postorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorden_recursivo(nodo.izq, resultado)
            self._postorden_recursivo(nodo.der, resultado)
            resultado.append(str(nodo))

    def profundidad(self):
        return self._profundidad(self.raiz)

    def _profundidad(self, nodo):
        if nodo is None:
            return 0
        izquierda = self._profundidad(nodo.izq)
        derecha = self._profundidad(nodo.der)
        return 1 + max(izquierda, derecha)

    def visualizar(self):
        dot = Digraph()
        dot.attr("node", shape="box3d")
        if self.raiz is not None:
            self._visualizar_recursivo(self.raiz, dot)
        return dot

    def _visualizar_recursivo(self, nodo, dot):
        etiqueta = f"{nodo.boleta}\n{nodo.nombre}\nProm: {nodo.prom:.2f}"
        dot.node(nodo.boleta, etiqueta)
        if nodo.izq is not None:
            dot.edge(nodo.boleta, nodo.izq.boleta)
            self._visualizar_recursivo(nodo.izq, dot)
        if nodo.der is not None:
            dot.edge(nodo.boleta, nodo.der.boleta)
            self._visualizar_recursivo(nodo.der, dot)

class Arbol:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Esime")
        self.ventana.geometry("500x700")
        self.arbol = ArbolEstudiante()
        tk.Label(self.ventana, text="boleta:").pack()
        self.entryBoleta = tk.Entry(self.ventana)
        self.entryBoleta.pack()
        tk.Label(self.ventana, text="nombre:").pack()
        self.entryNombre = tk.Entry(self.ventana)
        self.entryNombre.pack()
        tk.Label(self.ventana, text="parcial 1:").pack()
        self.entryP1 = tk.Entry(self.ventana)
        self.entryP1.pack()
        tk.Label(self.ventana, text="parcial 2:").pack()
        self.entryP2 = tk.Entry(self.ventana)
        self.entryP2.pack()
        tk.Label(self.ventana, text="parcial 3:").pack()
        self.entryP3 = tk.Entry(self.ventana)
        self.entryP3.pack()

        self.labelImagen = tk.Label(self.ventana)
        self.labelImagen.pack(pady=10)

        self.labelInorden = tk.Label(self.ventana, text="Inorden: ")
        self.labelInorden.pack()
        self.labelPreorden = tk.Label(self.ventana, text="Preorden: ")
        self.labelPreorden.pack()
        self.labelPostorden = tk.Label(self.ventana, text="Postorden: ")
        self.labelPostorden.pack()

        self.labelProfundidad = tk.Label(self.ventana, text="Profundidad: ...")
        self.labelProfundidad.pack(pady=5)

        self.labelBusqueda = tk.Label(self.ventana, text="")
        self.labelBusqueda.pack()

        tk.Button(self.ventana, text="Agregar Alumno", command=self.agregar).pack(pady=5)
        tk.Button(self.ventana, text="Buscar Alumno", command=self.buscar).pack(pady=5)
        tk.Button(self.ventana, text="Eliminar Alumno", command=self.eliminar).pack(pady=5)
        tk.Button(self.ventana, text="Ver arbol", command=self.visualizar).pack(pady=5)
        tk.Button(self.ventana, text="Ver Recorridos", command=self.verRecorridos).pack(pady=5)
        tk.Button(self.ventana, text="Ver Profundidad", command=self.verProfundidad).pack(pady=5)

    def agregar(self):
        boleta = self.entryBoleta.get()
        nombre = self.entryNombre.get()
        p1 = self.entryP1.get()
        p2 = self.entryP2.get()
        p3 = self.entryP3.get()
        self.arbol.insertar(boleta, nombre, p1, p2, p3)
        
    def buscar(self):
        boleta = self.entryBoleta.get()
        nodo = self.arbol.buscar(boleta)
        if nodo is None:
            self.labelBusqueda.config(text=f"El alumno con boleta {boleta} no se encontro")
        else:
            self.labelBusqueda.config(text=f"Encontrado: {nodo}")

    def eliminar(self):
        boleta = self.entryBoleta.get()
        self.arbol.eliminar(boleta)
        self.labelBusqueda.config(text=f"El alumno con la boleta {boleta} se ha eliminado.")

    def visualizar(self):
        dot = self.arbol.visualizar()
        dot.render("arbol", format="png", cleanup=True)
        imagen = Image.open("arbol.png")
        imagen = imagen.resize((400, 300))
        self.imagenTk = ImageTk.PhotoImage(imagen) 
        self.labelImagen.config(image=self.imagenTk)
        self.labelImagen.image = self.imagenTk

    def verRecorridos(self):
        self.labelInorden.config(text="Inorden: " + self.arbol.inorden())
        self.labelPreorden.config(text="Preorden: " + self.arbol.preorden())
        self.labelPostorden.config(text="Postorden: " + self.arbol.postorden())

    def verProfundidad(self):
        prof = self.arbol.profundidad()
        self.labelProfundidad.config(text=f"Profundidad: {prof}")

# Tercer Parcial concurrencia 
#Para poder hacer uso de este apartado se necesita tener el ESP32 CONECTADO A LA COMPUTADORA, EN EL PUERO COM3, AL IGUAL QUE TAMBIEN QUE TENGAS INSTALADAS LAS LIBRERIAS CORRESPONTIENDTES
class CINELEX:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("CINELEX")
        self.ventana.geometry("500x400")
        self.ventana.resizable(True, True)
        self.ventana.configure(background='#7c1324')
        self.personas_restantes = 15
        self.cajas_disponibles = [True, True, True, True]

        self.label_estado = tk.Label(self.ventana, text="PERSONAS POR ATENDER: 15", font=("Arial", 14))
        self.label_estado.pack(pady=10)

        self.barra = ttk.Progressbar(self.ventana, length=300, maximum=15)
        self.barra.pack(pady=10)

        self.boton_inicio = tk.Button(self.ventana, text="Empezar a atender", command=self.iniciar_simulacion)
        self.boton_inicio.pack(pady=10)

        self.texto_log = tk.Text(self.ventana, height=10, width=60)
        self.texto_log.pack(pady=10)
        self.texto_log.insert(tk.END, "Esperando inicio...\n")
        self.texto_log.config(state=tk.DISABLED)
        self.serial_port = self.conectar_esp32()

    def conectar_esp32(self):
        puertos = serial.tools.list_ports.comports()
        for puerto in puertos:
            try:
                s = serial.Serial(puerto.device, 115200, timeout=1) 
                return s
            except:
                continue
        print("No se encontro ESP32")
        return None

    def iniciar_simulacion(self):
        self.boton_inicio.config(state="disabled")
        threading.Thread(target=self.simular_fila, daemon=True).start()

    def simular_fila(self):
        while self.personas_restantes > 0:
            for i in range(4):
                if self.cajas_disponibles[i] and self.personas_restantes > 0:
                    self.cajas_disponibles[i] = False
                    threading.Thread(target=self.atender_persona, args=(i,), daemon=True).start()
                    self.personas_restantes -= 1
                    self.actualizar_interfaz()
            time.sleep(0.2)
    def atender_persona(self, caja_id):
        tiempo = random.randint(5, 10)
        self.log(f"Caja {caja_id} atendiendo por {tiempo} segundos...")
        self.serial_port.write(f"{caja_id}:1\n".encode())
        time.sleep(tiempo)
        self.serial_port.write(f"{caja_id}:0\n".encode())
        self.log(f"Caja {caja_id} libre (persona atendida en {tiempo} segundos).")
        self.cajas_disponibles[caja_id] = True
        self.barra["value"] += 1
        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        self.label_estado.config(text=f"Personas por atender: {self.personas_restantes}")
        self.ventana.update_idletasks()

    def log(self, mensaje):
        self.texto_log.config(state=tk.NORMAL)
        self.texto_log.insert(tk.END, mensaje + "\n")
        self.texto_log.see(tk.END)
        self.texto_log.config(state=tk.DISABLED)

#Menu general
class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Cuaderno Programacion Avanzada")
        master.geometry("900x400")
        self.barraMenus = tk.Menu(master)
        master.config(menu=self.barraMenus)
     # Primer Parcial 
        menu_primer_parcial = tk.Menu(self.barraMenus, tearoff=0)
        menu_primer_parcial.add_command(label="Cola", command=lambda: Cola(self.master))
        menu_primer_parcial.add_command(label="Pila", command=lambda: Pila(self.master))
        self.barraMenus.add_cascade(label="Primer Parcial", menu=menu_primer_parcial)
     # Segundo Parcial 
        menu_segundo_parcial = tk.Menu(self.barraMenus, tearoff=0)
        menu_segundo_parcial.add_command(label="Grafo", command=lambda: Grafo(self.master))
        menu_segundo_parcial.add_command(label="arbol", command=lambda: Arbol(self.master))
        self.barraMenus.add_cascade(label="Segundo Parcial", menu=menu_segundo_parcial)
     # Tercer Parcial 
        menu_tercer_parcial = tk.Menu(self.barraMenus, tearoff=0)
        menu_tercer_parcial.add_command(label="Concurrencia", command=lambda: CINELEX(self.master))
        self.barraMenus.add_cascade(label="Tercer Parcial", menu=menu_tercer_parcial)

        tk.Label(master, text="Bienvenido a mi cuaderno, en el menu de arriba podras ver mis practicas/proyectos", font=("Arial", 16)).pack(pady=50)

if __name__ == "__main__":
    
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
# 6.- ---------------- Documentación y Comentarios----------------------------------------------------------------------------------------------------------------------
#En este programa se hace uso de todo lo aprendido en el curso de Programacion Avanzada impartido por el profesor Jorge Anzaldo, se hace uso de interfaces graficas como 
#tkinter y de todos los temas vistos en el semestre, tambien incluye cosas extra como el ESP32

# Documentación oficial de Python (https://docs.python.org/3/tutorial/datastructures.html)
# Realizado con Material del Clasroom del profesor Jorge Anzaldo y con el concepto de arbol binario
# compilador: https://code.visualstudio.com