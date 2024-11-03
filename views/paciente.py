import logging
from typing import List
from uuid import UUID

import flet as ft

import ApiManager
from ApiManager import ApiAuthentication
from validations.PacienteDto import PacienteDto, VistaVacunaEnfermedad, from_json_to_vista_vacuna_enfermedad
from views.controles import contenedor, dialog_contactos

logger = logging.getLogger(__name__)


def botonera() -> ft.NavigationBar:
    return ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.INFO,
                label="Mi Info"
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.COLORIZE,
                label="Mis Vacunas"
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.PHONE,
                label="Contactanos",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.EXIT_TO_APP,
                label="Salir",
            ),
        ],
        indicator_color=ft.colors.LIGHT_BLUE_100,
        adaptive=True
    )


def cambio_info_paciente(paciente: PacienteDto) -> ft.Row:
    return ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Vacunas APP", weight=ft.FontWeight.BOLD, size=50, color=ft.colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            width=850,
                        ),
                        ft.Row(
                            [
                                ft.Column(  # Primera columna
                                    [ft.Container(
                                        ft.Column(
                                            controls=[ft.Row([ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                                                              ft.Text("Datos del Usuario", weight=ft.FontWeight.BOLD,
                                                                      size=15, color=ft.colors.BLACK)]),
                                                      ft.Divider(height=5, color=ft.colors.BLACK),
                                                      ft.TextField(label="Nombre", value=paciente.nombre, width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Apellido", value=paciente.apellido1,
                                                                   width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Cedula", value=paciente.cedula, width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Usuario", value=paciente.usuario.username,
                                                                   width=350,
                                                                   color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Correo", value=paciente.correo,
                                                                   width=350, color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.TextField(label="Numero de Telefono", value=paciente.telefono,
                                                                   width=350, color=ft.colors.BLACK, read_only=True,
                                                                   label_style=ft.TextStyle(color='black', size=19,
                                                                                            weight=ft.FontWeight.BOLD)),
                                                      ft.Divider(height=5, color=ft.colors.BLACK)]

                                        ),
                                        bgcolor=ft.colors.WHITE, width=350, alignment=ft.alignment.center, height=450)],
                                    width=357,
                                ),
                                ft.Column([
                                    ft.Container(
                                        ft.Column(controls=[
                                            ft.Container(
                                                ft.Image(src="/images/LogoVacuna.png", width=400, height=400),
                                                alignment=ft.alignment.center), ]),
                                        bgcolor=ft.colors.WHITE, width=350, alignment=ft.alignment.center, height=450)],
                                    width=357, ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=850
                        ), ],
                    alignment=ft.alignment.center, ),
                alignment=ft.alignment.center,
                margin=ft.margin.all(0),
                bgcolor=ft.colors.WHITE,
            )],
        alignment=ft.MainAxisAlignment.CENTER,
    )


def paciente_view(page: ft.Page) -> ft.View:
    data = page.session.get("paciente")
    paciente = PacienteDto(**data)
    contenido = contenedor()
    table_container = ft.Column(auto_scroll=True, )
    save_file_path: str
    vacuna_seleccionada: UUID
    botones = botonera()
    authentication: ApiAuthentication = ApiManager.ApiAuthentication(page.session.get('access_token'),
                                                                     page.session.get('refresh_token'))
    save_file_dialog = ft.FilePicker()

    async def handle_nav(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            cambio_info()
        elif selected_index == 1:
            await cambio_vacunas()
        elif selected_index == 2:
            page.overlay.append(dialog_contactos())
        elif selected_index == 3:
            page.go("/")
        page.update()

    botones.on_change = handle_nav

    # Decide según la plataforma si guardar el pdf con el sistema o enviar al navegador
    def seleccionar_vacuna(e):
        nonlocal vacuna_seleccionada
        vacuna_seleccionada = e.control.data
        logger.info(f"Vacuna seleccionada: {vacuna_seleccionada}")
        if not page.web:
            save_file_dialog.save_file(
                allowed_extensions=["pdf"], file_type=ft.FilePickerFileType.CUSTOM, file_name="certificado",
            )

            def save_file_result(event: ft.FilePickerResultEvent):
                nonlocal save_file_path
                save_file_path = event.path if event.path else None
                page.run_task(guardar_pdf_async)

            save_file_dialog.on_result = save_file_result
        else:
            page.launch_url(ApiManager.get_pdf_paciente_url(paciente.id, vacuna_seleccionada))

    # Guardar el pdf utilizando el sistema
    async def guardar_pdf_async():
        nonlocal save_file_path
        if save_file_path and not save_file_path.isspace():
            response = await ApiManager.get_pdf_file_paciente(paciente.id, vacuna_seleccionada)
            if response is not None and response.status_code == 200:
                save_file_path += ".pdf"
                logger.debug(f"Guardando archivo pdf en: {save_file_path}")
                with open(save_file_path, 'wb') as file:
                    file.write(response.content)
                logger.debug(f"Archivo PDF guardado en: {save_file_path}")
                page.overlay.append(
                    ft.SnackBar(content=ft.Text(f"Archivo PDF guardado en: {save_file_path}"), open=True))
            else:
                page.overlay.append(
                    ft.SnackBar(content=ft.Text("Error en generar el PDF, intente más tarde"), open=True))
                logger.error("Mostrando mensaje de error al usuario en crear PDF")
        else:
            logger.error("No hay path definido")
            page.overlay.append(
                ft.SnackBar(content=ft.Text("Guardar PDF cancelado, no hay ubicación para guardar"), open=True))
        page.update()

    def build_table(data_vacuna: List[VistaVacunaEnfermedad]):
        logger.info("Data para tabla: %s", data_vacuna)
        rows = []
        enfermedades = ""
        for row in data_vacuna:
            if row.enfermedades:
                for enfermedad in row.enfermedades:
                    enfermedades = enfermedad.get("nombre") + ", "
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(row.vacuna, color="black")),
                    ft.DataCell(ft.Text(row.numero_dosis, color="black")),
                    ft.DataCell(ft.Text(enfermedades, color="black")),
                    ft.DataCell(ft.Text(str(row.fecha_aplicacion), color="black")),
                    ft.DataCell(ft.IconButton(data=row.id_vacuna, on_click=seleccionar_vacuna, icon=ft.icons.DOWNLOAD,
                                              icon_size=20)),
                ])
            )

        return ft.DataTable(
            width=950,
            bgcolor=ft.colors.WHITE70,
            border=ft.border.all(2, "blue"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "blue"),
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=50,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            divider_thickness=0,
            columns=[
                ft.DataColumn(ft.Text("Vacuna", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(
                    ft.Text("Número Dosis", text_align=ft.alignment.center_left, color=ft.colors.BLUE)),
                ft.DataColumn(
                    ft.Text("Enfermedad previene", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(
                    ft.Text("Fecha de aplicación", text_align=ft.alignment.center, color=ft.colors.BLUE)),
                ft.DataColumn(ft.Text("Descarga", text_align=ft.alignment.center, color=ft.colors.BLUE)),
            ],
            rows=rows
        )

    async def cambio_vacunas():
        result_container.controls.clear()
        result_container.controls.append(menu_vacunas)
        page.update()
        view_data = await ApiManager.get_vista_paciente_vacuna_enfermedad(authentication)
        list_vacunas = view_data.get("view_vacuna_enfermedad")
        logger.debug(list_vacunas)
        vacuna: List[VistaVacunaEnfermedad] = [from_json_to_vista_vacuna_enfermedad(v) for v in list_vacunas]
        table_container.controls.clear()
        table_container.controls.append(build_table(vacuna))
        if not list_vacunas:
            page.overlay.append(ft.SnackBar(content=ft.Text("No tiene dosis registradas"), open=True))
        page.update()

    def cambio_info():
        result_container.controls.clear()
        result_container.controls.append(cambio_info_paciente(paciente))
        page.update()

    result_container = ft.Row([cambio_info_paciente(paciente)], alignment=ft.MainAxisAlignment.CENTER, )

    menu_vacunas = ft.Row([
        ft.Container(
            ft.Column([
                ft.Text("Vacunas APP", weight=ft.FontWeight.BOLD, size=50, color=ft.colors.BLACK),
                table_container, ],
                auto_scroll=True,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.all(0),
            bgcolor=ft.colors.WHITE,
            height=700,
            width=1000,
        ), ],
    )

    contenido.content = ft.Container(
        ft.Column(
            controls=[result_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        bgcolor=ft.colors.WHITE,
        height=580,
        width=1000,
        border_radius=30,
        alignment=ft.alignment.center,
    )
    if not page.web:
        page.overlay.append(save_file_dialog)

    return ft.View(
        route="/paciente",
        bgcolor=ft.colors.TRANSPARENT,
        controls=[ft.SafeArea(
            expand=True,
            content=contenido
        )],
        navigation_bar=botones
    )
