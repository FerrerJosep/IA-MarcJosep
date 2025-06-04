import flet as ft
from aws import consulta_simple
import os



def main(page: ft.Page):
    # Título y configuración de la página
    page.title = "ChatBot AWS"
    page.window_width = 600
    page.window_height = 800
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    # Obtener la ruta absoluta de la imagen
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bot_image_path = os.path.join(current_dir, "bot.jpg")

    # Verificar si la imagen existe
    if not os.path.exists(bot_image_path):
        bot_image_path = None

    # devuelve true si el modo oscuro está activo
    def is_dark_mode():
        return page.theme_mode == ft.ThemeMode.DARK


    def apply_theme():
        # Si esta oscuro, entra por aquí
        if is_dark_mode():
            # Lo pone normal
            page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    background=ft.colors.GREY_900,
                    surface=ft.colors.GREY_800,
                    on_surface=ft.colors.WHITE,
                    primary=ft.colors.BLUE_GREY_300,
                    on_primary=ft.colors.BLACK,
                )
            )
        else:
            
            pass
            #page.theme = ft.Theme()
            
        page.update()

    apply_theme()

    def get_input_bg():
        # Si está oscuro, pone un color gris oscuro
        # Si está claro, pone un color gris claro
        return ft.colors.GREY_800 if is_dark_mode() else ft.colors.GREY_100

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
        color=ft.colors.GREY_400,
        size=12
    )

    user_input = ft.TextField(
        hint_text="Escribe tu mensaje...",
        expand=True,
        autofocus=True,
        multiline=True,
        min_lines=1,
        max_lines=6,
        filled=True,
        border_radius=20,
        bgcolor=get_input_bg()
    )

    def send_message():
        msg = user_input.value.strip()
        if not msg:
            return

        send_button.disabled = True
        typing_indicator.visible = True
        page.update()

        # Configuración de colores
        user_msg_bg = ft.colors.BLUE_100 if not is_dark_mode() else ft.colors.BLUE_GREY_700
        user_text_color = ft.colors.BLACK if not is_dark_mode() else ft.colors.WHITE
        bot_msg_bg = ft.colors.GREY_200 if not is_dark_mode() else ft.colors.GREY_700
        bot_text_color = ft.colors.BLACK if not is_dark_mode() else ft.colors.WHITE

        # Mensaje del usuario 
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(msg, selectable=True, color=user_text_color, size=14),
                alignment=ft.alignment.center_right,
                padding=10,
                bgcolor=user_msg_bg,
                border_radius=10,
                margin=5,
            )
        )

        user_input.value = ""
        page.update()

        try:
            respuesta = consulta_simple(msg)
            print("Respuesta recibida:", respuesta)
            
            if isinstance(respuesta, dict):
                #texto = respuesta.get("text") or respuesta.get("respuesta") or str(respuesta)
                texto = respuesta.get("text")
            else:
                texto = str(respuesta)

            # Mensaje del bot (ancho limitado al 85%)
            bot_image = ft.Image(
                src=bot_image_path if bot_image_path else None,
                width=40,
                height=40,
                fit=ft.ImageFit.CONTAIN,
                border_radius=20,
                error_content=ft.Icon(ft.icons.ANDROID, size=40) if not bot_image_path else None
            )

            chat_history.controls.append(
                ft.Row(
                    controls=[
                        bot_image,
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Bot AWS", weight="bold", size=10, color=bot_text_color),
                                ft.Text(texto, selectable=True, color=bot_text_color, size=14),
                            ]),
                            padding=10,
                            bgcolor=bot_msg_bg,
                            border_radius=10,
                            margin=5,
                            width=page.window_width * 0.85,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                )
            )
        # Error en la llamada.
        except Exception as e:
            print("Error:", str(e))
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(f"Error: {str(e)}", color=ft.colors.RED),
                    alignment=ft.alignment.center_left,
                    padding=10,
                    bgcolor=ft.colors.GREY_200,
                    border_radius=10,
                )
            )

        typing_indicator.visible = False
        send_button.disabled = False
        page.update()

    def clear_chat():
        chat_history.controls.clear()
        page.update()

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if is_dark_mode() else ft.ThemeMode.DARK
        )
        apply_theme()
        user_input.bgcolor = get_input_bg()
        page.update()

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        tooltip="Enviar mensaje (Ctrl+Enter)",
        on_click=lambda e: send_message(),
    )

    clear_button = ft.IconButton(
        icon=ft.icons.DELETE_FOREVER,
        tooltip="Eliminar historial del chat",
        on_click=lambda e: clear_chat(),
    )

    theme_button = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        tooltip="Cambiar modo claro/oscuro",
        on_click=toggle_theme,
    )

    def keyboard_handler(e: ft.KeyboardEvent):
        if user_input.focus:
            if e.ctrl and e.key == "Enter":
                send_message()
            elif e.key == "Enter":
                user_input.value += "\n"
                page.update()

    page.on_keyboard_event = keyboard_handler

    input_row = ft.Row(
        controls=[user_input, send_button, clear_button, theme_button],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    page.add(
        ft.Column(
            controls=[
                chat_history,
                ft.Container(typing_indicator, padding=10),
            ],
            expand=True,
        ),
        ft.Container(
            content=input_row, 
            padding=ft.padding.only(bottom=20, left=10, right=10)
        )
    )

ft.app(target=main)