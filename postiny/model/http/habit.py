from peewee import *

class HabitRequestModel(Model):
    '''
    
    '''

    class Meta:
        table='p_habit_request'

    url_protocol = CharField(10)
    url_other = CharField(160)
    create_at = DateTimeField(formats='')