from datetime import datetime
import flet as ft
import requests as req
import subprocess
import sys

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

            if response.json().get("vehi_esta_dentro") == True:
                url = "http://localhost:5000/saleCoche"
                response = req.post(url, json={"matricula": matricula})
                informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha salido del aparcamiento a la hora {hora_actual}"
                informacion_estado_vehiculo.visible = True

                url = "http://localhost:5000/calcularImporte"
                response = req.get(url, params={"matricula": matricula})
                minutos=response.json().get('minutos')

                if minutos != None:
                    importeFinal=minutos*0.1
                    informacion_importe_vehiculo.value = f"El vehiculo con matrícula {matricula} ha estado {minutos} minutos en el aparcamiento. El importe a pagar es de {importeFinal} euros."
                else:
                    informacion_importe_vehiculo.value = f"El vehiculo con matrícula {matricula} ha estado {minutos} minutos en el aparcamiento. No tienes que pagar nada."

                informacion_importe_vehiculo.visible = True
            else:
                url = "http://localhost:5000/entraCoche"
                response = req.post(url, json={"matricula": matricula})
                informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha entrado al aparcamiento a la hora {hora_actual}"
                informacion_estado_vehiculo.visible = True
                informacion_importe_vehiculo.visible = False
        else:
            informacion_estado_vehiculo.value = "Por favor, introduce una matrícula válida en el campo de texto."
        
        page.update()
                
    campo_texto_matricula = ft.TextField(
        label="Matricula",
        autofocus=True,
        width=200,
        text_align=ft.TextAlign.LEFT,
        on_submit=enviarMatricula,
    )

    def handle_image_result(matricula):
        if matricula:
            campo_texto_matricula.value = matricula
            page.update()
            enviarMatricula(None)  # Simulate click event

    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0].path
            print(f"Archivo seleccionado: {selected_file}")
            
            # Call the plate detection script
            try:
                result = subprocess.run(
                    [sys.executable, "Projecte2/main.py", "--image", selected_file],
                    capture_output=True,
                    text=True,
                    check=True
                )
                matricula = result.stdout.strip()
                print(f"Matrícula detectada: {matricula}")
                handle_image_result(matricula)
            except subprocess.CalledProcessError as e:
                print(f"Error al procesar la imagen: {e.stderr}")
                informacion_estado_vehiculo.value = "Error al procesar la imagen. Intente con otra."
                informacion_estado_vehiculo.visible = True
                page.update()

    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    boton_aparcamiento = ft.IconButton(
        icon=ft.icons.LOCAL_PARKING,
        tooltip="Simular entrada/salida de coche",
        on_click=enviarMatricula,
        style=ft.ButtonStyle(icon_size=50)
    )

    boton_imagen = ft.ElevatedButton(
        text="Seleccionar imagen",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"]
        )
    )

    page.add(
        ft.Column([
            ft.Row([ft.Container(height=50)]),
            ft.Row([campo_texto_matricula, boton_aparcamiento], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([boton_imagen], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Container(height=50)]),
            ft.Row([informacion_estado_vehiculo], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([informacion_importe_vehiculo], alignment=ft.MainAxisAlignment.CENTER),
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)