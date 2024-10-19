import unittest
from datetime import datetime
from uuid import uuid4

from pydantic import ValidationError

from validations.AccountDto import UsuarioDto, RolDto
from validations.DireccionesDto import DireccionDto
from validations.PacienteDto import PacienteDto


class TestPacienteDto(unittest.TestCase):
    def test_paciente_dto_valid(self):
        with self.assertRaises(ValidationError) as exc_info:
            PacienteDto(
                id=uuid4(),
                cedula="8-1024-1653",
                pasaporte=None,
                nombre="Rey",
                nombre2="Alberto",
                apellido1="Acosta",
                apellido2="Muñoz",
                correo=None,
                telefono=None,
                fecha_nacimiento=datetime(2025, 1, 1),
                edad=None,
                sexo='M',
                estado="VALIDADO",
                disabled=False,
                direccion=DireccionDto(
                    id=uuid4(),
                    direccion="Calle falsa 123",
                    distrito=None,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
                usuario=UsuarioDto(
                    id=uuid4(),
                    username="reyAcosta",
                    password="pruebas1234",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    last_used=datetime.now(),
                    roles={
                        RolDto(
                            id=1,
                            nombre="pruebaRol",
                            descripcion=None,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            permisos=None
                        )
                    },
                    cedula="8-1024-1653",
                    pasaporte=None,
                    licencia_fabricante=None
                )
            )
        self.assertIn('La fecha debe ser hoy o en el pasado', str(exc_info.exception))


if __name__ == '__main__':
    unittest.main()
