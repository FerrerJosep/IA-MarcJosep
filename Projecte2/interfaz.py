from datetime import datetime

import flet as ft
import requests as req

def main(page: ft.Page):
    page.title = "Interfaz de prueba"

    informacion_estado_vehiculo = ft.Text("Estado del vehículo", size=20, color=ft.colors.BLUE_900, visible=False)
    informacion_importe_vehiculo = ft.Text("Importe del vehículo", size=20, color=ft.colors.BLUE_900, visible=False)

    def enviarMatricula(e):
        
        matricula = campo_texto_matricula.value
        print(matricula)

        hora_actual = datetime.now().strftime("%H:%M:%S")


        if matricula:

            url = "http://localhost:5000/estadoAparcamiento"
            response = req.post(url, json={"matricula": matricula})
            print(response.json())

            # Comprobar si el coche está dentro o fuera del aparcamiento
            if response.json().get("vehi_esta_dentro") == True:
                # Si el coche esta dentro, simulamos que sale
                url = "http://localhost:5000/saleCoche"
                response = req.post(url, json={"matricula": matricula})
                informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha salido del aparcamiento a la hora {hora_actual}"

                informacion_estado_vehiculo.visible = True

                # Calculamos el importe segun el tiempo que ha estado dentro
                url = "http://localhost:5000/calcularImporte"
                response = req.get(url, params={"matricula": matricula})
                minutos=response.json().get('minutos')

                if minutos != None:
                    # Si el coche ha estado mas de 1 minuto, se le cobra
                    importeFinal=minutos*0.1
                    informacion_importe_vehiculo.value = f"El vehiculo con matrícula {matricula} ha estado {minutos} minutos en el aparcamiento. El importe a pagar es de {importeFinal} euros."
                    

                else:
                    # Si el coche ha estado menos de 1 minuto, no se le cobra nada
                    informacion_importe_vehiculo.value = f"El vehiculo con matrícula {matricula} ha estado {minutos} minutos en el aparcamiento. No tienes que pagar nada."

                informacion_importe_vehiculo.visible = True



            else:

                url = "http://localhost:5000/entraCoche"
                response = req.post(url, json={"matricula": matricula})
                informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha entrado al aparcamiento a la hora {hora_actual}"
                informacion_estado_vehiculo.visible = True

                # No mostramos el importe porque no se ha calculado
                informacion_importe_vehiculo.visible = False
                # Mostramos el estado del vehiculo
                informacion_estado_vehiculo.visible = True
                

            # if response.json().get("vehi_esta_dentro") == False:
            #     # Entra el coche
            #     url = "http://localhost:5000/entraCoche"
            #     response = req.post(url, json={"matricula": matricula})
            #     informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha entrado al aparcamiento"
            
            # if response.json().get("vehi_esta_dentro") == "coche_no_existe":
            #     informacion_estado_vehiculo.value = "Por favor, introduce una matrícula válida."
        else:

            informacion_estado_vehiculo.value = "Por favor, introduce una matrícula válida en el campo de texto."

        
        page.update()
                
            
            

    campo_texto_matricula = ft.TextField(
        label="Matricula",
        autofocus=True,
        width=200,
        text_align=ft.TextAlign.LEFT,
        on_submit=enviarMatricula,)
    

    # --- Función para seleccionar imagen ---
    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0].path
            print(f"Archivo seleccionado: {selected_file}")
            return selected_file
            # Aquí puedes hacer lo que quieras con la imagen, como subirla, mostrarla, etc.

    # Crear el FilePicker
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    

    # Botón para entrar al aparcamiento
    boton_aparcamiento = ft.IconButton(
        icon=ft.icons.LOCAL_PARKING,
        tooltip="Simular entrada/salida de coche",
        on_click=enviarMatricula,
        style=ft.ButtonStyle(icon_size=50)
    )

    # Botón para seleccionar imagen
    boton_imagen = ft.ElevatedButton(
        text="Seleccionar imagen",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"]
        )
    )

    # Agregar botones a la página
    page.add(
        ft.Column([
            ft.Row([ft.Container(height=50)]),
            ft.Row([ campo_texto_matricula, boton_aparcamiento], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([boton_imagen], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Container(height=50)]),
            ft.Row([informacion_estado_vehiculo], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([informacion_importe_vehiculo], alignment=ft.MainAxisAlignment.CENTER),
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
