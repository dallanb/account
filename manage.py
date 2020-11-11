import os
from flask import g
from flask.cli import FlaskGroup
from src import app, db, common
from bin import init_account_status, init_account_role
import src

cli = FlaskGroup(app)


def full_init():
    initialize_statuses()
    os.system('flask seed run')


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def clear_cache():
    common.cache.clear()


def initialize_statuses():
    init_account_status(status_enums=common.StatusEnum)
    init_account_role(role_enums=common.RoleEnum)
    return


@cli.command("init")
def init():
    full_init()


@cli.command("reset_db")
def reset_db():
    create_db()


@cli.command("delete_db")
def delete_db():
    clear_db()


@cli.command("flush_cache")
def flush_cache():
    clear_cache()


@cli.command("init_status")
def init_status():
    initialize_statuses()


if __name__ == "__main__":
    cli()
