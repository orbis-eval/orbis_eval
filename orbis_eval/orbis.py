"""
Main
"""
import pathlib
import os
import click

from orbis_eval_libs.libs import user_folder as uf

import logging

logger = logging.getLogger(__name__)


class Orbis(object):
    """
    Orbis
    """
    def __init__(self):
        """Summary
        """
        super(Orbis, self).__init__()

        self.folder = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.user_folder = None
        self.configs = None

    def check_user_folder(self):
        """
        Check if user folder exists
        """
        user_folder = uf.find()
        if not user_folder:
            print(f"User folder not found. Please run orbis init to create.")
            os.abort()
        return user_folder


@click.group()
def cli():
    """
    Entry Point
    """
    pass


@click.command()
@click.option('--user-folder', default=False, help='')
@click.option('--headless', default=False, help='')
def init(user_folder, headless):
    """

    Args:
        user_folder:
        headless:
    """
    orbis = Orbis()
    user_folder = uf.find(headless=headless, orbis_dir=False, custom_user_root=False)

    if orbis.user_folder and uf.check(user_folder):
        print(f"Orbis set up with user folder at {user_folder}")
        os.abort()

    else:
        orbis.user_folder = uf.ask()
        uf.create(user_folder, orbis.folder)
        os.abort()


@click.command()
@click.option('--yaml', default=False, help='')
def run(yaml):
    """

    Args:
        yaml:
    """
    orbis = Orbis()
    user_folder = orbis.check_user_folder()

    configs = [yaml] if yaml else user_folder
    print(configs)


@click.command()
@click.option('--user-folder', default=False, help='')
def show(user_folder):
    """

    Args:
        user_folder:
    """
    orbis = Orbis()
    user_folder = orbis.check_user_folder()
    print(user_folder)

cli.add_command(init)
cli.add_command(run)
