from fpdf import FPDF


class FacturaPDF:
    def __init__(self,cliente, productos, total, filename="factura.pdf"):
        self.cliente = cliente
        self.productos = productos
        self.total = total
        self.filename = filename
        self.pdf = FPDF() #Creamos un objeto FPDF que es el documento donde escribiremos, pero no tiene hoja aún

    def generar(self):
        self.pdf.add_page() #Añadimos una hoja para escribir sobre ella
        self.pdf.set_font("Arial", size=12) #Definimos la letra y el tamaño

        self.pdf.cell(200,10, txt=f"Factura para {self.cliente}", ln=True)
        self.pdf.cell(200,10,txt=f"Productos:", ln=True)

        for producto in self.productos:
            self.pdf.cell(200, 10, txt=f"- {producto['nombre']}: ${producto['precio']}", ln=True)

        self.pdf.cell(200,10,txt=f"Total: ${self.total}",ln=True)

        self.pdf.output(self.filename)

