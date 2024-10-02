import flet as ft
from flet import *
from Connection import *
import App as app
from App import *
from Login import *


def conn_on_click(e):
    conexion()


pacienteButtom = ft.ElevatedButton(
    text="Paciente",
    #on_click=go_login(),
    width=200,
    height=40,
    style=ft.ButtonStyle(
        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
        shape=ft.RoundedRectangleBorder(radius=20),
        elevation={"": 2, "hovered": 6}
    ),
    icon=ft.icons.PERSON,
)

docButtom = ft.ElevatedButton(
    text="Doctor",
    on_click=conn_on_click,
    width=200,
    height=40,
    style=ft.ButtonStyle(
        bgcolor={"": ft.colors.BLUE_ACCENT, "hovered": ft.colors.BLUE},
        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
        shape=ft.RoundedRectangleBorder(radius=20),
        elevation={"": 2, "hovered": 6}
    ),
    icon=ft.icons.LOCAL_HOSPITAL,
)

adminButtom = ft.ElevatedButton(
    text="Admin",
    on_click=conn_on_click,
    width=200,
    height=40,
    style=ft.ButtonStyle(
        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
        shape=ft.RoundedRectangleBorder(radius=20),
        elevation={"": 2, "hovered": 6}
    ),
    icon=ft.icons.ADMIN_PANEL_SETTINGS
)

autorButtom = ft.ElevatedButton(
    text="Autoridad",
    on_click=conn_on_click,
    width=200,
    height=40,
    style=ft.ButtonStyle(
        bgcolor={"": ft.colors.GREEN, "hovered": ft.colors.GREEN_600},
        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
        shape=ft.RoundedRectangleBorder(radius=20),
        elevation={"": 2, "hovered": 6}
    ),
    icon=ft.icons.SECURITY
)

provButtom = ft.ElevatedButton(
    text="Proveedor",
    on_click=conn_on_click,
    width=200,
    height=40,
    style=ft.ButtonStyle(
        bgcolor={"": ft.colors.BLUE_ACCENT, "hovered": ft.colors.BLUE},
        color={"": ft.colors.WHITE, "hovered": ft.colors.WHITE70},
        shape=ft.RoundedRectangleBorder(radius=20),
        elevation={"": 2, "hovered": 6}
    ),
    icon=ft.icons.SHOP,
)

salida = ft.ElevatedButton(
        bgcolor=ft.colors.WHITE,
        width=30,
        height=30,
        content=ft.Image(src="salidaIcon.png", width=23, height=23),
        ##on_click=closeApp
    )
