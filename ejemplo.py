from typing import List

import flet as ft

import ApiManager
from validations.DireccionesDto import DistritoDto  # Asumiendo que ya tienes estas clases


# Obtener tanto provincias como distritos al inicio
async def obtener_provincias_y_distritos():
    provincias = await ApiManager.get_provincias()
    distritos = await ApiManager.get_distritos()  # Devuelve todos los distritos
    return provincias, distritos


# Filtrar distritos por provincia seleccionada
def filtrar_distritos_por_provincia(distritos: List[DistritoDto], provincia_id: int):
    return [d for d in distritos if d.provincia.id == provincia_id]


async def main(page: ft.Page):
    page.title = "Dropdown Dinámico"

    # Obtener provincias y distritos al cargar la página
    provincias, distritos = await obtener_provincias_y_distritos()

    # Dropdown de provincias
    dropdown_provincia = ft.Dropdown(
        options=[ft.dropdown.Option(text=prov.nombre, key=str(prov.id)) for prov in provincias],
        label="Seleccione una provincia",
        on_change=lambda e: actualizar_distritos(e.control.value)  # Cambiar distritos cuando la provincia cambie
    )

    # Dropdown de distritos
    dropdown_distrito = ft.Dropdown(
        options=[],  # Se llenará dinámicamente según la provincia seleccionada
        label="Seleccione un distrito"
    )

    # Agregar dropdowns a la página
    page.add(dropdown_provincia, dropdown_distrito)

    # Función para actualizar los distritos según la provincia seleccionada
    def actualizar_distritos(provincia_id):
        distritos_filtrados = filtrar_distritos_por_provincia(distritos, int(provincia_id))
        dropdown_distrito.options = [ft.dropdown.Option(text=d.nombre, key=str(d.id)) for d in distritos_filtrados]
        dropdown_distrito.value = None  # Reiniciar el valor seleccionado del dropdown de distritos
        page.update()  # Actualizar la interfaz

    page.update()

if __name__ == '__main__':
    ft.app(target=main)
