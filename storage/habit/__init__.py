from importlib import import_module
from inspect import isclass
from pkgutil import iter_modules
from loguru import logger
from peewee import *
from config.habit import *

DB_HABIT_PROXY = DatabaseProxy()


class HabitModel(Model):
    class Meta:
        database = DB_HABIT_PROXY


def storage_init_habit():
    '''

    '''

    db = SqliteDatabase(
        DB_HABIT_PATH,
        pragmas={
            'journal_mode': DB_HABIT_JOURNAL_MODE,
            'cache_size': DB_HABIT_CACHE_SIZE,
            'synchronous': DB_HABIT_SYNCHRONOUS,
        }
    )
    DB_HABIT_PROXY.initialize(db)

    for _, child, _ in iter_modules(__path__):
        mn = f'{__name__}.{child}'
        m = import_module(mn)
        logger.info(f'load: {mn}')
        for mv in m.__dict__.values():
            if isclass(mv) and issubclass(mv, HabitModel) and mv != HabitModel:
                mv.create_table(safe=True)

    
