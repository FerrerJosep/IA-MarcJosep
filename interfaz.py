import flet as ft
from customWidgets import CustomTextField, CustomButton, CustomSpacerRow

def main(page: ft.Page):
    page.title = "Interfaz de prueba"
    
    # Crear los campos de texto
    memoria_field = CustomTextField(label="Memória", hint_text="Introduce el valor en GB", icon=ft.icons.MEMORY)
    ram_field = CustomTextField(label="RAM", hint_text="Introduce el valor en GB")
    precio_field = CustomTextField(label="Precio", hint_text="Introduce el valor en €", icon=ft.icons.EURO)

    # Crear el campo para mostrar el resultado de la predicción
    resultado_text = ft.Text(value="", size=16, color=ft.colors.GREEN_700)  # Este es el texto que se actualizará
    
    # Función para obtener los datos y realizar la predicción
    def obtenerDatos(e):
        print("hola")

        # Obtener los valores de los campos
        memoria = memoria_field.value
        ram = ram_field.value
        precio = precio_field.value

        if memoria.isnumeric() and ram.isnumeric() and precio.isnumeric():
        
        # Realizar la predicción
            resultado = realizarPrediccion(memoria, ram, precio)
        else:
            resultado_text.value="Error: Solo se permiten valores numéricos"
            page.update()
            return 
        # Cambiar el texto y el color del resultado
        if resultado == 0:
            resultado_text.value = "Mala oferta"
            resultado_text.color = ft.colors.RED_700  # Cambiar color a rojo
        else:
            resultado_text.value = "Buena oferta"
            resultado_text.color = ft.colors.GREEN_700
        # Actualizar el texto con el resultado de la predicción
        resultado_text.value = f"Resultado de la predicción: {resultado}"
        page.update()  # Actualizar la página para reflejar el nuevo valor del texto

    def realizarPrediccion(memoria, ram, precio):
        
        # return model.predict(memoria, ram, precio)  
        return 0

    boton_obtener = CustomButton(accion=obtenerDatos, texto="Comprueba")

    # Hacer que cada campo de texto se expanda en el Row y se ajuste a la pantalla
    # Esto hará que cada TextField ocupe el mismo espacio dentro del Row
    page.add(
        # Añadimos un row vacio para crear un margen.
        CustomSpacerRow(),
        ft.Row(
            [
                ft.Column([memoria_field], expand=True),
                ft.Column([ram_field], expand=True),
                ft.Column([precio_field], expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alineación central
            spacing=20,  # Espaciado entre los campos
        ),
        CustomSpacerRow(),
        ft.Row([boton_obtener], alignment=ft.MainAxisAlignment.CENTER),
        CustomSpacerRow(),
        ft.Row([resultado_text], alignment=ft.MainAxisAlignment.CENTER),
    )


if __name__ == "__main__":
    ft.app(target=main)
