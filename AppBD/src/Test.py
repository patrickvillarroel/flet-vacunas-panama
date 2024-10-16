import flet as ft
from flet import *

def paciente_test(page: Page):
    page.title = 'Paciente'
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window.width = 1000
    page.window.height = 1000
    page.theme_mode = "LIGHT"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.INFO,
                label="Mi Info"
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.COLORIZE,
                label="Mis Vacunas"
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.PHONE,
                label="Contactanos",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.EXIT_TO_APP,
                label="Salir",
            ),
        ],
        on_change=lambda e: handle_nav_change(e),
        indicator_color=ft.colors.LIGHT_BLUE_100,
        adaptive=True
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

    def CambioVacunas():
        result_container.controls.clear()
        result_container.controls.append(MenuVacunas)
        page.update()

    def CambioInfo():
        result_container.controls.clear()
        result_container.controls.append(MenuInfoUsuario)
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


    MenuVacunas = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Vacunas APP", weight="bold", size=50, color=ft.colors.BLACK),
                        ft.Text("Tabla de Datos (En proceso)", weight="bold", size=100, color=ft.colors.RED)
                    ]
                ),
                alignment = ft.alignment.center,
                margin = ft.margin.all(0),
                bgcolor = ft.colors.WHITE,
                height = 700,
                width = 1000,
            )
        ],

    )
    MenuInfoUsuario = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                      ft.Row(
                          [
                              ft.Text("Vacunas APP", weight="bold", size=50, color=ft.colors.BLACK),
                           ],
                          alignment=MainAxisAlignment.CENTER,
                          vertical_alignment=ft.CrossAxisAlignment.START,
                          width=850,
                      ),
                      ft.Row(
                          [
                              ft.Column( #Primera columna
                                  [ft.Container(
                                      ft.Column(
                                          controls=[ft.Row([ft.Icon(ft.icons.ACCOUNT_CIRCLE), ft.Text("Datos del Usuario", weight="bold", size=15, color=ft.colors.BLACK)]),
                                                    ft.Divider(height=5, color=ft.colors.BLACK),
                                                    ft.TextField(label="Nombre", value="Prueba", width=350, color=ft.colors.BLACK, read_only=True,label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                                    ft.TextField(label="Apellido", value="Python", width=350, color=ft.colors.BLACK, read_only=True,label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                                    ft.TextField(label="Cedula", value="1", width=350, color=ft.colors.BLACK, read_only=True,label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                                    ft.TextField(label="Usuario", value="Pythoner", width=350, color=ft.colors.BLACK, read_only=True,label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                                    ft.TextField(label="Correo", value="prueba.py@gmail.com", width=350, color=ft.colors.BLACK, read_only=True,label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                                    ft.TextField(label="Numero de Telefono", value="6574-3435", width=350, color=ft.colors.BLACK, read_only=True, label_style=ft.TextStyle(color='black', size=19, weight="bold")),
                                                    ft.Divider(height=5, color=ft.colors.BLACK),
                                                    ft.Row(
                                                        controls=
                                                        [
                                                            ft.ElevatedButton(
                                                                "Actualizar Información",
                                                                width=170,
                                                                height=50,
                                                                style=ft.ButtonStyle(
                                                                    color={ft.ControlState.DEFAULT: ft.colors.WHITE,
                                                                           ft.ControlState.HOVERED: ft.colors.WHITE},
                                                                    # Cambia el texto a negro cuando se pase el mouse
                                                                    bgcolor={
                                                                        ft.ControlState.DEFAULT: ft.colors.BLUE_700,
                                                                        ft.ControlState.HOVERED: ft.colors.BLUE_900},
                                                                    # Cambia el color del fondo cuando se pasa el mouse
                                                                    shape=ft.RoundedRectangleBorder(radius=25),
                                                                    # Bordes redondeados
                                                                    elevation={"pressed": 10, "default": 2},
                                                                    # Animación de elevación al presionar
                                                                    animation_duration=300,
                                                                    # Duración de la animación (en milisegundos)
                                                                ),
                                                                icon=ft.icons.UPDATE,  # Icono a la izquierda del texto
                                                                icon_color=ft.colors.WHITE,  # Color del ícono
                                                                on_click=lambda e: print("Información actualizada!")
                                                                # Acción al hacer clic
                                                            )
                                                        ],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                    )
                                                    ]
                                  ),
                                  bgcolor=ft.colors.WHITE, width=350, alignment=ft.alignment.center, height=450)],
                                  width=357,
                              ),
                              ft.Column( #Segunda columna
                                  [ft.Container(ft.Column(controls=[
                                      ft.Container(ft.Image(src='../img/LogoVacuna.png', width=400, height=400), alignment=ft.alignment.center),
                                  ]), bgcolor=ft.colors.WHITE, width=350, alignment=ft.alignment.center, height=450)],
                                  width=357,
                              ),

                          ],
                          alignment=ft.MainAxisAlignment.CENTER,
                          width=850
                      ),
                    ],
                    alignment=ft.alignment.center
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.all(0),
                bgcolor=ft.colors.WHITE,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def handle_nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            CambioInfo()
        elif selected_index == 1:
            CambioVacunas()
        elif selected_index == 2:
            show_message()

    result_container = ft.Row(
        [
            MenuInfoUsuario
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    pac_container = ft.Container(
        ft.Column(
            controls=
            [
                result_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        bgcolor=ft.colors.WHITE,
        height=580,
        width=1000,
        border_radius=30,
        alignment=ft.alignment.center,
    )

    final_container = ft.Container(
        expand=True,
        image_src="../img/fondo2.jpg",
        image_fit=ft.ImageFit.COVER,
        content=pac_container,
        alignment=ft.alignment.center,
        margin=-10,
    )

    def clear_entry():
        ced.value = " "
        page.update()

    page.clean()

    page.add(
        final_container,
    )
    page.update()


ft.app(target=paciente_test)