#!/usr/bin/env python2

from flask.cli import FlaskGroup
import click
import os

os.environ['FLASK_APP'] = 'asmlearner/__init__.py'


@click.group(cls=FlaskGroup)
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def admin():
    '''Creates an editor account from the console.'''
    from asmlearner.db.models import User
    import getpass

    id_ = raw_input('ID: ')
    password_ = getpass.getpass('PW: ')

    user = User.create(name=id_, password=password_, role='admin').save(True)
    print 'Created user %r with id %r' % (user.name, user.id)


@cli.command()
def initdb():
    '''Creates some tables for the database'''
    from asmlearner import create_db
    create_db()
    print 'Initialized the database.'


if __name__ == '__main__':
    cli()
