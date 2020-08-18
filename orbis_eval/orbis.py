"""
Main
"""
import pathlib
import os
import click
from typing import Union, AnyStr

from orbis_eval_libs.libs import user_folder as uf
from orbis_eval_libs.libs import yaml as ym

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

        self.folder = pathlib.Path(os.path.dirname(os.path.realpath(__file__))).resolve()

    def check_user_folder(
            self,
            headless: bool = False,
            custom_user_folder: Union[AnyStr, None] = None
    ) -> Union[bool, pathlib.Path]:

        """
        Check if user folder exists
        """

        user_folder, msg = uf.find(headless=headless, orbis_dir=self.folder, custom_user_folder=custom_user_folder)
        if not user_folder:
            click.echo(f"User folder not found. Please run orbis init to create.")
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
@click.option('--headless', is_flag=True, default=False, help='')
def init(
        user_folder: Union[AnyStr, bool],
        headless: bool
):
    """

    Args:
        user_folder:
        headless:
    """

    orbis = Orbis()
    user_folder, msg = uf.find(headless=headless, custom_user_folder=user_folder)

    user_folder = pathlib.Path(user_folder)
    if user_folder and uf.check(user_folder):
        click.echo(f"Orbis set up with user folder at {user_folder}")
        os.abort()

    else:
        user_folder = uf.ask()
        uf.create(user_folder, orbis.folder)
        os.abort()


@click.command()
@click.option('--yaml', default=False, help='')
@click.option('--headless', default=False, is_flag=True, help='')
@click.option('--user-folder', default=False, help='')
def run(
        yaml: Union[AnyStr, bool],
        headless: bool,
        user_folder: Union[AnyStr, bool]
):
    """

    Args:
        yaml:
        headless:
        user_folder:
    """

    orbis = Orbis()
    user_folder = orbis.check_user_folder(custom_user_folder=user_folder, headless=headless)

    configs_folder = [yaml] if yaml else user_folder
    config_files = ym.fetch_yamls(configs_folder)
    configs = ym.read_yamls(config_files)
    click.echo(configs)


@click.command()
@click.option('--user-folder', default=False, help='')
@click.option('--headless', default=False, is_flag=True, help='')
def show(
        user_folder: Union[AnyStr, bool],
        headless: bool
):
    """

    Args:
        user_folder:
        headless:
    """
    orbis = Orbis()
    user_folder = orbis.check_user_folder(custom_user_folder=user_folder, headless=headless)
    click.echo(user_folder)


cli.add_command(init)
cli.add_command(run)
