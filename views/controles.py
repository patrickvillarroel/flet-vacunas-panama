import flet as ft


def contenedor() -> ft.Container:
    return ft.Container(
        image=ft.DecorationImage(
            src="/images/fondo2.jpg",
            fit=ft.ImageFit.COVER,
        ),
        bgcolor=ft.colors.TRANSPARENT,
        expand=True,
        margin=-10,
        alignment=ft.alignment.center,
    )
