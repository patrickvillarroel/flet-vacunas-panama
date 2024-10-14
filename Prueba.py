import flet as ft

def main(page: ft.Page):
    page.title = 'VacunAPP'
    page.window.width = 900
    page.window.height = 950
    page.bgcolor = ft.colors.WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.adaptive = True

    nombre = ft.TextField(
        width=400,
        height=40,
        hint_text='Nombre',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    apellido = ft.TextField(
        width=400,
        height=40,
        hint_text='Apellido',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.PERSON,
    )

    fecha_nacimiento = ft.TextField(
        width=400,
        height=40,
        hint_text='Nacimiento',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.DATE_RANGE,
    )

    cedula = ft.TextField(
        width=400,
        height=40,
        hint_text='Cedula',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.CREDIT_CARD,

    )

    direccion = ft.TextField(
        width=400,
        height=40,
        hint_text='Direccion',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.OTHER_HOUSES,
    )

    correo = ft.TextField(
        width=400,
        height=40,
        hint_text='Correo Electronico',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.CONTACT_MAIL,
    )

    telefono = ft.TextField(
        width=400,
        height=40,
        hint_text='Telefono',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.CONTACT_PHONE,
    )

    user = ft.TextField(
        width=400,
        height=40,
        hint_text='Usuario',
        border=ft.InputBorder.UNDERLINE,
        prefix_icon=ft.icons.SUPERVISED_USER_CIRCLE,
    )

    password = ft.TextField(
        width=400,
        height=40,
        hint_text='Contraseña',
        prefix_icon=ft.icons.LOCK_PERSON,
        border=ft.InputBorder.UNDERLINE,
        color='black',
        password=True,
        can_reveal_password=True
    )

    registrar = ft.ElevatedButton(
        content=ft.Text(
            'REGISTRAR',
            color='blue',
            weight=ft.FontWeight.W_500,
        ),
        #on_click=lambda e: insertDato(nombre.value, user.value, password.value, 1, page),
        width=200,
        bgcolor='white',
    )

    body = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Container(
                            ft.Image(
                                src='assets/logo.png',
                                width=100,
                                height=100
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                'REGISTRARSE',
                                width=400,
                                size=30,
                                weight=ft.FontWeight.W_900,
                                text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            controls=[
                                nombre,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                apellido
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                cedula
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                fecha_nacimiento
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                direccion
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                correo
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                telefono
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                user
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Row(
                            controls=[
                                password
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Container(
                            registrar,
                            alignment=ft.alignment.center
                        ),
                        ft.Row(
                            [
                                ft.TextButton(content=(ft.Text('Regresar a la pagina principal', color=ft.colors.WHITE))),
                            ],
                            spacing=1,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),


                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                gradient=ft.LinearGradient(['blue', 'lightblue']),
                width=600,
                height=900,
                border_radius=20,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
    )

    contenedor = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src='assets/fondo2.jpg',
            fit=ft.ImageFit.COVER,
        ),
        content=body,
        alignment=ft.alignment.center,
        margin=-10
    )

    page.clean()
    page.controls.append(contenedor)
    page.update()

if __name__ == '__main__':
    ft.app(target=main)