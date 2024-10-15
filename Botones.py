import flet as ft

pacienteButton = ft.ElevatedButton(
    adaptive=True,
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

docButton = ft.ElevatedButton(
    adaptive=True,
    text="Doctor",
    #on_click=conn_on_click,
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

adminButton = ft.ElevatedButton(
    adaptive=True,
    text="Admin",
    #on_click=conn_on_click,
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

autoridadButton = ft.ElevatedButton(
    adaptive=True,
    text="Autoridad",
    #on_click=conn_on_click,
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

fabricanteButton = ft.ElevatedButton(
    adaptive=True,
    text="Proveedor",
    #on_click=conn_on_click,
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
    adaptive=True,
    bgcolor=ft.colors.WHITE,
    width=30,
    height=30,
    content=ft.Image(src="assets/images/salidaIcon.png", width=23, height=23),
    ##on_click=closeApp
)
