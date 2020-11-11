import logging

from src import Role, db


def init_account_role(role_enums):
    logging.info(f"init_account_role started")

    for role_enum in role_enums:
        status = Role(name=role_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_account_role completed")
    return
