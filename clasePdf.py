import pdfkit  # Librería para html a pdf
import jinja2  # Librería para plantillas pdf
import os  # Manejar rutas

class Pdf:
    def __init__(self, content_route: str, css: str, info: dict, output_route: str):
        # Ruta plantilla html
        self.content_route = content_route
        
        # Ruta css para dar estilo al pdf
        self.css = css

        # Datos a insertar
        self.info = info

        # Ruta de guardado del pdf
        self.output_route = output_route

    def createPdf(self):
        # Genera un pdf a partir de una plantilla
        try:
            # Extraemos el nombre del archivo de la ruta
            nombre_template = os.path.basename(self.content_route)
            
            # Configuramos jinja2
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(self.content_route)))
            template = env.get_template(nombre_template)
            html = template.render(self.info)
            
            # Configuramos pdfkit
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

            # Definimos opciones
            options = {
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None
            }

            # Generamos el PDF
            pdfkit.from_string(html, self.output_route, options=options, configuration=config, css=self.css)

            print(f"PDF generado correctamente en {self.output_route}")
            return "PDF generado correctamente", "green"

        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            return f"Error al generar el PDF: {e}", "red"
