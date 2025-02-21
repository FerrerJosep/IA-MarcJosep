import flet as ft

# Esta clase hereda de ft.TextField y añade un icono y un color de fondo personalizado
# Parametros:
#   - label: texto que aparecerá en la parte superior del TextField
#   - hint_text: texto que aparecerá en el TextField cuando no haya texto
#   - icon: icono que aparecerá en la parte izquierda del TextField
#   - escalado: factor de escalado del TextField
class CustomTextField(ft.TextField):
    def __init__(self, label, hint_text, icon=None, escalado=None, color_fondo=None, radio_borde=None):
        # Aqui se definen los valores por defecto de los campos que pueden ser None
        if color_fondo is None:
            color_fondo = ft.colors.GREY_200
        if escalado is None:
            escalado = 1
        if radio_borde is None:
            radio_borde = 10

        if icon is None:
            icon = ft.icons.TEXT_FIELDS
        super().__init__(
            label=label,
            hint_text=hint_text,
            prefix_icon=icon,
            border_radius=radio_borde,
            bgcolor=color_fondo,
            scale=escalado)



# Esta clase hereda de ft.ElevatedButton
# Parametros:
#   - texto: texto que aparecerá en el botón
#   - accion: función que se ejecutará al hacer click en el botón (No puede ser nula porque de normal un boton realiza una acción)
#   - color: color del botón
class CustomButton(ft.ElevatedButton):
    def __init__(self, texto: str, accion, color=None):
        # Establecemos un color por defecto si no se pasa ninguno
        if color is None:
            color = ft.colors.BLUE

        # Llamamos al constructor de la clase base (ft.ElevatedButton)
        super().__init__(text=texto, on_click=accion, color=color)

# Esta clase hereda de ft.Row y añade un espacio en blanco
# Parametros:
#   - height: altura del espacio en blanco
class CustomSpacerRow(ft.Row):
    def __init__(self, height=40):
        super().__init__(height=height)