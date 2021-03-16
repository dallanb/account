from src import Role, db


def init_account_role(role_enums):
    for role_enum in role_enums:
        status = Role(name=role_enum)
        db.session.add(status)
    db.session.commit()
    return
