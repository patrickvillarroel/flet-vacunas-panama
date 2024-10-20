import logging

import flet as ft

import ApiManager
from validations.PacienteDto import PacienteDto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def login(page: ft.Page, username: str, password: str):
    if username and not username.isspace() and password and not password.isspace():
        response = await ApiManager.login_paciente(username, password)
        if "error" not in response:
            paciente_json = response.get("paciente")
            if paciente_json:
                logger.info(paciente_json)
                paciente = PacienteDto(**paciente_json)
                page.add(
                    ft.Text(
                        value=f"Successful login for {paciente.nombre} and token is: {response.get('access_token')}",
                        style=ft.TextStyle(color=ft.colors.BLACK)))
                page.session.set("access_token", response.get("access_token"))
                page.session.set("refresh_token", response.get("refresh_token"))
                logger.info("Token en session storage: %s", page.session.contains_key("access_token"))
            else:
                page.overlay.append(ft.AlertDialog(content=ft.Text(value="No es un paciente"), open=True))
        else:
            page.overlay.append(ft.AlertDialog(content=ft.Text(value="Ha ocurrido un error"), open=True))
    else:
        page.overlay.append(ft.AlertDialog(content=ft.Text(value="Usuario y contraseña es requerido"), open=True))
    page.update()


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE
    # Configurar controles de input text
    username = ft.TextField(autofocus=True, text_style=ft.TextStyle(color=ft.colors.BLACK))
    password = ft.TextField(password=True, can_reveal_password=True, text_style=ft.TextStyle(color=ft.colors.BLACK))
    page.add(username, password)

    async def handle_login(e):
        await login(page, username.value, password.value)

    page.add(ft.FilledButton(text='Iniciar Sesión', on_click=handle_login))
    page.update()


ft.app(target=main)
