import flet as ft
import datetime
from managers import ApiManager
from typing import List
from validations.DireccionesDto import ProvinciaDto, DistritoDto


async def obtener_provincias_y_distritos():
    provincias = await ApiManager.get_provincias()
    distritos = await ApiManager.get_distritos()  # Devuelve todos los distritos
    return provincias, distritos


def filtrar_distritos_por_provincia(distritos: List[DistritoDto], provincia_id: int):
    return [d for d in distritos if d.provincia.id == provincia_id]


async def formulario(page: Page):
    page.title = 'Paciente'
    page.window.width = 900
    page.window.height = 650
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.resizable = False
    page.spacing = 0

    provincias, distritos = await obtener_provincias_y_distritos()

    doc_identificacion = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(
                value="ced",
                label="Cedula",
                fill_color=ft.colors.BLUE,  # Cambia el color del botón
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,  # Cambia el color del texto
                )
            ),
            ft.Radio(
                value="pass",
                label="Pasaporte",
                fill_color=ft.colors.BLUE,  # Cambia el color del botón
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,  # Cambia el color del texto
                )
            )
        ])
    )

    sexo = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(
                value="Masculino",
                label="M",
                fill_color=ft.colors.BLUE,  # Cambia el color del botón
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,  # Cambia el color del texto
                )
            ),
            ft.Radio(
                value="2",
                label="F",
                fill_color=ft.colors.BLUE,  # Cambia el color del botón
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,  # Cambia el color del texto
                )
            ),
            ft.Radio(
                value="3",
                label="O",
                fill_color=ft.colors.BLUE,  # Cambia el color del botón
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,  # Cambia el color del texto
                )
            )
        ])
    )

    dropdown_provincia = ft.Dropdown(
        label="Provincia",  # Etiqueta personalizada
        icon_enabled_color=ft.colors.BLACK,
        options=[ft.dropdown.Option(text=prov.nombre, key=str(prov.id)) for prov in provincias],
        on_change=lambda e: actualizar_distritos(e.control.value),
        value=str(0),
        autofocus=True,
        width=270,
        label_style=ft.TextStyle(
            color=ft.colors.BLACK,  # Cambia el color del label
            size=16,  # Cambia el tamaño del texto
            weight=ft.FontWeight.BOLD,  # Hacer el label en negrita
        ),
        text_style=ft.TextStyle(
            color=ft.colors.BLACK,  # Cambia el color del texto seleccionado
            size=14,  # Tamaño del texto seleccionado
        ),
        hint_style=ft.TextStyle(
            color=ft.colors.BLACK,  # Cambia el color del label
            size=14,  # Cambia el tamaño del texto
        ),
        bgcolor=ft.colors.WHITE,  # Color de fondo del Dropdown
        border_radius=10,  # Esquinas redondeadas del Dropdown
        content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_color="Black"

    )

    dropdown_distrito = ft.Dropdown(
        label="Dristito",  # Etiqueta personalizada
        icon_enabled_color=ft.colors.BLACK,
        options=[],
        value=str(0),
        autofocus=True,
        width=270,
        label_style=ft.TextStyle(
            color=ft.colors.BLACK,  # Cambia el color del label
            size=16,  # Cambia el tamaño del texto
            weight=ft.FontWeight.BOLD,  # Hacer el label en negrita
        ),
        text_style=ft.TextStyle(
            color=ft.colors.BLACK,  # Cambia el color del texto seleccionado
            size=14,  # Tamaño del texto seleccionado
        ),
        hint_style=ft.TextStyle(
            color=ft.colors.BLACK,  # Cambia el color del label
            size=14,  # Cambia el tamaño del texto
        ),
        bgcolor=ft.colors.WHITE,  # Color de fondo del Dropdown
        border_radius=10,  # Esquinas redondeadas del Dropdown
        content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_color="Black"

    )

    def handle_change(e):
        fecha.value = e.control.value.strftime('%Y-%m-%d')
        page.update()

    def handle_dismissal(e):
        print("Necesito una fecha")

    fecha = ft.TextField(label="Fecha de Nacimiento", width=210, color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK, size=15, weight=ft.FontWeight.BOLD))

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
                                                                        weight=ft.FontWeight.BOLD,
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
                                                                            first_date=datetime.datetime(year=1900,
                                                                                                         month=1,
                                                                                                         day=1),
                                                                            last_date=datetime.datetime(year=2024,
                                                                                                        month=12,
                                                                                                        day=31),
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
                                                                doc_identificacion,
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
                                                                ft.Row(),
                                                                ft.Row(controls=[
                                                                    ft.Text("Sexo: ", size=15, weight=ft.FontWeight.BOLD,
                                                                            color="black"), sexo],
                                                                       alignment=ft.MainAxisAlignment.CENTER),

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
                                    width=280*2,
                                    alignment=ft.alignment.center,
                                    border=ft.border.all(1, "black"),
                                    border_radius=10,
                                ),
                                ft.Container(
                                    ft.Column([
                                        ft.Text(
                                            "Direccion", color="black", size=15, weight=ft.FontWeight.BOLD
                                        ),
                                        dropdown_provincia,
                                        dropdown_distrito,
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
                                icon=ft.icons.MEDICAL_INFORMATION,
                                icon_color=ft.colors.WHITE,
                                on_click=lambda e: print("Usuario Registrado!"),
                            ),
                        ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )

                    ],

                ),
                alignment=ft.alignment.center,
                margin=ft.margin.all(0),
                bgcolor=ft.colors.WHITE,
                height=525,
                width=880,
                expand=True,

            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        height=500
    )
    page.clean()

    reg_container = ft.Container(
        content=registro,
        width=880,
        height=525,
        border=ft.border.all(4, "white"),
        border_radius=50,
    )

    final_container = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src="assets/images/fondo2.jpg",
            fit=ft.ImageFit.COVER,
        ),
        content=reg_container,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.add(final_container)

    def actualizar_distritos(provincia_id):
        distritos_filtrados = filtrar_distritos_por_provincia(distritos, int(provincia_id))
        dropdown_distrito.options = [ft.dropdown.Option(text=d.nombre, key=str(d.id)) for d in distritos_filtrados]
        dropdown_distrito.value = 0
        page.update()

    page.update()


ft.app(target=formulario)