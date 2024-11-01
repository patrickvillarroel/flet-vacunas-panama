import logging

import flet as ft

from views.index import view

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
    page.navigation_bar = False
    page.window.maximized = True
    page.scroll = None
    page.theme_mode = "LIGHT"
    page.adaptive = True
    page.decoration = ft.BoxDecoration(
        bgcolor=ft.colors.TRANSPARENT,
        image=ft.DecorationImage(
            src="/images/fondo2.jpg",
            fit=ft.ImageFit.COVER,
        ))
    page.clean()
    page.views.append(view(page))
    page.go("/")
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
