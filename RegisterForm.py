import flet as ft
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def formulario(page: ft.Page):
    page.title = 'Paciente'
    page.window.width = 900
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.resizable = False
    page.adaptive = True
    page.spacing = 0

    tipo_identificacion = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(
                value="ced",
                label="Cedula",
                fill_color=ft.colors.BLUE,
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,
                )
            ),
            ft.Radio(
                value="pass",
                label="Pasaporte",
                fill_color=ft.colors.BLUE,
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,
                )
            )
        ])
    )

    def handle_change(e):
        fecha.value = e.control.value.strftime('%Y-%m-%d')
        page.update()

    def handle_dismissal(e):
        logger.info(f"datetime picker dismissed. {e.control.value}")

    fecha = ft.TextField(label="Fecha de Nacimiento", width=210, color=ft.colors.BLACK,
                         label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    registro = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Vacunas APP", weight=ft.FontWeight.BOLD, size=40, color=ft.colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                                ft.Text("Registrarse", size=20, color=ft.colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    ft.Column(
                                        controls=
                                        [
                                            ft.Row(
                                                controls=[
                                                    ft.Column(
                                                        controls=
                                                        [
                                                            ft.Row(
                                                                controls=
                                                                [
                                                                    ft.Text(
                                                                        "Datos Personales", color="black", size=20,
                                                                        weight=ft.FontWeight.BOLD
                                                                    ),
                                                                ],
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                            ),
                                                            ft.TextField(label="Nombre", width=270,
                                                                         color=ft.colors.BLACK,
                                                                         label_style=ft.TextStyle(color='black',
                                                                                                  size=15,
                                                                                                  weight=ft.FontWeight.BOLD)),
                                                            ft.TextField(label="Segundo Nombre", width=270,
                                                                         color=ft.colors.BLACK,
                                                                         label_style=ft.TextStyle(color='black',
                                                                                                  size=15,
                                                                                                  weight=ft.FontWeight.BOLD)),
                                                            ft.TextField(label="Apellido", width=270,
                                                                         color=ft.colors.BLACK,
                                                                         label_style=ft.TextStyle(color='black',
                                                                                                  size=15,
                                                                                                  weight=ft.FontWeight.BOLD)),
                                                            ft.TextField(label="Segundo Apellido", width=270,
                                                                         color=ft.colors.BLACK,
                                                                         label_style=ft.TextStyle(color='black',
                                                                                                  size=15,
                                                                                                  weight=ft.FontWeight.BOLD)),
                                                            ft.Row(controls=[
                                                                fecha,
                                                                ft.IconButton(
                                                                    icon=ft.icons.CALENDAR_MONTH,
                                                                    width=50,
                                                                    bgcolor="blue",
                                                                    on_click=lambda e: page.open(
                                                                        ft.DatePicker(
                                                                            first_date=datetime(year=1900,
                                                                                                         month=1,
                                                                                                         day=1),
                                                                            last_date=datetime.now(),
                                                                            on_change=handle_change,
                                                                            on_dismiss=handle_dismissal,
                                                                        )
                                                                    ),
                                                                ),
                                                            ])
                                                        ],
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                    ),
                                                    ft.Container(
                                                        ft.Column(
                                                            controls=
                                                            [
                                                                tipo_identificacion,
                                                                ft.Row(),
                                                                ft.TextField(label="Doc.Identificacion", width=270,
                                                                             color=ft.colors.BLACK,
                                                                             label_style=ft.TextStyle(color='black',
                                                                                                      size=15,
                                                                                                      weight=ft.FontWeight.BOLD)),
                                                                ft.TextField(label="Num.Telefono", width=270,
                                                                             color=ft.colors.BLACK,
                                                                             label_style=ft.TextStyle(color='black',
                                                                                                      size=15,
                                                                                                      weight=ft.FontWeight.BOLD)),
                                                                ft.TextField(label="Corro Electronico", width=270,
                                                                             color=ft.colors.BLACK,
                                                                             label_style=ft.TextStyle(color='black',
                                                                                                      size=15,
                                                                                                      weight=ft.FontWeight.BOLD)),
                                                            ],
                                                        ),
                                                        height=230
                                                    ),

                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,
                                            ),
                                        ]
                                    ),
                                    height=330,
                                    width=280 * 2,
                                    alignment=ft.alignment.center,
                                    border=ft.border.all(1, "black"),
                                    border_radius=10,
                                ),
                                ft.Container(
                                    ft.Column([
                                        ft.Text(
                                            "Direccion", color="black", size=20, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Dropdown(
                                            label="Provincia",  # Etiqueta personalizada
                                            icon_enabled_color=ft.colors.BLACK,
                                            options=[
                                                ft.dropdown.Option("Panamá"),
                                                ft.dropdown.Option("Colón"),
                                                ft.dropdown.Option("Coclé"),
                                            ],
                                            autofocus=True,
                                            width=270,
                                            label_style=ft.TextStyle(
                                                color=ft.colors.BLACK,
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            text_style=ft.TextStyle(
                                                color=ft.colors.BLACK,
                                                size=14,
                                            ),
                                            hint_style=ft.TextStyle(
                                                color=ft.colors.BLACK,
                                                size=14,
                                            ),
                                            bgcolor=ft.colors.WHITE,
                                            border_radius=10,
                                            content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                            border_color="Black"

                                        ),
                                        ft.Dropdown(
                                            label="Distrito",
                                            icon_enabled_color=ft.colors.BLACK,
                                            options=[
                                                ft.dropdown.Option("Panamá"),
                                                ft.dropdown.Option("San Miguelito"),
                                            ],
                                            autofocus=True,
                                            width=270,
                                            label_style=ft.TextStyle(
                                                color=ft.colors.BLACK,
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            text_style=ft.TextStyle(
                                                color=ft.colors.BLACK,
                                                size=14,
                                            ),
                                            hint_style=ft.TextStyle(
                                                color=ft.colors.BLACK,
                                                size=14,
                                            ),
                                            bgcolor=ft.colors.WHITE,
                                            border_radius=10,
                                            content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                            border_color="Black"

                                        ),
                                        ft.TextField(label="Dirección Exacta", width=270,
                                                     color=ft.colors.BLACK,
                                                     label_style=ft.TextStyle(color='black', size=15,
                                                                              weight=ft.FontWeight.BOLD)),
                                    ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    height=330,
                                    width=280,
                                    border=ft.border.all(0, "black"),
                                    border_radius=10,
                                )

                            ],
                            alignment=ft.MainAxisAlignment.CENTER,

                        ),
                        ft.Row(controls=[
                            ft.ElevatedButton(
                                "Registrarse",
                                width=170,
                                height=50,
                                style=ft.ButtonStyle(
                                    color={ft.ControlState.DEFAULT: ft.colors.WHITE,
                                           ft.ControlState.HOVERED: ft.colors.WHITE},

                                    bgcolor={ft.ControlState.DEFAULT: ft.colors.BLUE_700,
                                             ft.ControlState.HOVERED: ft.colors.BLUE_900},

                                    shape=ft.RoundedRectangleBorder(radius=25),
                                    elevation={"pressed": 10, "default": 2},
                                    animation_duration=300,
                                ),
                                icon=ft.icons.UPDATE,
                                icon_color=ft.colors.WHITE,
                                on_click=lambda e: logger.info("Usuario registrado"),
                            ),
                        ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )

                    ],

                ),
                alignment=ft.alignment.center,
                margin=ft.margin.all(0),
                bgcolor=ft.colors.WHITE,
                height=500,
                width=900,
                expand=True
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.START
    )
    page.clean()

    page.add(registro)
    page.update()


ft.app(target=formulario)
