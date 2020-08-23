from flask import g
import logging


def init_account_role(role_enums):
    logging.info(f"init_account_role started")
    Role = g.src.Role

    for role_enum in role_enums:
        status = Role(name=role_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_account_role completed")
    return
