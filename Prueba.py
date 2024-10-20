import flet as ft

import ApiManager


async def obtener_opciones():
    # List[ProvinciaDto]
    # Esta función puede generar los datos dinámicamente o extraerlos de una fuente
    provincias = await ApiManager.get_provincias()  # Convierte los datos en una lista de Dropdown.Option
    return [ft.dropdown.Option(text=op.nombre, key=str(op.id)) for op in provincias]


async def main(page: ft.Page):
    page.title = "Dropdown Dinámico"

    # Crear el dropdown, las opciones se obtienen de la función obtener_opciones
    dropdown_menu = ft.Dropdown(
        options=[],
        label="Seleccione una opción",
        on_change=lambda e: print(f"Opción seleccionada: {e.control.value}")
    )
    page.add(dropdown_menu)

    # Agregar el dropdown al contenido de la página
    async def actualizar_opciones():
        opciones = await obtener_opciones()
        dropdown_menu.options = opciones
        dropdown_menu.value = 0
        page.update()
    await actualizar_opciones()
    page.update()

if __name__ == '__main__':
    ft.app(target=main)
