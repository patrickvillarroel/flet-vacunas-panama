import flet as ft
from flet import *
#from Connection import *

global_tipo = 0
#def conn():
   # conexion()
def acoount(page: Page):
    page.title = 'VacunAPP'
    page.window_width = 900
    page.window_height = 500
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

    def insertDato(nom, us, pas, typ, page):
        #result = conexionU(us, pas, typ)
        print(result)
        if result != "None":
            insertP(nom, us, pas, typ)
            log(page)
        else:
            show_error_message("Usuario ya existente")

    nombre = ft.TextField(
        width=200,
        height=40,
        hint_text='Cedula (e-eeee-eeee)',
        border='underline',
        prefix_icon=ft.icons.PERSON,
    )

    user = ft.TextField(
        width=200,
        height=40,
        hint_text='Usuario',
        border='underline',
        prefix_icon=ft.icons.PERSON,
    )

    password = ft.TextField(
        width=200,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK,
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
        on_click=lambda e: insertDato(nombre.value, user.value, password.value, 1, page),
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
                        ft.Text(
                            'REGISTRARSE',
                            width=400,
                            size=30,
                            weight='w900',
                            text_align='center',
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
        image_src="fondo2.jpg",
        image_fit=ft.ImageFit.COVER,
        content=body,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.controls.append(contenedor)
    page.update()

#______________________________________________________________________________________________________________________
def pac(page: Page):
    page.title = 'VacunAPP'
    page.window_width = 1300
    page.window_height = 700
    page.bgcolor = ft.colors.BLACK
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_resizable = False

    result_container = ft.Column(
        alignment=ft.alignment.center
    )

    ced = ft.TextField(
        width=300,
        height=50,
        hint_style=ft.TextStyle(color='black'),
        hint_text='Cedula del paciente a buscar',
        border='underline',
        prefix_icon=ft.icons.PERSON,
        color=ft.colors.BLACK,
        max_length=12,
    )

    def fetch_data(cedula):
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute(f"select * from vwPaciente where Cedula = '{cedula}'")
        data = cursor.fetchall()
        conn.close()
        return data

    def search_user():
        ced_value = ced.value
        data = fetch_data(ced_value)
        table = build_table(data)
        result_container.controls.clear()
        result_container.controls.append(table)
        page.update()

    def show_message():
        error_dialog = ft.AlertDialog(
            title=ft.Text("Contactos"),
            content=ft.Text("Ministerio de Salud (512-9100)" + "\n" +
                            "Caja del Seguro Social (199)"),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ],
        )
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

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

    body2 = ft.Row([
        ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        height=15
                    ),
                    ft.Row(controls=[ft.Text("User Information", size=30, weight="bold", text_align=ft.alignment.top_center, color="blue")],
                    alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),

                    ft.Row([ced, ft.ElevatedButton("Buscar", width=120, height=50, on_click=lambda e: search_user())],
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
                                            src='icon1.png',
                                            width=100,
                                            height=100

                                        ),
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text(
                                        'Bienvenido',
                                        width=200,
                                        size=30,
                                        weight='w300',
                                        text_align='center',
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
                                        ft.ElevatedButton(content=ft.Text("Menu de inicio", color=ft.colors.BLUE), width=170, height=40, bgcolor='white', on_click=lambda e: main(page)),
                                    ),
                                    ft.Container(
                                        ft.ElevatedButton(content=ft.Text("Contactanos", color=ft.colors.BLUE), width=170, height=40, bgcolor='white', on_click=lambda e: show_message()),
                                    ),
                                ]
                            )
                        ],
                    ),
                    ft.Row(

                    ),
                    ft.Row(

                    ),

                    ft.Row(
                        height=100
                    ),

                    ft.Row(

                    ),
                    ft.Row(

                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.colors.BLUE,
            height=700,


        )
    ])


    def clear_entry():
        ced.value = " "
        page.update()

    page.clean()

    page.add(ft.Row([
        body3,
        body2
    ]))
    page.update()



#_______________________________________________________________________________________________________________________
def log(page: Page):
    page.title = 'VacunAPP'
    page.window_width = 900
    page.window_height = 500
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

    def validarDato(us, pas, typ, pag):
        #result = conexionU(us, pas, typ)
        print(result)
        if result != "None":
            show_error_message("No se encontró ningún usuario con el nombre de usuario: " + us)
        else:
            pac(page)


    user = ft.TextField(
        width=200,
        height=40,
        hint_text='Usuario',
        border='underline',
        prefix_icon=ft.icons.PERSON,
    )

    password = ft.TextField(
        width=200,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK,
        border='underline',
        color='black',
        password=True,
        can_reveal_password=True
    )

    go = ft.ElevatedButton(
        content=ft.Text(
            'INICIAR',
            color='blue',
            weight='w500',
        ),
        on_click=lambda e: validarDato(user.value, password.value, global_tipo, page),
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
                        ft.Text(
                            'Iniciar sesión',
                            width=400,
                            size=30,
                            weight='w900',
                            text_align='center',
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
                                ft.Text('¿No tiene una cuenta?'),
                                ft.TextButton('Crear una cuenta', on_click=lambda e: acoount(page)),
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
        image_src="fondo2.jpg",
        image_fit=ft.ImageFit.COVER,
        content=body,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.controls.append(contenedor)
    page.update()

#----------------------------------------------------------------------------------------------------------------------------------------------------
#App principal
def main(page: Page):

    Page.title = 'VacunAPP'
    Page.vertical_alignment = ft.MainAxisAlignment.CENTER
    Page.bgcolor=ft.colors.WHITE
    Page.window_width=900
    Page.window_height=500

    def button_click(e, t):
        global global_tipo
        log(e)
        global_tipo = t

    background_container = ft.Container(
        expand=True,
        width=280,
        height=440,
        bgcolor=ft.colors.LIGHT_BLUE,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Image(src="Icon1.png", width=100, height=100),
                ft.ElevatedButton(
                    text="Paciente",
                    on_click=lambda e: button_click(page, 1),
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=20),
                        elevation={"": 2, "hovered": 6}
                    ),
                    icon=ft.icons.PERSON,
                ),
                ft.ElevatedButton(
                    text="Doctor",
                    on_click=lambda e: button_click(page, 2),
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.BLUE_ACCENT, "hovered": ft.colors.BLUE},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=20),
                        elevation={"": 2, "hovered": 6}
                    ),
                    icon=ft.icons.LOCAL_HOSPITAL,
                ),
                ft.ElevatedButton(
                    text="Admin",
                    # on_click=conn_on_click,
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=20),
                        elevation={"": 2, "hovered": 6}
                    ),
                    icon=ft.icons.ADMIN_PANEL_SETTINGS
                ),
                ft.ElevatedButton(
                    text="Proveedor",
                    # on_click=conn_on_click,
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.BLUE_ACCENT, "hovered": ft.colors.BLUE},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=20),
                        elevation={"": 2, "hovered": 6}
                    ),
                    icon=ft.icons.SHOP,
                ),
                ft.ElevatedButton(
                    text="Autoridad",
                    # on_click=conn_on_click,
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
                        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
                        shape=ft.RoundedRectangleBorder(radius=20),
                        elevation={"": 2, "hovered": 6}
                    ),
                    icon=ft.icons.SECURITY
                ),

                ft.ElevatedButton(
                    bgcolor=ft.colors.WHITE,
                    width=30,
                    height=30,
                    content=ft.Image(src="salidaIcon.png", width=23, height=23),
                    ##on_click=closeApp
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        border_radius=20
    )

    contenedor3 = ft.Container(
        expand=True,
        image_src="fondo2.jpg",
        image_fit=ft.ImageFit.COVER,
        content=background_container,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.add(contenedor3)7
    page.update()

if __name__ == '__main__':
        ft.app(target=main)
