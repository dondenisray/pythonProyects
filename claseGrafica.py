import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from claseBBDD import BBDD  # Importamos la clase para obtener datos de MySQL

class Grafica:
    def __init__(self, frame_derecho, nombre_grafica="grafica_temperaturas"):
        #Inicializa la gráfica con su nombre y el frame donde se mostrará
        self.frame_derecho = frame_derecho
        self.nombre_grafica = nombre_grafica
        self.labelx = "Comunidades Autónomas"
        self.labely = "Temperatura en grados"
        self.datosx = []  # Comunidades
        self.datosy_max = []  # Temperaturas máximas
        self.datosy_min = []  # Temperaturas mínimas
        self.titulo = "Temperaturas máximas y mínimas"

    def obtenerDatos(self):
        #Obtiene los datos de temperaturas desde la base de datos
        try:
            db = BBDD(user="root", password="root", host="127.0.0.1", database="temperaturas")

            # Consulta para obtener los datos
            query = "SELECT comunidad, max_temp, min_temp FROM temperaturas"
            conn = db.conectar()  # Conectar manualmente
            cursor = conn.cursor()
            cursor.execute(query)
            datos = cursor.fetchall()
            conn.close()

            if not datos:
                return False, " No hay datos en la base de datos", "red"

            # Extraer los datos en listas separadas
            self.datosx = [row[0] for row in datos]
            self.datosy_max = [row[1] for row in datos]
            self.datosy_min = [row[2] for row in datos]

            return True, " Datos obtenidos correctamente", "green"

        except Exception as e:
            return False, f" Error al obtener datos: {e}", "red"

    def prepararGrafica(self):
        #Prepara la gráfica con los datos obtenidos
        plt.figure(figsize=(6, 4))
        plt.bar(self.datosx, self.datosy_max, label="Temperatura Máxima", color="red")
        plt.bar(self.datosx, self.datosy_min, label="Temperatura Mínima", color="blue")

        plt.title(self.titulo)
        plt.xlabel(self.labelx)
        plt.ylabel(self.labely)
        plt.legend()

    def mostrarGrafica(self):
        #Muestra la gráfica dentro del frame de Tkinter
        estado, mensaje, color = self.obtenerDatos()
        if not estado:
            return mensaje, color  # Si hubo error, lo devolvemos

        self.prepararGrafica()  # Genera la gráfica correctamente

        # Limpiar antes de agregar nueva gráfica
        for widget in self.frame_derecho.winfo_children():
            widget.destroy()

        fig = plt.gcf()  # Obtener la figura actual
        canvas = FigureCanvasTkAgg(fig, master=self.frame_derecho)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return " Gráfica generada correctamente", "green"

    def guardarGrafica(self):
        """Guarda la gráfica como PNG"""
        estado, mensaje, color = self.obtenerDatos()
        if not estado:
            return mensaje, color  # Si hubo error, lo devolvemos

        self.prepararGrafica()
        plt.savefig(self.nombre_grafica + ".png")  # Guardar la imagen
        return f" Gráfica guardada como {self.nombre_grafica}.png", "green"
