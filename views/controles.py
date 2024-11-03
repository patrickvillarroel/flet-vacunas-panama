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


def dialog_contactos() -> ft.AlertDialog:
    return ft.AlertDialog(
        title=ft.Text("Contactos"),
        content=ft.Text("Ministerio de Salud (512-9100)" + "\n" +
                        "Caja del Seguro Social (199)"),
        open=True,
    )
