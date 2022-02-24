from peewee import *
from . import HabitModel

class HabitRequestModel(HabitModel):
    '''
    
    '''

    class Meta:
        table_name='p_habit_request'

    url_protocol = CharField(10)
    url_host = CharField(160)
    url_path = CharField(160)
    create_at = DateTimeField()