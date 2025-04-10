from fpdf import FPDF
from datetime import datetime

class FacturaPDF:
    def __init__(self,cliente, carrito, total, factura_id,filename="factura.pdf"):
        self.cliente = cliente
        self.productos = carrito
        self.total = total
        self.factura_id = factura_id
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.filename = filename
        self.pdf = FPDF() #Creamos un objeto FPDF que es el documento donde escribiremos, pero no tiene hoja aún

    def generar(self):
        self.pdf.add_page() #Añadimos una hoja para escribir sobre ella
        self.pdf.set_font("Arial",style="B", size=16)

        #Titulo
        self.pdf.cell(0,10,txt="FACTURA",ln=True,align="C")

        #Info de la factura
        self.pdf.set_font("Arial",size=12)
        self.pdf.ln(10)
        self.pdf.cell(100,10, txt=f"Factura ID: {self.factura_id}")
        self.pdf.cell(0,10,txt=f"Fecha:{self.fecha}", ln=True)

        self.pdf.cell(100,10,txt=f"Cliente: {self.cliente}", ln=True)
        self.pdf.ln(10)

        #Encabezado de la tabla
        self.pdf.set_font("Arial", style="B",size=12)
        self.pdf.cell(80,10,"Producto", border=1)
        self.pdf.cell(30, 10, "Cantidad", border=1)
        self.pdf.cell(40, 10, "Precio Unitario", border=1)
        self.pdf.cell(40, 10, "Subtotal", border=1,ln=True)

        #Filas de productos
        self.pdf.set_font("Arial", size=12)
        for producto in self.carrito:
            for nombre, cantidad in producto.items():
                nombre=nombre.nombre
                cantidad=cantidad
                precio=nombre.precio
                subtotal= cantidad*precio

                self.pdf.cell(80, 10,nombre, border=1)
                self.pdf.cell(30, 10, str(cantidad), border=1)
                self.pdf.cell(40, 10, txt=f"${precio:.2f}", border=1)
                self.pdf.cell(40, 10, txt=f"${subtotal:.2f}", border=1,ln=True)

        #Total
        self.pdf.ln(5)
        self.pdf.set_font("Arial", style="B",size=12)
        self.pdf.cell(150,10,txt="TOTAL:",align="R")
        self.pdf.cell(40, 10, txt=f"{self.total:.2f}", border=1, ln=True)

        #Pie de página
        self.pdf.ln(15)
        self.pdf.set_font("Arial", style="I",size=10)
        self.pdf.cell(0,10,"Gracias por la compra. Para cualquier duda, contacte con soporte@alu.ua.es",ln=True,align="C")

        #Guardar
        self.pdf.output(self.filename)

