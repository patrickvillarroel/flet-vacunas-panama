import flet as ft
import datetime

from pydantic import ValidationError

import ApiManager
from typing import List

from validations.AccountDto import RolDto, UsuarioDto
from validations.DireccionesDto import ProvinciaDto, DistritoDto
from validations.PacienteDto import PacienteDto


async def obtener_provincias_y_distritos():
    provincias = await ApiManager.get_provincias()
    distritos = await ApiManager.get_distritos()  # Devuelve todos los distritos
    return provincias, distritos


def filtrar_distritos_por_provincia(distritos: List[DistritoDto], provincia_id: int):
    return [d for d in distritos if d.provincia.id == provincia_id]


async def formulario(page: ft.Page):
    page.title = 'Formulario de registros'
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

    async def handle_regs():
        await validaciones(nombre.value, segundo_nombre.value,)

    def validar_datos(nombre, segundo_nombre, apellido, segundo_apellido, fecha, pasaporte, cedula, correo, telefono,
                      usuario, password, sexo):
        # Validación de campos para evitar valores vacíos o solo espacios
        nombre1 = nombre.value if nombre.value and not nombre.value.isspace() else None
        nombre2 = segundo_nombre.value if segundo_nombre.value and not segundo_nombre.value.isspace() else None
        apellido1 = apellido.value if apellido.value and not apellido.value.isspace() else None
        apellido2 = segundo_apellido.value if segundo_apellido.value and not segundo_apellido.value.isspace() else None
        fecha_nacimientoValid = fecha.value.format('%d-%m-%YT%T') if fecha.value else None
        pasaporteValid = pasaporte.value if pasaporte.value and not pasaporte.value.isspace() else None
        cedulaValid = cedula.value if cedula.value and not cedula.value.isspace() else None
        correoValid = correo.value if correo.value and not correo.value.isspace() else None
        telefonoValid = telefono.value if telefono.value and not telefono.value.isspace() else None
        usernameValid = usuario.value if usuario.value and not usuario.value.isspace() else None
        passwordValid = password.value if password.value and not password.value.isspace() else None
        sexoValid = sexo.value if sexo.value and not sexo.value.isspace() else None

        return {
            "nombre1": nombre1,
            "nombre2": nombre2,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "fecha_nacimiento": fecha_nacimientoValid,
            "pasaporteValid": pasaporteValid,
            "cedulaValid": cedulaValid,
            "correoValid": correoValid,
            "telefonoValid": telefonoValid,
            "usernameValid": usernameValid,
            "passwordValid": passwordValid,
            "sexoValid": sexoValid
        }

    def armar_dto_paciente(datos_validados):
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
                sexo=datos_validados["sexoValid"],  # Aquí asumí que el valor de sexo es fijo
                estado="ACTIVO",  # Aquí también el estado es fijo
                disabled=False,  # Fijo
                usuario=UsuarioDto(
                    username=datos_validados["usernameValid"],
                    password=datos_validados["passwordValid"],
                    roles={RolDto(id=1)}  # Aquí asumo que solo asignas un rol con ID 1
                )
            )
        except ValidationError as e:
            logger.error(e)
            return

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

    usuario = ft.TextField(label="Nombre de Usuario", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    correo = ft.TextField(label="Corro Electronico", width=270, color=ft.colors.BLACK,
                          label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))

    telefono = ft.TextField(label="Num.Telefono", width=270, color=ft.colors.BLACK,
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
                                    password

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
                    on_click=lambda e: print("Usuario Registrado!"),
                ),
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


ft.app(target=formulario)
