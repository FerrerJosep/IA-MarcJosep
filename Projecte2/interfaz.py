from datetime import datetime
import flet as ft
import requests as req
import subprocess
import sys
import os

def main(page: ft.Page):
    page.title = "Interfaz de prueba"

    informacion_estado_vehiculo = ft.Text("Estado del vehículo", size=20, color=ft.colors.BLUE_900, visible=False)
    informacion_importe_vehiculo = ft.Text("Importe del vehículo", size=20, color=ft.colors.BLUE_900, visible=False)

    campo_texto_matricula = ft.TextField(
        label="Matrícula",
        autofocus=True,
        width=200,
        text_align=ft.TextAlign.LEFT,
        on_submit=lambda e: enviarMatricula()
    )

    # Función que se llama tras detectar matrícula desde imagen
    def handle_image_result(matricula_detectada):
        if matricula_detectada:
            campo_texto_matricula.value = matricula_detectada
            page.update()
            enviarMatricula()

    # Lógica principal para enviar matrícula
    def enviarMatricula():
        matricula = campo_texto_matricula.value.strip().upper()
        print(f"[DEBUG] Matrícula procesada: {matricula}")

        hora_actual = datetime.now().strftime("%H:%M:%S")

        if not matricula:
            informacion_estado_vehiculo.value = "Por favor, introduce una matrícula válida en el campo de texto."
            informacion_estado_vehiculo.visible = True
            informacion_importe_vehiculo.visible = False
            page.update()
            return

        # Consultar si el coche está dentro
        response = req.post("http://localhost:5000/estadoAparcamiento", json={"matricula": matricula})
        estado = response.json()

        if estado.get("vehi_esta_dentro"):
            # Simular salida
            req.post("http://localhost:5000/saleCoche", json={"matricula": matricula})
            informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha salido del aparcamiento a las {hora_actual}"
            informacion_estado_vehiculo.visible = True

            # Calcular minutos
            response = req.post("http://localhost:5000/calcularMinutos", json={"matricula": matricula})
            minutos = response.json().get("minutos")
            print(f"[DEBUG] Minutos calculados: {minutos}")

            if minutos is not None and minutos > 0:
                importe_final = round(minutos * 0.1, 2)
                informacion_importe_vehiculo.value = f"Ha estado {minutos} minutos. Importe: {importe_final} euros."
            else:
                informacion_importe_vehiculo.value = f"No se registraron minutos suficientes. No se cobra nada."

            informacion_importe_vehiculo.visible = True

        else:
            # Simular entrada
            req.post("http://localhost:5000/entraCoche", json={"matricula": matricula})
            informacion_estado_vehiculo.value = f"El coche con matrícula {matricula} ha entrado al aparcamiento a las {hora_actual}"
            informacion_estado_vehiculo.visible = True
            informacion_importe_vehiculo.visible = False

        page.update()

    # Procesar imagen seleccionada
    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0].path
            print(f"[DEBUG] Imagen seleccionada: {selected_file}")

            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))  # <-- Arreglado aquí
                main_script_path = os.path.join(script_dir, "main.py")

                if not os.path.exists(main_script_path):
                    informacion_estado_vehiculo.value = f"main.py no encontrado en: {main_script_path}"
                    informacion_estado_vehiculo.visible = True
                    page.update()
                    return

                result = subprocess.run(
                    [sys.executable, main_script_path, "--image", selected_file],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=script_dir
                )
                matricula_detectada = result.stdout.strip()
                print(f"[DEBUG] Matrícula detectada: {matricula_detectada}")
                handle_image_result(matricula_detectada)

            except subprocess.CalledProcessError as e:
                informacion_estado_vehiculo.value = f"Error al procesar imagen: {e.stderr}"
                informacion_estado_vehiculo.visible = True
                page.update()

    # Crear FilePicker y agregarlo al overlay
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    # Botón para entrada/salida manual
    boton_aparcamiento = ft.IconButton(
        icon=ft.icons.LOCAL_PARKING,
        tooltip="Simular entrada/salida de coche",
        on_click=lambda _: enviarMatricula(),
        style=ft.ButtonStyle(icon_size=50)
    )

    # Botón para subir imagen
    boton_imagen = ft.ElevatedButton(
        text="Seleccionar imagen",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"]
        )
    )

    # Estructura de la UI
    page.add(
        ft.Column([
            ft.Row([campo_texto_matricula, boton_aparcamiento], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([boton_imagen], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([informacion_estado_vehiculo], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([informacion_importe_vehiculo], alignment=ft.MainAxisAlignment.CENTER),
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
