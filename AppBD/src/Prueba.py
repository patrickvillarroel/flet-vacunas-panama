import flet as ft
from flet import *
from Connection import *

def main(page: Page):
    page.title = 'VacunAPP'
    page.window_width = 900
    page.window_height = 950
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def show_error_message(message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ]
        )
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()


    nombre = ft.TextField(
        width=400,
        height=40,
        hint_text='Nombre',
        border='underline',
        prefix_icon=ft.icons.PERSON,
    )

    Apellido = ft.TextField(
        width=400,
        height=40,
        hint_text='Apellido',
        border='underline',
        prefix_icon=ft.icons.PERSON,
    )

    Fecha = ft.TextField(
        width=400,
        height=40,
        hint_text='Nacimiento',
        border='underline',
        prefix_icon=ft.icons.DATE_RANGE,
    )

    Cedula = ft.TextField(
        width=400,
        height=40,
        hint_text='Cedula',
        border='underline',
        prefix_icon=ft.icons.CREDIT_CARD,

    )

    Direccion = ft.TextField(
        width=400,
        height=40,
        hint_text='Direccion',
        border='underline',
        prefix_icon=ft.icons.OTHER_HOUSES,
    )

    Correo = ft.TextField(
        width=400,
        height=40,
        hint_text='Correo Electronico',
        border='underline',
        prefix_icon=ft.icons.CONTACT_MAIL,
    )

    Telefono = ft.TextField(
        width=400,
        height=40,
        hint_text='Telefono',
        border='underline',
        prefix_icon=ft.icons.CONTACT_PHONE,
    )

    user = ft.TextField(
        width=400,
        height=40,
        hint_text='Usuario',
        border='underline',
        prefix_icon=ft.icons.SUPERVISED_USER_CIRCLE,
    )

    password = ft.TextField(
        width=400,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK_PERSON,
        border='underline',
        color='black',
        password=True,
        can_reveal_password=True
    )

    go = ft.ElevatedButton(
        content=ft.Text(
            'REGISTRAR',
            color='blue',
            weight='w500',
        ),
        #on_click=lambda e: insertDato(nombre.value, user.value, password.value, 1, page),
        width=200,
        bgcolor='white',
    )

    body = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Container(
                            ft.Image(
                                src='logo.png',
                                width=100,
                                height=100
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                'REGISTRARSE',
                                width=400,
                                size=30,
                                weight='w900',
                                text_align='center',
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            controls=[
                                nombre,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                Apellido
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                Cedula
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                Fecha
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                Direccion
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                Correo
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                Telefono
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                user
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                password
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Container(
                            go,
                            alignment=ft.alignment.center
                        ),
                        ft.Row(
                            [
                                ft.TextButton(content=(ft.Text('Regresar a la pagina principal', color=ft.colors.WHITE))),
                            ],
                            spacing=1,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),


                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                gradient=ft.LinearGradient(['blue', 'lightblue']),
                width=600,
                height=900,
                border_radius=20,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
    )

    contenedor = ft.Container(
        expand=True,
        image_src="fondo2.jpg",
        image_fit=ft.ImageFit.COVER,
        content=body,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.controls.append(contenedor)
    page.update()

if __name__ == '__main__':
    ft.app(target=main)