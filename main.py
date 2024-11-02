import logging

import flet as ft
from flet_core import ThemeMode

import views as vs

logging.basicConfig(level=logging.INFO)
# Colocarle a httpx solo nivel WARN
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARN)
handler = logging.StreamHandler()
handler.setLevel(logging.WARN)
httpx_logger.addHandler(handler)

logger = logging.getLogger(__name__)


def main(page: ft.Page):
    page.session.clear()
    page.title = "Vacunas APP"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.TRANSPARENT
    page.navigation_bar = None
    page.window.maximized = True
    page.scroll = None
    page.theme_mode = ThemeMode.LIGHT
    page.adaptive = True
    page.decoration = ft.BoxDecoration(
        bgcolor=ft.colors.TRANSPARENT,
        image=ft.DecorationImage(
            src="/images/fondo2.jpg",
            fit=ft.ImageFit.COVER,
        ))
    page.clean()

    def route_manager(route):
        page.views.clear()
        page.scroll = None
        page.navigation_bar = None
        if page.route == "/":
            page.session.clear()
            page.views.append(vs.index_view(page))
        elif page.route == "/login":
            page.views.append(vs.sign_in(page))
        elif page.route == "/register":
            page.views.append(vs.sign_up(page))
        else:
            page.overlay.append(ft.SnackBar(content=ft.Text(value="Ruta inválida"), open=True))
            page.update()
            page.go("/")
        page.update()
        # TODO agregar solo las vistas permitidas por rol

    page.on_route_change = route_manager
    page.go("/")
    page.update()

if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
