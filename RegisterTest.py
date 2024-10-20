import logging
from datetime import datetime

import flet as ft

import ApiManager
from validations.AccountDto import UsuarioDto, RolDto
from validations.PacienteDto import PacienteDto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE
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
    usuario = ft.TextField(label="Usuario", width=270, color=ft.colors.BLACK,
                           label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))
    password = ft.TextField(label="Contraseña *", width=270, color=ft.colors.BLACK,
                            label_style=ft.TextStyle(color='black', size=15, weight=ft.FontWeight.BOLD))
    direccion = ft.TextField(label="Dirección Exacta", width=270, color=ft.colors.BLACK,
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
        logger.info("Fecha de nacimiento picker dismissed")
        if e.control.value is None:
            fecha.border_color = ft.colors.RED

    fecha_picker = ft.DatePicker(
        first_date=datetime(
            year=1900,
            month=1,
            day=1),
        last_date=datetime.today(),
        on_change=handle_change,
        on_dismiss=handle_dismissal,
    )

    async def register():
        try:
            # Validación de campos para evitar valores vacíos o solo espacios
            nombre1 = nombre.value if nombre.value and not nombre.value.isspace() else None
            nombre2 = segundo_nombre.value if segundo_nombre.value and not segundo_nombre.value.isspace() else None
            apellido1 = apellido.value if apellido.value and not apellido.value.isspace() else None
            apellido2 = segundo_apellido.value if segundo_apellido.value and not segundo_apellido.value.isspace() else None
            fecha_nacimiento = fecha.value.format('%d-%m-%YT%T') if fecha.value else None
            pasaporteValid = pasaporte.value if pasaporte.value and not pasaporte.value.isspace() else None
            cedulaValid = cedula.value if cedula.value and not cedula.value.isspace() else None
            correoValid = correo.value if correo.value and not correo.value.isspace() else None
            telefonoValid = telefono.value if telefono.value and not telefono.value.isspace() else None
            usernameValid = usuario.value if usuario.value and not usuario.value.isspace() else None
            passwordValid = password.value if password.value and not password.value.isspace() else None

            # Crear el DTO del paciente con los valores validados
            paciente_dto = PacienteDto(
                nombre=nombre1,
                nombre2=nombre2,
                apellido1=apellido1,
                apellido2=apellido2,
                fecha_nacimiento=fecha_nacimiento,
                pasaporte=pasaporteValid,
                cedula=cedulaValid,
                correo=correoValid,
                telefono=telefonoValid,
                sexo='M',  # Aquí asumí que el valor de sexo es fijo
                estado="ACTIVO",  # Aquí también el estado es fijo
                disabled=False,  # Fijo
                usuario=UsuarioDto(
                    username=usernameValid,
                    password=passwordValid,
                    roles={RolDto(id=1)}  # Aquí asumo que solo asignas un rol con ID 1
                )
            )

            data = await ApiManager.register_paciente(paciente_dto)
            if data:
                logger.info(data)
                access_token = data.get('access_token')
                refresh_token = data.get('refresh_token')
                if access_token and refresh_token:
                    page.overlay.append(ft.AlertDialog(content=ft.Text(value="Exito al registrar"), open=True))
                    logger.info("Tokens obtenidos del registro paciente")
                    page.session.set("access_token", access_token)
                    page.session.set("refresh_token", refresh_token)
                else:
                    page.overlay.append(ft.AlertDialog(content=ft.Text(value="Exitoso, pero sin tokens"), open=True))
                    logger.error("Los tokens no fueron obtenidos")
            else:
                page.overlay.append(ft.AlertDialog(content=ft.Text(value="Error recibido"), open=True))
                logger.error("No hay data obtenida")
        except Exception as e:
            logger.error(e)
            return

    async def handle_register(e):
        await register()
        page.update()

    page.add(nombre, segundo_nombre, apellido, segundo_apellido, fecha, fecha_picker, pasaporte, cedula,
             usuario, password, correo, ft.FilledButton(text="Registrar Paciente", on_click=handle_register))
    page.update()


ft.app(target=main)
