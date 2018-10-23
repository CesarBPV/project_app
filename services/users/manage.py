# services/users/manage.py

import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

# configurando informes de cobertura con coverage 4.5.1

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    """Recrea la base de datos"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Ejecución de pruebas sin cobertura de código"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Sembrado la base de datos."""
    db.session.add(User(username='igor', email="igorchipana@upeu.edu.pe"))
    db.session.add(User(username='cesar', email="cesarpareja@upeu.edu.pe"))
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con cobertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de cobertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
