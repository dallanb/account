from flask import g
import logging


def init_account_status(status_enums):
    logging.info(f"init_account_status started")
    Status = g.src.Status

    for status_enum in status_enums:
        status = Status(name=status_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_account_status completed")
    return
