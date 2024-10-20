import asyncio
import datetime
import logging
from typing import List

import flet as ft
from pydantic import ValidationError

import ApiManager
from util import RolesEnum
from validations.AccountDto import UsuarioDto, RolDto
from validations.DireccionesDto import DistritoDto
from validations.PacienteDto import PacienteDto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales
FONDO = "assets/images/fondo2.jpg"
LOGO = "assets/images/logo.png"
global_tipo: RolesEnum.Roles
TITULO = "Vacunas APP"


# Funciones globales
async def obtener_provincias_y_distritos():
    provincias = await ApiManager.get_provincias()
    distritos = await ApiManager.get_distritos()  # Devuelve todos los distritos
    return provincias, distritos


def filtrar_distritos_por_provincia(distritos: List[DistritoDto], provincia_id: int):
    return [d for d in distritos if d.provincia.id == provincia_id]


def show_error_message(page: ft.Page, message):
    error_dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(message),
        open=True,
        on_dismiss=lambda e: logger.info("error dialog dismissed"),
    )
    page.overlay.append(error_dialog)
    page.update()


async def formulario(page: ft.Page):
    page.title = 'Paciente'
    page.window.width = 900
    page.window.height = 650
    page.bgcolor = ft.colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.resizable = False
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.decoration = ft.BoxDecoration(image=ft.DecorationImage(
        src="assets/images/fondo2.jpg",
        fit=ft.ImageFit.COVER,
    ))

    provincias, distritos = await obtener_provincias_y_distritos()

    def validar_datos():
        nombre1 = nombre.value if nombre.value and not nombre.value.isspace() else None
        nombre2 = segundo_nombre.value if segundo_nombre.value and not segundo_nombre.value.isspace() else None
        apellido1 = apellido.value if apellido.value and not apellido.value.isspace() else None
        apellido2 = segundo_apellido.value if segundo_apellido.value and not segundo_apellido.value.isspace() else None
        if fecha.value:
            # Primero convierte el formato de texto a datetime
            fecha_datetime = datetime.datetime.strptime(fecha.value, "%d-%m-%Y")

            # Luego lo formateas al formato que espera Java (ISO 8601)
            fecha_nacimiento_valid = fecha_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            fecha_nacimiento_valid = None
        pasaporte_valid = pasaporte.value if pasaporte.value and not pasaporte.value.isspace() else None
        cedula_valid = cedula.value if cedula.value and not cedula.value.isspace() else None
        correo_valid = correo.value if correo.value and not correo.value.isspace() else None
        telefono_valid = telefono.value if telefono.value and not telefono.value.isspace() else None
        username_valid = usuario.value if usuario.value and not usuario.value.isspace() else None
        password_valid = password.value if password.value and not password.value.isspace() else None
        sexo_valid = sexo.value if sexo.value and not sexo.value.isspace() else None

        return {
            "nombre1": nombre1,
            "nombre2": nombre2,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "fecha_nacimiento": fecha_nacimiento_valid,
            "pasaporteValid": pasaporte_valid,
            "cedulaValid": cedula_valid,
            "correoValid": correo_valid,
            "telefonoValid": telefono_valid,
            "usernameValid": username_valid,
            "passwordValid": password_valid,
            "sexoValid": sexo_valid
        }

    def armar_dto_paciente(datos_validados):
        global global_tipo
        try:
            # Crear el DTO del paciente con los valores validados
            paciente_dto = PacienteDto(
                nombre=datos_validados["nombre1"],
                nombre2=datos_validados["nombre2"],
                apellido1=datos_validados["apellido1"],
                apellido2=datos_validados["apellido2"],
                fecha_nacimiento=datos_validados["fecha_nacimiento"],
                pasaporte=datos_validados["pasaporteValid"],
                cedula=datos_validados["cedulaValid"],
                correo=datos_validados["correoValid"],
                telefono=datos_validados["telefonoValid"],
                sexo=datos_validados["sexoValid"],
                estado="ACTIVO",  # Datos fijos para demo
                disabled=False,
                usuario=UsuarioDto(
                    username=datos_validados["usernameValid"],
                    password=datos_validados["passwordValid"],
                    roles={RolDto(id=global_tipo.value)}
                )
            )
            return paciente_dto
        except ValidationError as e:
            logger.error(e)
            return

    async def register_session():
        paciente_dto = armar_dto_paciente(validar_datos())
        if not paciente_dto:
            return
        data = await ApiManager.register_paciente(paciente_dto)
        if data:
            logger.info(data)
            await paciente(page, data)
        else:
            page.overlay.append(ft.AlertDialog(content=ft.Text(value="Error recibido"), open=True))
            logger.error("No hay data obtenida")

    sexo = ft.RadioGroup(
        value=None,
        content=ft.Row([
            ft.Radio(
                value="M",
                label="M",
                fill_color=ft.colors.BLUE,
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,
                )
            ),
            ft.Radio(
                value="F",
                label="F",
                fill_color=ft.colors.BLUE,
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,
                )
            ),
            ft.Radio(
                value="X",
                label="Otro",
                fill_color=ft.colors.BLUE,
                label_style=ft.TextStyle(
                    color=ft.colors.BLACK,
                )
            )
        ],
            spacing=3
        )
    )

    dropdown_provincia = ft.Dropdown(
        label="Provincia",  # Etiqueta personalizada
        icon_enabled_color=ft.colors.BLACK,
        options=[ft.dropdown.Option(text=prov.nombre, key=str(prov.id)) for prov in provincias],
        on_change=lambda e: actualizar_distritos(e.control.value),
        value=str(0),
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

    )

    dropdown_distrito = ft.Dropdown(
        label="Dristito",  # Etiqueta personalizada
        icon_enabled_color=ft.colors.BLACK,
        options=[],
        value=str(0),
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

    )

    nombre = ft.TextField(label="Nombre *", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    segundo_nombre = ft.TextField(label="Segundo Nombre", width=270, color=ft.colors.BLACK,
                                  label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    apellido = ft.TextField(label="Apellido *", width=270, color=ft.colors.BLACK,
                            label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    segundo_apellido = ft.TextField(label="Segundo Apellido", width=270, color=ft.colors.BLACK,
                                    label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    fecha = ft.TextField(label="Fecha de Nacimiento *", width=210, color=ft.colors.BLACK,
                         label_style=ft.TextStyle(color=ft.colors.BLACK, size=15, weight=ft.FontWeight.BOLD))

    pasaporte = ft.TextField(label="Pasaporte *", width=270, color=ft.colors.BLACK,
                             label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    cedula = ft.TextField(label="Cedula *", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    password = ft.TextField(label="Contraseña *", width=270, color=ft.colors.BLACK,
                            label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    direccion = ft.TextField(label="Dirección Exacta", width=270, color=ft.colors.BLACK,
                             label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    correo = ft.TextField(label="Corro Electronico", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    telefono = ft.TextField(label="Num.Telefono", width=270, color=ft.colors.BLACK,
                            label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    usuario = ft.TextField(label="Nombre de Usuario", width=270, color=ft.colors.BLACK,
                           label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    def handle_change(e):
        fecha.value = e.control.value.strftime('%d-%m-%Y')
        # Formato para enviar '%d-%m-%YT%T'
        page.update()

    def handle_dismissal(e):
        print("Necesito una fecha")

    registro = ft.Column(
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
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=
                                [
                                    nombre,
                                    segundo_nombre,
                                    apellido,
                                    segundo_apellido,
                                    ft.Row(controls=[
                                        fecha,
                                        ft.IconButton(
                                            icon=ft.icons.CALENDAR_MONTH,
                                            width=50,
                                            bgcolor="blue",
                                            on_click=lambda e: page.open(
                                                ft.DatePicker(
                                                    first_date=datetime.datetime(
                                                        year=1900,
                                                        month=1,
                                                        day=1),
                                                    last_date=datetime.datetime.today(),
                                                    on_change=handle_change,
                                                    on_dismiss=handle_dismissal,
                                                ),
                                            ),
                                        ),
                                    ]),
                                    cedula,
                                    pasaporte,
                                    telefono,
                                    correo,
                                    ft.Row(),
                                    ft.Row(controls=[
                                        ft.Text("Sexo: ", size=15,
                                                weight=ft.FontWeight.BOLD,
                                                color="black"), sexo],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    dropdown_provincia,
                                    dropdown_distrito,
                                    direccion,
                                    usuario,
                                    password,

                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll=ft.ScrollMode.ALWAYS
                            ),

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,

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
                    on_click=lambda e: asyncio.run(register_session()),
                ),
                ft.ElevatedButton(
                    "Salir",
                    width=100,
                    height=40,
                    style=ft.ButtonStyle(
                        color={ft.ControlState.DEFAULT: ft.colors.WHITE,
                               ft.ControlState.HOVERED: ft.colors.WHITE},

                        bgcolor={ft.ControlState.DEFAULT: ft.colors.GREY,
                                 ft.ControlState.HOVERED: ft.colors.RED},

                        shape=ft.RoundedRectangleBorder(radius=25),
                        elevation={"pressed": 10, "default": 2},
                        animation_duration=300,
                    ),
                    icon=ft.icons.EXIT_TO_APP,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda e: main(page),
                )
            ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        ],
        scroll=ft.ScrollMode.ALWAYS
    )
    page.clean()

    header = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(TITULO, weight=ft.FontWeight.BOLD, size=40,
                                color=ft.colors.BLACK),
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
            ]
        ),
        width=300
    )

    reg_container = ft.Container(
        content=registro,
        border=ft.border.all(4, "white"),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        col={"sm": 4, "md": 4, "xl": 4},
    )

    final_container = ft.Container(
        expand=True,
        content=ft.Column(controls=[ft.Row(controls=[header], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.ResponsiveRow(controls=[reg_container], alignment=ft.MainAxisAlignment.CENTER)],
                          alignment=ft.MainAxisAlignment.CENTER),
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


# ______________________________________________________________________________________________________________________

async def paciente(page: ft.page, data: dict):
    page.title = 'Paciente'
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
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

    paciente = PacienteDto(**data.get("paciente"))
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    if access_token and refresh_token:
        # page.overlay.append(ft.AlertDialog(content=ft.Text(value="Exito al registrar"), open=True))
        logger.debug("Tokens obtenidos del registro paciente")
        page.session.set("access_token", access_token)
        page.session.set("refresh_token", refresh_token)
    else:
        # page.overlay.append(ft.AlertDialog(content=ft.Text(value="Exitoso, pero sin tokens"), open=True))
        logger.error("Los tokens no fueron obtenidos")

    ced = ft.TextField(
        width=300,
        height=50,
        hint_style=ft.TextStyle(color='black'),
        hint_text='Cedula del paciente a buscar',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
        color=ft.colors.BLACK,
        max_length=12,
    )

    def cambio_vacunas():
        result_container.controls.clear()
        result_container.controls.append(menu_vacunas)
        page.update()

    def cambio_info():
        result_container.controls.clear()
        result_container.controls.append(menu_usuario)
        page.update()

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

    menu_vacunas = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Text(TITULO, weight=ft.FontWeight.BOLD, size=50, color=ft.colors.BLACK),
                        ft.Text(value="Bienvenido " + paciente.nombre, color=ft.colors.BLACK),
                        ft.Text("Tabla de Datos (En proceso)", weight=ft.FontWeight.BOLD, size=100, color=ft.colors.RED)
                    ]
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.all(0),
                bgcolor=ft.colors.WHITE,
                height=700,
                width=1000,
            )
        ],

    )

    menu_usuario = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(TITULO, weight=ft.FontWeight.BOLD, size=50, color=ft.colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            width=850,
                        ),
                        ft.Row(
                            [
                                ft.Column(  # Primera columna
                                    [ft.Container(
                                        ft.Column(
                                            controls=[ft.Row([ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                                                              ft.Text("Datos del Usuario", weight=ft.FontWeight.BOLD,
                                                                      size=15, color=ft.colors.BLACK)]),
                                                      ft.Divider(height=5, color=ft.colors.BLACK),
                                                      ft.TextField(label="Nombre", value="Prueba", width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Apellido", value="Python", width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Cedula", value="1", width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Usuario", value="Pythoner", width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Correo", value="prueba.py@gmail.com",
                                                                   width=350, color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Numero de Telefono", value="6574-3435",
                                                                   width=350, color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
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
                                                                  icon=ft.icons.UPDATE,
                                                                  # Icono a la izquierda del texto
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
                                ft.Column(  # Segunda columna
                                    [ft.Container(ft.Column(controls=[
                                        ft.Container(
                                            ft.Image(src="assets/images/LogoVacuna.png", width=400, height=400),
                                            alignment=ft.alignment.center),
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
            cambio_info()
        elif selected_index == 1:
            cambio_vacunas()
        elif selected_index == 2:
            show_message()
        elif selected_index == 3:
            main(page)

    result_container = ft.Row(
        [
            menu_usuario
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
        image=ft.DecorationImage(
            src=FONDO,
            fit=ft.ImageFit.COVER,
        ),
        content=pac_container,
        alignment=ft.alignment.center,
        margin=-10,
    )

    page.clean()

    page.add(
        final_container,
    )
    page.update()


# _______________________________________________________________________________________________________________________
async def login(page: ft.Page):
    page.title = 'VacunAPP'
    page.window.width = 900
    page.window.height = 500
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.adaptive = True

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
                                ft.TextButton('Crear una cuenta', on_click=lambda e: asyncio.run(formulario(page))),
                            ], spacing=8),
                            padding=ft.padding.only(24),
                        ),
                        ft.Container(
                            ft.Row([
                                ft.TextButton('Regresar a la pagina principal',
                                              on_click=lambda e: main(page)),
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
    page.bgcolor = ft.colors.WHITE
    page.navigation_bar = False

    def button_click(e: ft.Page, t: RolesEnum.Roles):
        global global_tipo
        asyncio.run(login(e))
        global_tipo = t

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
                    on_click=lambda e: button_click(page, RolesEnum.Roles.PACIENTE),
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
                    on_click=lambda e: button_click(page, RolesEnum.Roles.DOCTOR),
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
