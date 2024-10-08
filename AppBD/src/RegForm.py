import flet as ft
from flet import *
import datetime

def formulario(page: Page):
    page.title = 'Paciente'
    page.window_width = 1300
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.resizable = False
    page.spacing = 0

    doc_identificacion = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="ced", label="Cedula"),
        ft.Radio(value="pass", label="Pasaporte")]))

    def handle_change(e):
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}"))

    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    registro = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Vacunas APP", weight="bold", size=40, color=ft.colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                                ft.Text("Registrarse", size=20, color=ft.colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(),
                        ft.Column(
                            [
                                ft.TextField(label="Nombre", value="Prueba", width=270, color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                ft.TextField(label="Segundo Nombre", value="Prueba", width=270, color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                ft.TextField(label="Apellido", value="Prueba", width=270, color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                ft.TextField(label="Segundo Apellido", value="Prueba", width=270, color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                ft.ElevatedButton(
                                    "Pick date",
                                    icon=ft.icons.CALENDAR_MONTH,
                                    on_click=lambda e: page.open(
                                        ft.DatePicker(
                                            first_date=datetime.datetime(year=1900, month=1, day=1),
                                            last_date=datetime.datetime(year=2024, month=12, day=31),
                                            on_change=handle_change,
                                            on_dismiss=handle_dismissal,
                                        )
                                    ),
                                ),
                                doc_identificacion,
                                ft.TextField(label="Doc.Identificacion", value="Prueba", width=270,
                                             color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                ft.TextField(label="Num.Telefono", value="Prueba", width=270,
                                             color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                ft.TextField(label="Corro Electronico", value="Prueba", width=270,
                                             color=ft.colors.BLACK,
                                             label_style=ft.TextStyle(color='black', size=19, weight="bold")),

                            ],
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.all(0),
                bgcolor=ft.colors.WHITE,
                height=700,
                width=1300,
            )
        ],

    )
    page.clean()

    page.add(registro)
    page.update()


ft.app(target=formulario)
