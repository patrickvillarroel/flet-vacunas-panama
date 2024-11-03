import datetime
import logging
from typing import List

import flet as ft
from pydantic import ValidationError

import ApiManager
from validations.AccountDto import UsuarioDto, RolDto
from validations.DireccionesDto import DistritoDto, ProvinciaDto, DireccionDto
from validations.PacienteDto import PacienteDto
from views.controles import contenedor

logger = logging.getLogger(__name__)


# Iniciar sesión TODO redirigir a un dashboard construido de forma dinámica
def sign_in(page: ft.Page) -> ft.View:
    async def login_pass(username: str, password: str):
        if username and not username.isspace() and password and not password.isspace():
            response = await ApiManager.login(username=username, password=password)
            logger.debug(f"Respuesta del servidor: {response}")

            if "error" not in response:
                page.session.set("access_token", response.get("access_token"))
                page.session.set("refresh_token", response.get("refresh_token"))
                # Redirigir a su dashboard con la información ya guardada
                if response.get("paciente", None):
                    page.session.set("paciente", response.get("paciente"))
                    page.go("/paciente")
                else:
                    page.overlay.append(ft.AlertDialog(content=ft.Text("Rol no soportado. Lo sentimos"), open=True))
            else:
                logger.error("Error durante el login")
                error = response.get("error")
                if isinstance(error, ValidationError):
                    page.overlay.append(
                        ft.AlertDialog(content=ft.Text("Validación fallida. Intente nuevamente"), open=True))
                elif isinstance(error, Exception):
                    page.overlay.append(
                        ft.AlertDialog(content=ft.Text("Error de conexión o de servidor"), open=True))
                else:
                    page.overlay.append(
                        ft.AlertDialog(content=ft.Text("Revise su contraseña y usuario"), open=True))
        else:
            page.overlay.append(ft.AlertDialog(content=ft.Text("Usuario y contraseña son requeridos"), open=True))
        page.update()

    async def handle_login(e):
        await login_pass(user_field.value, password_field.value)

    user_field = ft.TextField(
        width=300,
        height=40,
        color=ft.colors.BLACK,
        max_length=50,
        autofocus=True,
        hint_text='Cédula/Pasaporte/Correo/Usuario',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    password_field = ft.TextField(
        width=300,
        height=40,
        max_length=70,
        color=ft.colors.BLACK,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK,
        border=ft.InputBorder.UNDERLINE,
        password=True,
        can_reveal_password=True,
    )

    control = contenedor()

    control.content = ft.Container(
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    gradient=ft.LinearGradient(begin=ft.alignment.top_center,
                                               end=ft.alignment.bottom_center,
                                               colors=[ft.colors.BLUE_300, ft.colors.BLUE_200]),
                    width=320,
                    height=460,
                    border_radius=20,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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
                                user_field,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                password_field,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        'INICIAR',
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    width=200,
                                    bgcolor='#0056b3',
                                    on_click=handle_login
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                ft.Row([
                                    ft.Text('¿No tiene una cuenta?'),
                                    ft.FilledTonalButton('Crear una cuenta',
                                                         width=158,
                                                         on_click=lambda _: page.go("/register"),
                                                         ),
                                ], ),
                                padding=ft.padding.only(10),
                            ),
                            ft.Container(
                                ft.Row([
                                    ft.FilledTonalButton('Regresar a la pagina principal',
                                                         on_click=lambda _: page.go("/")),
                                ], ),
                                padding=ft.padding.symmetric(-10, 40),
                                alignment=ft.alignment.center
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    return ft.View(
        route="/login",
        controls=[ft.SafeArea(
            expand=True,
            content=control,
        )]
    )


# Registrarse TODO basado en el rol
def sign_up(page: ft.Page) -> ft.View:
    provincias: List[ProvinciaDto] = []
    distritos: List[DistritoDto] = []

    if not page.session.contains_key("rol"):
        page.overlay.append(
            ft.AlertDialog(content=ft.Text("No se ha podido determinar su rol. Intente nuevamente"),
                           open=True,
                           on_dismiss=lambda _: page.go("/")))
        page.update()

    def filtrar_distritos_por_provincia(provincia_id: int):
        return [d for d in distritos if d.provincia.id == provincia_id]

    def actualizar_distritos(provincia_id):
        distritos_filtrados = filtrar_distritos_por_provincia(int(provincia_id))
        dropdown_distrito.options = [ft.dropdown.Option(text=d.nombre, key=str(d.id)) for d in distritos_filtrados]
        dropdown_distrito.value = 0
        page.update()

    async def obtener_prov_dist():
        nonlocal provincias, distritos
        provincias = await ApiManager.get_provincias()
        distritos = await ApiManager.get_distritos()
        dropdown_provincia.options = [ft.dropdown.Option(text=prov.nombre, key=str(prov.id)) for prov in provincias]
        page.update()

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
        direccion_valid = direccion.value if direccion.value and not direccion.value.isspace() else None
        distrito_valid = dropdown_distrito.value if dropdown_distrito.value != 0 else None

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
            "sexoValid": sexo_valid,
            "direccionValid": direccion_valid,
            "distritosValid": distrito_valid,
        }

    def armar_dto_paciente(datos_validados: dict):
        try:
            rol = page.session.get("rol")
            direccion_dto = DireccionDto(
                direccion=datos_validados["direccionValid"],
                distritos=DistritoDto(id=datos_validados["distritosValid"])
            ) if datos_validados["direccionValid"] is not None else None
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
                disabled=False,  # Datos fijos para demo
                usuario=UsuarioDto(
                    username=datos_validados["usernameValid"],
                    password=datos_validados["passwordValid"],
                    roles={RolDto(id=rol.value)}
                ),
                direccion=direccion_dto
            )
            return paciente_dto
        except ValidationError as e:
            logger.error(e)
            return None

    async def register_handler(e):
        paciente_dto = armar_dto_paciente(validar_datos())
        if paciente_dto is None:
            page.overlay.append(
                ft.AlertDialog(content=ft.Text("Validación fallida. Revise los datos"), open=True))
            page.update()
            return
        data = await ApiManager.register_paciente(paciente_dto)
        if "error" not in data:
            logger.info(data)
            page.overlay.append(ft.AlertDialog(content=ft.Text("Registrado exitoso"), open=True,
                                               on_dismiss=lambda _: page.go("/login"), ))
            page.update()
        else:
            mensaje = data.get("message", "Error")
            page.overlay.append(ft.AlertDialog(content=ft.Text(mensaje), open=True))
            page.update()

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
        label="Distrito",
        icon_enabled_color=ft.colors.BLACK,
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
                         read_only=True, hint_text="DD-MM-AAAA")

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
        logger.info("Calendario dismissed. Necesito una fecha xd")

    registro = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
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
                                            on_click=lambda _: page.open(
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
                                        ft.Text("Sexo * : ", size=15,
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
                            ),

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
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
                    on_click=register_handler,
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
        col={"sm": 3.5, "md": 3.5, "xl": 3.5},
    )

    contenido = contenedor()
    contenido.margin = 0
    contenido.content = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ft.Row(controls=[header], alignment=ft.MainAxisAlignment.CENTER),
                  ft.ResponsiveRow(controls=[reg_container], alignment=ft.MainAxisAlignment.CENTER), ],
    )

    return ft.View(
        route="/register",
        scroll=ft.ScrollMode.HIDDEN,
        controls=[ft.SafeArea(
            expand=True,
            content=contenido,
        )]
    )
