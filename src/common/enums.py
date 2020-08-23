import enum


class StatusEnum(enum.Enum):
    pending = 1
    active = 2
    inactive = 3


class RoleEnum(enum.Enum):
    basic = 1
    admin = 2
    root = 3
