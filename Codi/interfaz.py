import time
import flet as ft
import json
import requests
from customWidgets import CustomTextField, CustomButton, CustomSpacerRow, CustomAlertDialog

def main(page: ft.Page):
    page.title = "Interfaz de prueba"
    
    page.theme_mode = ft.ThemeMode.LIGHT  # Set initial theme mode

    

    def alternar_tema(e):
        print("Alternando tema")
        if page.theme_mode == ft.ThemeMode.DARK:
            
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    # Campos de entrada
    estrellas_field = CustomTextField(label="Estrellas", hint_text="Introduce la valoración", valor_defecto="4.5")
    marca_field = CustomTextField(label="Marca", hint_text="Introduce la marca", valor_defecto="Samsung")
    dimensiones_field = CustomTextField(label="Dimensiones", hint_text="Formato: Ancho x Alto x Profundidad", valor_defecto="10 x 20 x 5")
    peso_field = CustomTextField(label="Peso", hint_text="Introduce el peso en kg",    valor_defecto="0.5")
    memoria_field = CustomTextField(label="Memoria", hint_text="Introduce el valor en GB", icon=ft.icons.MEMORY, valor_defecto="64")
    ram_field = CustomTextField(label="RAM", hint_text="Introduce el valor en GB", valor_defecto="4")
    precio_field = CustomTextField(label="Precio", hint_text="Introduce el valor en €", icon=ft.icons.EURO, valor_defecto="200")

    resultado_text = ft.Text(value="", size=16, color=ft.colors.GREEN_700)
    boton_tema = CustomButton(accion=alternar_tema, texto="Alternar Tema")

        
    def mostrar_dialogo_cargando():
        dlg = CustomAlertDialog(
            title=ft.Text("Cargando"),
            content=ft.Text("Por favor, espere..."),
            open=True,
            actions=[]
        )
        page.overlay.append(dlg)
        page.update()
        time.sleep(3)
        dlg.open = False
        page.update()

    

    

    def obtener_datos(e):
        mostrar_dialogo_cargando()
        memoria = memoria_field.value
        ram = ram_field.value
        precio = precio_field.value
        estrellas = estrellas_field.value
        marca = marca_field.value
        dimensiones = dimensiones_field.value
        peso = peso_field.value

        resultado = realizar_prediccion(memoria, ram, precio, estrellas, marca, dimensiones, peso)

        resultado_text.value = f"Resultado de la predicción: {resultado}"
        resultado_text.color = ft.colors.GREEN_700 if resultado == "Buena oferta" else ft.colors.RED_700
        page.update()
        

    def realizar_prediccion(memoria, ram, precio, estrellas, marca, dimensiones, peso):
        url = "http://localhost:5000/predecir"
        data = {
            "Memoria": memoria,
            "RAM": ram,
            "Precio": precio,
            "Estrellas": estrellas,
            "Marca": marca,
            "Dimensiones": dimensiones,
            "Peso": peso
        }
        
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            if "prediccion" in response_data:
                return response_data["prediccion"]
            else:
                return "Error en la predicción"

        except Exception as e:
            return "Error inesperado"

    boton_obtener = CustomButton(accion=obtener_datos, texto="Comprueba")

    page.add(
        CustomSpacerRow(),
        ft.Row(
            [
                ft.Column([memoria_field], expand=True),
                ft.Column([ram_field], expand=True),
                ft.Column([precio_field], expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        ft.Row(
            [
                ft.Column([estrellas_field], expand=True),
                ft.Column([marca_field], expand=True),
                ft.Column([dimensiones_field], expand=True),
                ft.Column([peso_field], expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        CustomSpacerRow(),
        ft.Row([boton_obtener], alignment=ft.MainAxisAlignment.CENTER),
        CustomSpacerRow(),
        ft.Row([resultado_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Row([boton_tema], alignment=ft.MainAxisAlignment.CENTER),
    )

if __name__ == "__main__":
    ft.app(target=main)

