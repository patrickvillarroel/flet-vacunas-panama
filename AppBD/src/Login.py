import flet as ft
from flet import *


def log(page: Page):
    page.title = 'VacunAPP'
    page.window_width = 900
    page.window_height = 500
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

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
                        ft.Text(
                            'Iniciar sesión',
                            width=400,
                            size=30,
                            weight='w900',
                            text_align='center',
                        ),
                        ft.Container(
                            ft.TextField(
                                width=200,
                                height=40,
                                hint_text='Usuario',
                                border='underline',
                                prefix_icon=ft.icons.PERSON,
                            ),
                            padding=ft.padding.only(20, -10),
                        ),
                        ft.Container(
                            ft.TextField(
                                width=200,
                                height=40,
                                hint_text='Contraseña',
                                prefix_icon=ft.icons.LOCK,
                                border='underline',
                                color='black',
                                password=True,
                            ),
                            padding=ft.padding.only(20),
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                content=ft.Text(
                                    'INICIAR',
                                    color='blue',
                                    weight='w500',
                                ),
                                width=200,
                                bgcolor='white',
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.Row([
                                ft.Text('¿No tiene una cuenta?'),
                                ft.TextButton('Crear una cuenta'),
                            ], spacing=8),
                            padding=ft.padding.only(24),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                gradient=ft.LinearGradient(['blue', 'lightblue']),
                width=320,
                height=460,
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

    page.controls.append(contenedor)
    page.update()
def open_new_window(e):
    ft.app(target=log())
