# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase

from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Pruebas para el Servicio de Usuarios """

    def test_users(self):
        """comprobado que la ruta /ping funcione correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_user(self):
        """ Asegurando que se pueda agregar un nuevo usuario a la base de datos"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username':'cesar',
                    'email':'cesarpareja@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data=json.loads(response.data.decode())
            self.assertEqual(response.status_code,201)
            self.assertIn('cesarpareja@upeu.edu.pe fue agregado!!!',data['mensaje'])
            self.assertIn('satisfactorio',data['estado'])

    def test_add_user_invalid_json(self):
        """Asegurando de que se lance un error cuando el objeto JSON esta vacío."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_user_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene una clave de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email':'cesarpareja@upeu.edu.pe'}),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_user_duplicate_email(self):
        """Asegurando que se produce un error si el email ya existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username':'cesar',
                    'email': 'cesarpareja@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'cesar',
                    'email': 'cesarpareja@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento, ese email ya existe.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_single_user(self):
        """Asegurando que el usuario único se comporte correctamente."""
        user = add_user('cesar', 'cesarpareja.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('cesar', data['data']['username'])
            self.assertIn('cesarpareja.edu.pe', data['data']['email'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        """Asegúrese de que se arroje un error si no se proporciona una identificación."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['mensaje'])
            self.assertIn('falló', data['estado'])
            
    def test_single_user_incorrect_id(self):
        """Asegurando de que se arroje un error si la identificación no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_all_users(self):
        """Asegurando obtener todos los usuarios correctamente."""
        add_user('cesar', 'cesarpareja@upeu.edu.pe')
        add_user('igor', 'igorchipana@upeu.edu.pe')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('cesar', data['data']['users'][0]['username'])
            self.assertIn('cesarpareja@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('igor', data['data']['users'][1]['username'])
            self.assertIn('igorchipana@upeu.edu.pe', data['data']['users'][1]['email'])
            self.assertIn('satisfactorio', data['estado'])



if __name__ == '__main__':
    unittest.main()
