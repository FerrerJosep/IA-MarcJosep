import flet as ft
from aws import consulta_simple  # o también puedes importar consulta_avanzada si deseas

def main(page: ft.Page):
    page.title = "ChatBot AWS – Interfaz Profesional"
    page.window_width = 600
    page.window_height = 800
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )

    user_input = ft.TextField(
        hint_text="Escribe tu mensaje...",
        expand=True,
        autofocus=True,
        on_submit=lambda e: send_message(None)
    )

    def send_message(e):
        msg = user_input.value.strip()
        if not msg:
            return

        # Agrega el mensaje del usuario
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(f"Tú: {msg}", selectable=True),
                alignment=ft.alignment.center_right,
                padding=10,
                bgcolor=ft.colors.BLUE_100,
                border_radius=10,
            )
        )

        # Llama a la API de consulta simple
        respuesta = consulta_simple(msg)
        texto = respuesta.get("text") or respuesta.get("respuesta") or "No se obtuvo respuesta."

        # Agrega la respuesta del bot
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(f"Bot: {texto}", selectable=True),
                alignment=ft.alignment.center_left,
                padding=10,
                bgcolor=ft.colors.GREY_200,
                border_radius=10,
            )
        )

        user_input.value = ""
        page.update()

    def clear_chat(e):
        chat_history.controls.clear()
        page.update()

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        tooltip="Enviar mensaje",
        on_click=send_message,
    )

    clear_button = ft.IconButton(
        icon=ft.icons.DELETE_FOREVER,
        tooltip="Eliminar historial del chat",
        on_click=clear_chat,
    )

    controls_row = ft.Row(
        controls=[user_input, send_button, clear_button],
        spacing=5,
    )

    page.add(chat_history, controls_row)

ft.app(target=main)
