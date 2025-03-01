import tkinter as tk  # Importamos tkinter para la interfaz gráfica
from PIL import Image, ImageTk
from claseBBDD import BBDD
from claseGrafica import Grafica
from clasePdf import Pdf

class interfaz(tk.Tk):  # Creamos una clase que hereda de Tk (ventana principal)
    def __init__(self):
        super().__init__()  # Inicializa la ventana principal

        self.title("Examen Segundo DAM - FECHA")  # Título de la ventana
        self.geometry("800x500")  # Tamaño
        self.resizable(False, False)  # No redimensionable
        self.config(bg="white")  # Color de la ventana

        # Frame Arriba
        self.frame_superior = tk.Frame(self, height=50, bg="#74B0CF")
        self.frame_superior.pack(fill="x")

        self.label_nombre = tk.Label(self.frame_superior, text="Nombre del alumno",
                                     font=("Arial", 12, "bold"), bg="#74B0CF", fg="black")
        self.label_nombre.pack(side="left", padx=20, pady=10)

        # Frame inferior con botón
        self.frame_inferior = tk.Frame(self, height=50, bg="#A7D0E4")
        self.frame_inferior.pack(side="bottom", fill="x")

        self.btn_acerca = tk.Button(self.frame_inferior, width=220, text="Acerca de..", command=self.mostrar_acerca)
        self.btn_acerca.pack(side="right", padx=20, pady=10)

        # Frame izquierdo, logo + botones
        self.frame_izquierdo = tk.Frame(self, width=220, bg="#A7D0E4")
        self.frame_izquierdo.pack(side="left", fill="y", padx=20, pady=20)

        # Cargar imagen
        self.logo_img = Image.open("logo.png")  # Ruta imagen
        self.logo_img = self.logo_img.resize((120, 50))  # Ajustamos tamaño
        self.logo_img = ImageTk.PhotoImage(self.logo_img)

        self.logo_label = tk.Label(self.frame_izquierdo, image=self.logo_img, bg="#A7D0E4")
        self.logo_label.pack(pady=5)

        # Botones frame izquierdo
        self.btn_connectar = tk.Button(self.frame_izquierdo, text="Conexion BD", command=self.conectar_bbdd,
                                       bg="#D9EAF1", width=20)
        self.btn_connectar.pack(pady=10)

        self.btn_grafica = tk.Button(self.frame_izquierdo, text="Generar Gráfica", command=self.generar_grafica,
                                     bg="#D9EAF1", width=20)
        self.btn_grafica.pack(pady=10)

        self.btn_pdf = tk.Button(self.frame_izquierdo, text="Generar pdf", command=self.generar_pdf,
                                 bg="#D9EAF1", width=20)
        self.btn_pdf.pack(pady=10)

        # Frame derecho mostrará lo que generemos
        self.frame_derecho = tk.Frame(self, bg="white", width=500, height=400)
        self.frame_derecho.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.label_mensaje = tk.Label(self.frame_derecho, text="Resultados",
                                      font=("Arial", 12), bg="white")
        self.label_mensaje.pack(pady=20)

    def mostrar_acerca(self):
        ventana_acerca = tk.Toplevel(self)
        ventana_acerca.title("Acerca de..")
        ventana_acerca.geometry("300x150")
        ventana_acerca.resizable(False, False)

        tk.Label(ventana_acerca, text="Nombre del alumno", font=("Arial", 12)).pack(pady=5)
        tk.Label(ventana_acerca, text="Desarrollo de Aplicaciones Multiplataforma", font=("Arial", 12)).pack(pady=5)
        tk.Label(ventana_acerca, text="2025", font=("Arial", 12)).pack(pady=5)

    def conectar_bbdd(self):
        #Conecta con la base de datos si hay suerte
        try:
            db = BBDD(user = "root",password="root",host="127.0.0.1",database="temperaturas")

            #intendamos crear table y base de datos por si no existe
            db.createDB()
            db.createTable()

            if hasattr(self, 'label_mensaje') and self.label_mensaje.winfo_exists():
                self.label_mensaje.config(text=" Todo fue bien con la BBDD", fg="green")
            else:
                print("⚠ ERROR: `label_mensaje` no existe en la interfaz.")

        except Exception as e:
            if hasattr(self, 'label_mensaje') and self.label_mensaje.winfo_exists():
                self.label_mensaje.config(text=f"Algo falló en la BBDD: {e}", fg="red")
            else:
                print(f"⚠ ERROR al modificar `label_mensaje`: {e}")

            #Si tenemos suerte mensaje a la interfaz 

            self.label_mensaje.config(text="Todo fue bien con la BBDD" , fg="green")
        except Exception as e:
            #Si no hay suerte

            self.label_mensaje.config(text=f"Algo fallo en bbdd {e}", bg="red")


    def generar_grafica(self):
        #LLama a la clase grafica para generar la gráfica,redundante
        grafica = Grafica(self.frame_derecho) #creamos la instancia de la clase grafica
        mensaje,color = grafica.mostrarGrafica() #la generamos
        self.label_mensaje.config(text=mensaje, fg=color) 


    def generar_pdf(self):
        #Llama a la clase Pdf para generar el PDF
        # Conectar a la base de datos y obtener los datos
        db = BBDD(user="root", password="root", host="127.0.0.1", database="temperaturas")
        conn = db.conectar()
        if conn is None:
            self.label_mensaje.config(text=" Error al conectar a la base de datos", fg="red")
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT comunidad, max_temp, min_temp FROM temperaturas")
        temperaturas = cursor.fetchall()
        conn.close()

        # Datos que se pasarán a la plantilla
        info = {"temperaturas": temperaturas}

        # Creamos una instancia de Pdf
        pdf = Pdf(
            content_route="Plantilla.html",
            css="styles.css",
            info=info,
            output_route="."
        )

        # Generamos el PDF
        mensaje, color = pdf.createPdf()
        self.label_mensaje.config(text=mensaje, fg=color)
