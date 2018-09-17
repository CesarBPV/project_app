# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Pruebas para el servicio Users. """

    def test_users(self):
        """comprobado que la ruta /ping funcione correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])


if __name__ == '__main__':
    unittest.main()
