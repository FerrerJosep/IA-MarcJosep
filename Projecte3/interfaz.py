import flet as ft


def main(page: ft.Page):
    page.title = "Interfaz de Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(ft.Text("Hola, Flet!"))
    page.add(ft.ElevatedButton("Click me!", on_click=lambda _: print("Button clicked!")))


if __name__ == "__main__":
    ft.app(target=main)