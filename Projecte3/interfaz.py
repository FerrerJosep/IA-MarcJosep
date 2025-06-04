import flet as ft
from aws import consulta_simple

async def main(page: ft.Page):
    page.title = "ChatBot AWS"
    page.window_width = 600
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True
    )
    

    typing_indicator = ft.Text(
        "El bot está escribiendo...",
        visible=False,
        italic=True,
        color=ft.colors.GREY,
        size=12
        
    )

    # Campo de entrada
    user_input = ft.TextField(
        hint_text="Escribe tu mensaje...",
        expand=True,
        autofocus=True,
        multiline=True,
        min_lines=1,
        max_lines=6,
        filled=True,
        border_radius=20,
        bgcolor=ft.colors.GREY_100,
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        tooltip="Enviar mensaje (Ctrl+Enter)",
        on_click=lambda e: send_message(),
        disabled=False,
    )

    clear_button = ft.IconButton(
        icon=ft.icons.DELETE_FOREVER,
        tooltip="Eliminar historial del chat",
        on_click=lambda e: clear_chat(),
    )

    def send_message():
        msg = user_input.value.strip()
        if not msg:
            return

        send_button.disabled = True
        typing_indicator.visible = True
        page.update()

        chat_history.controls.append(
            ft.Container(
                content=ft.Text(msg, selectable=True),
                alignment=ft.alignment.center_right,
                padding=10,
                bgcolor=ft.colors.BLUE_100,
                border_radius=10,
                margin=5,
            )
        )

        user_input.value = ""
        page.update()

        respuesta = consulta_simple(msg)
        texto = respuesta.get("text") or respuesta.get("respuesta") or "No se obtuvo respuesta."

        chat_history.controls.append(
            ft.Container(
                content=ft.Text(texto, selectable=True),
                alignment=ft.alignment.center_left,
                padding=10,
                bgcolor=ft.colors.GREY_200,
                border_radius=10,
                margin=5,
            )
        )

        typing_indicator.visible = False
        send_button.disabled = False
        page.update()

    def clear_chat():
        chat_history.controls.clear()
        page.update()

    # Capturar eventos de teclado en toda la página
    def keyboard_handler(e: ft.KeyboardEvent):
        if user_input.focus:
            if e.ctrl and e.key == "Enter":
                send_message()
            elif e.key == "Enter":
                user_input.value += "\n"
                page.update()

    page.on_keyboard_event = keyboard_handler

    input_row = ft.Row(
        controls=[user_input, send_button, clear_button],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    page.add(
        ft.Column(
            controls=[
                chat_history,
                ft.Container(
                    typing_indicator,
                    padding=10                   
                ),
                
                
            ],
            expand=True,
        ),
        ft.Container(content=input_row, padding=ft.padding.only(bottom=20, left=10, right=10))
    )

ft.app(target=main)