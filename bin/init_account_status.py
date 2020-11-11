import logging

from src import Status, db


def init_account_status(status_enums):
    logging.info(f"init_account_status started")

    for status_enum in status_enums:
        status = Status(name=status_enum)
        db.session.add(status)

    db.session.commit()
    logging.info(f"init_account_status completed")
    return
