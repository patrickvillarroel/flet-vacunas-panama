import flet as ft
import logging

logger = logging.getLogger(__name__)

# Variables globales
FONDO = "assets/images/fondo2.jpg"
LOGO = "assets/images/logo.png"
global_tipo = 0  # define el tipo de usuario en sesión


# Funciones globales
def show_error_message(page: ft.Page, message):
    error_dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(message),
        open=True,
        on_dismiss=lambda e: logger.info("error dialog dismissed"),
    )
    page.overlay.append(error_dialog)
    page.update()


def account(page: ft.Page):
    page.title = "VacunAPP"
    page.window.width = 900
    page.window.height = 500
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.adaptive = True

    # def insertDato(nom, us, pas, typ, page):
    # result = conexionU(us, pas, typ)
    # print(result)
    # if result != "None":
    # insertP(nom, us, pas, typ)
    # log(page)
    # else:
    # show_error_message("Usuario ya existente")

    nombre = ft.TextField(
        width=200,
        height=40,
        hint_text='Cedula (e-eeee-eeee)',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    user = ft.TextField(
        width=200,
        height=40,
        hint_text='Usuario',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    password = ft.TextField(
        width=200,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK,
        border=ft.InputBorder.UNDERLINE,
        color='black',
        password=True,
        can_reveal_password=True
    )

    go = ft.ElevatedButton(
        content=ft.Text(
            'REGISTRAR',
            color='blue',
            weight=ft.FontWeight.W_500,
        ),
        # on_click=lambda e: insertDato(nombre.value, user.value, password.value, 1, page),
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
                                src=LOGO,
                                width=100,
                                height=100
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Text(
                            'REGISTRARSE',
                            width=400,
                            size=30,
                            weight=ft.FontWeight.W_900,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            nombre,
                            padding=ft.padding.only(20, -10),
                        ),
                        ft.Container(
                            user,
                            padding=ft.padding.only(20, -10),
                        ),
                        ft.Container(
                            password,
                            padding=ft.padding.only(20),
                        ),
                        ft.Container(
                            go,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.Row([
                                ft.TextButton('Regresar a la pagina principal', on_click=lambda e: main(page)),
                            ], spacing=1),
                            padding=ft.padding.symmetric(-10, 50),
                            alignment=ft.alignment.center
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
        image=ft.DecorationImage(
            src=FONDO,
            fit=ft.ImageFit.COVER,
        ),
        content=body,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.controls.append(contenedor)
    page.update()


# ______________________________________________________________________________________________________________________
def paciente(page: ft.Page):
    page.title = 'VacunAPP'
    page.window.width = 1300
    page.window.height = 700
    page.bgcolor = ft.colors.BLACK
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.resizable = False
    page.adaptive = True

    result_container = ft.Column(
        alignment=ft.alignment.center
    )

    cedula = ft.TextField(
        width=300,
        height=50,
        hint_style=ft.TextStyle(color='black'),
        hint_text='Cédula del paciente a buscar',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
        color=ft.colors.BLACK,
        max_length=12,
    )

    """
    def fetch_data(cedula):
        #conn = conexion()
        #cursor = conn.cursor()
        #cursor.execute(f"select * from vwPaciente where Cedula = '{cedula}'")
        #data = cursor.fetchall()
        #conn.close()
        #return data

    def search_user():
        #ced_value = ced.value
        #data = fetch_data(ced_value)
        #table = build_table(data)
        #result_container.controls.clear()
        #result_container.controls.append(table)
        #page.update()
    """

    def show_message():
        contact_dialog = ft.AlertDialog(
            title=ft.Text("Contactos"),
            content=ft.Text("Ministerio de Salud (512-9100)" + "\n" +
                            "Caja del Seguro Social (199)"),
            open=True,
            on_dismiss=lambda e: logger.info("contact dialog dismissed"),
        )
        page.overlay.append(contact_dialog)
        page.update()

    """
    def build_table(data):
        if not data:
            return ft.Text("No se encontraron pacientes.", color=ft.colors.RED, size=20)

        rows = []
        for row in data:
            rows.append(
                ft.DataRow(
                    cells=[

                        ft.DataCell(ft.Text(row[3], color="black")),
                        ft.DataCell(ft.Text(row[8], color="black")),
                        ft.DataCell(ft.Text(row[4], color="black")),
                        ft.DataCell(ft.Text(row[5], color="black")),
                        ft.DataCell(ft.Text(row[6], color="black")),
                        ft.DataCell(ft.Text(row[7], color="black"))
                    ]
                )
            )

        table = ft.DataTable(
            width=1050,
            bgcolor=ft.colors.WHITE70,
            border=ft.border.all(2, "blue"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "blue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=50,
            data_row_color={"hovered": "0x30FF0000"},
            #show_checkbox_column=True,
            divider_thickness=0,

            columns=[

                ft.DataColumn(ft.Text("Vacuna", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(ft.Text("Numero Dosis", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(ft.Text("Enfermedad", text_align=ft.alignment.center , color=ft.colors.BLUE)),
                ft.DataColumn(ft.Text("Fecha", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(ft.Text("Sede", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(ft.Text("Dependencia", text_align=ft.alignment.center, color=ft.colors.BLUE)),

            ],
            rows=rows
        )
        return table
    """

    body2 = ft.Row([
        ft.Container(
            ft.Column(
                controls=[
                    ft.Row(height=15),
                    ft.Row(
                        controls=[ft.Text("User Information", size=30, weight=ft.FontWeight.BOLD,
                                          text_align=ft.alignment.top_center, color="blue")],
                        alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
                    ft.Row([cedula, ft.ElevatedButton("Buscar", width=120, height=50)],
                           spacing=10, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
                    ft.Container(result_container, alignment=ft.alignment.center, padding=ft.padding.symmetric(100)),
                ],
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.all(0),
            bgcolor=ft.colors.WHITE,
            height=700,
            width=1075,
        )
    ],
        alignment=ft.alignment.center,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    body3 = ft.Row([
        ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        ft.Image(
                                            src='/images/icon.png',
                                            width=100,
                                            height=100

                                        ),
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text(
                                        'Bienvenido',
                                        width=200,
                                        size=30,
                                        weight=ft.FontWeight.W_300,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        ft.ElevatedButton(content=ft.Text("Menu de inicio", color=ft.colors.BLUE),
                                                          width=170, height=40, bgcolor='white',
                                                          on_click=lambda e: main(page)),
                                    ),
                                    ft.Container(
                                        ft.ElevatedButton(content=ft.Text("Contactanos", color=ft.colors.BLUE),
                                                          width=170, height=40, bgcolor='white',
                                                          on_click=lambda e: show_message()),
                                    ),
                                ]
                            )
                        ],
                    ),
                    ft.Row(),
                    ft.Row(),
                    ft.Row(height=100),
                    ft.Row(),
                    ft.Row(),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.colors.BLUE,
            height=700,

        )
    ])

    # por usar?
    def clear_entry():
        cedula.value = ""
        page.update()

    page.clean()

    page.add(ft.Row([
        body3,
        body2
    ]))
    page.update()


# _______________________________________________________________________________________________________________________
def login(page: ft.Page):
    page.title = 'VacunAPP'
    page.window.width = 900
    page.window.height = 500
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.adaptive = True

    """
    def validarDato(us, pas, typ, pag):
        result = conexionU(us, pas, typ)
        print(result)
        if result != "None":
            show_error_message("No se encontró ningún usuario con el nombre de usuario: " + us)
        else:
            pac(page)
    """

    user = ft.TextField(
        width=200,
        height=40,
        hint_text='Usuario',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    password = ft.TextField(
        width=200,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK,
        border=ft.InputBorder.UNDERLINE,
        color=ft.colors.BLACK,
        password=True,
        can_reveal_password=True
    )

    login_in = ft.ElevatedButton(
        content=ft.Text(
            'INICIAR',
            color=ft.colors.BLUE,
            weight=ft.FontWeight.W_500,
        ),
        # on_click=lambda e: validarDato(user.value, password.value, global_tipo, page),
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
                                src=LOGO,
                                width=100,
                                height=100
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Text(
                            'Iniciar sesión',
                            width=400,
                            size=30,
                            weight=ft.FontWeight.W_900,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            user,
                            padding=ft.padding.only(20, -10),
                        ),
                        ft.Container(
                            password,
                            padding=ft.padding.only(20),
                        ),
                        ft.Container(
                            login_in,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.Row([
                                ft.Text('¿No tiene una cuenta?'),
                                ft.TextButton('Crear una cuenta', on_click=lambda e: account(page)),
                            ], spacing=8),
                            padding=ft.padding.only(24),
                        ),
                        ft.Container(
                            ft.Row([
                                ft.TextButton('Regresar a la pagina principal', on_click=lambda e: main(page)),
                            ], spacing=1),
                            padding=ft.padding.symmetric(-10, 50),
                            alignment=ft.alignment.center
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
        image=ft.DecorationImage(
            src=FONDO,
            fit=ft.ImageFit.COVER,
        ),
        content=body,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.controls.append(contenedor)
    page.update()


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# App principal
def main(page: ft.page):

    page.title = 'VacunAPP'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor=ft.colors.WHITE
    page.window.width = 900
    page.window.height = 800
    page.navigation_bar = False

    def button_click(e, t):
        global global_tipo
        paciente(e)
        global_tipo = t

    def resize(e):
        # Ajustar el contenido dependiendo del tamaño de la ventana
        if page.window.width < 600:
            # Ajustes para pantallas pequeñas
            background_container.width = 300
            background_container.height = 400
        else:
            # Ajustes para pantallas más grandes
            background_container.width = 500
            background_container.height = 600
        page.update()

    background_container = ft.Container(
        expand=True,
        width=500,
        height=700,
        bgcolor=ft.colors.LIGHT_BLUE,
        alignment=ft.alignment.center,
        content=
        ft.Container(content=ft.Column(
            controls=[
                ft.Text(
                    "VACUNAS APP", color="black", size=35, weight=ft.FontWeight.BOLD
                ),
                ft.Image(src=LOGO, width=150, height=150),
                ft.ElevatedButton(
                    text="Paciente",
                    on_click=lambda e: button_click(page, 1),
                    width=220,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=40),
                        elevation={"": 2, "hovered": 6},
                        text_style=ft.TextStyle(size=25)
                    ),
                    icon=ft.icons.PERSON,
                ),
                ft.ElevatedButton(
                    text="Doctor",
                    on_click=lambda e: button_click(page, 2),
                    width=220,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.BLUE_ACCENT, "hovered": ft.colors.BLUE},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=40),
                        elevation={"": 2, "hovered": 6},
                        text_style=ft.TextStyle(size=20)
                    ),
                    icon=ft.icons.LOCAL_HOSPITAL,
                ),
                ft.ElevatedButton(
                    text="Admin",
                    width=220,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREY},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=40),
                        elevation={"": 2, "hovered": 6},
                        text_style=ft.TextStyle(size=25)
                    ),
                    icon=ft.icons.ADMIN_PANEL_SETTINGS
                ),
                ft.ElevatedButton(
                    text="Proveedor",
                    width=220,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.BLUE_ACCENT, "hovered": ft.colors.GREY},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=40),
                        elevation={"": 2, "hovered": 6},
                        text_style=ft.TextStyle(size=25)
                    ),
                    icon=ft.icons.SHOP,
                ),
                ft.ElevatedButton(
                    text="Autoridad",
                    width=220,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREY},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=40),
                        elevation={"": 2, "hovered": 6},
                        text_style=ft.TextStyle(size=25)
                    ),
                    icon=ft.icons.SECURITY
                ),

                ft.IconButton(
                    icon=ft.icons.EXIT_TO_APP,
                    icon_color="black",
                    icon_size=30,
                    height=50,
                    width=50,
                    style=ft.ButtonStyle(
                        bgcolor={"hovered": ft.colors.GREY_300},
                    ),
                    on_click=lambda e: page.window.close(),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
            bgcolor=ft.colors.WHITE,
            height=650,
            width=450,
            border_radius=20,
        ),
        border_radius=20
    )

    contenedor3 = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src=FONDO,
            fit=ft.ImageFit.COVER,
        ),
        content=background_container,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.add(contenedor3)
    page.update()

if __name__ == '__main__':
        ft.app(target=main)
