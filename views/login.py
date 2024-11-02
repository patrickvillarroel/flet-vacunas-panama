import datetime
import logging
from typing import List

import flet as ft
from pydantic import ValidationError

import ApiManager
from validations.AccountDto import UsuarioDto, RolDto
from validations.DireccionesDto import DistritoDto, ProvinciaDto
from validations.PacienteDto import PacienteDto
from views.controles import contenedor

logger = logging.getLogger(__name__)


# Iniciar sesión
def sign_in(page: ft.Page) -> ft.View:
    async def login_pass(username: str, password: str):
        if username and not username.isspace() and password and not password.isspace():
            response = await ApiManager.login_paciente(username, password)
            logger.debug(f"Respuesta del servidor: {response}")

            if "error" not in response:
                page.session.set("access_token", response.get("access_token"))
                page.session.set("refresh_token", response.get("refresh_token"))
                paciente_json = response.get("paciente")

                # TODO mapear basado en el rol recibido
                if paciente_json:
                    logger.debug(f"Paciente encontrado: {paciente_json}")
                    paciente_log = PacienteDto(**paciente_json)
                    # Llamar a la función `paciente` solo si hay información válida
                    # await pacientes(page, response)
                else:
                    logger.warning("No se encontró información del paciente")
                    page.overlay.append(ft.AlertDialog(content=ft.Text(value="No es un paciente"), open=True))
            else:
                page.overlay.append(
                    ft.AlertDialog(content=ft.Text(value="Revise su contraseña y usuario"), open=True))
            logger.exception("Error durante el login")
            # page.overlay.append(ft.AlertDialog(content=ft.Text(value="Error de conexión o de servidor"), open=True))

        else:
            page.overlay.append(ft.AlertDialog(content=ft.Text(value="Usuario y contraseña son requeridos"), open=True))

        # Asegúrate de actualizar la página
        page.update()

    async def handle_login(e):
        await login_pass(user.value, password.value)

    user = ft.TextField(
        width=300,
        height=40,
        hint_text='Cédula/Pasaporte/Correo/Usuario',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    password = ft.TextField(
        width=300,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK,
        border=ft.InputBorder.UNDERLINE,
        password=True,
        can_reveal_password=True,
    )

    control = contenedor()

    control.content = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Container(
                            ft.Image(
                                src="/images/icon.png",
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
                            color=ft.colors.WHITE
                        ),
                        ft.Container(
                            user,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            password,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                content=ft.Text(
                                    'INICIAR',
                                    color=ft.colors.BLUE,
                                    weight=ft.FontWeight.W_500,
                                ),
                                width=200,
                                bgcolor='white',
                                on_click=handle_login
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.Row([
                                ft.Text('¿No tiene una cuenta?'),
                                ft.TextButton('Crear una cuenta',
                                              on_click=lambda _: page.go("/register"),
                                              ),
                            ], spacing=8),
                            padding=ft.padding.only(24),
                        ),
                        ft.Container(
                            ft.Row([
                                ft.TextButton('Regresar a la pagina principal',
                                              on_click=lambda _: page.go("/")),
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

    return ft.View(
        route="/login-in",
        controls=[ft.SafeArea(
            expand=True,
            content=control,
        )]
    )


# Registrarse basado en el rol
def sign_up(page: ft.Page) -> ft.View:
    provincias: List[ProvinciaDto] = []
    distritos: List[DistritoDto] = []

    if not page.session.contains_key("rol"):
        page.overlay.append(ft.AlertDialog(content=ft.Text(value="No se ha podido determinar su rol"),
                                           open=True,
                                           on_dismiss=page.go("/")))

    async def obtener_provincias_y_distritos():
        provincias = await ApiManager.get_provincias()
        distritos = await ApiManager.get_distritos()
        return provincias, distritos

    def filtrar_distritos_por_provincia(distritos: List[DistritoDto], provincia_id: int):
        return [d for d in distritos if d.provincia.id == provincia_id]

    async def obtener_prov_dist():
        nonlocal provincias, distritos
        provincias, distritos = await obtener_provincias_y_distritos()

    page.run_task(obtener_prov_dist)

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
        try:
            rol = page.session.get("rol")
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
                    roles={RolDto(id=rol.value)}
                )
            )
            return paciente_dto
        except ValidationError as e:
            logger.error(e)
            return

    async def register_session(e):
        paciente_dto = armar_dto_paciente(validar_datos())
        if not paciente_dto:
            return
        data = await ApiManager.register_paciente(paciente_dto)
        if data:
            logger.info(data)
            page.overlay.append(ft.AlertDialog(content=ft.Text(value="Registrado exitoso"), open=True))
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
        label="Provincia",
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
                         label_style=ft.TextStyle(color=ft.colors.BLACK, size=15, weight=ft.FontWeight.BOLD),
                         read_only=True, hint_text="DD/MM/AAAA")

    pasaporte = ft.TextField(label="Pasaporte *", width=270, color=ft.colors.BLACK,
                             label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    cedula = ft.TextField(label="Cedula *", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    password = ft.TextField(label="Contraseña *", width=270, color=ft.colors.BLACK,
                            label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD), password=True,
                            can_reveal_password=True)

    direccion = ft.TextField(label="Dirección Exacta", width=270, color=ft.colors.BLACK,
                             label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    correo = ft.TextField(label="Corro Electronico", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    telefono = ft.TextField(label="Num.Telefono", width=270, color=ft.colors.BLACK,
                            label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD),
                            hint_text="+50700000000")

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
                scroll=ft.ScrollMode.ALWAYS,
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
                    on_click=register_session,
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
                    on_click=lambda _: page.go("/"),
                )
            ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        ],
        scroll=ft.ScrollMode.ALWAYS
    )

    header = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text("Vacunas APP", weight=ft.FontWeight.BOLD, size=40,
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

    contenido = contenedor()
    contenido.content = ft.Column(
        controls=[ft.Row(controls=[header],
                         alignment=ft.MainAxisAlignment.CENTER),
                  ft.ResponsiveRow(controls=[reg_container],
                                   alignment=ft.MainAxisAlignment.CENTER)],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def actualizar_distritos(provincia_id):
        distritos_filtrados = filtrar_distritos_por_provincia(distritos, int(provincia_id))
        dropdown_distrito.options = [ft.dropdown.Option(text=d.nombre, key=str(d.id)) for d in distritos_filtrados]
        dropdown_distrito.value = 0
        page.update()

    return ft.View(
        route="/register",
        scroll=ft.ScrollMode.HIDDEN,
        controls=[ft.SafeArea(
            expand=True,
            content=contenido,
        )]
    )
