from peewee import *
from . import HabitModel

class HabitRequestModel(HabitModel):
    '''
    
    '''

    class Meta:
        table_name='p_habit_request'

    url_protocol = CharField(10)
    url_host = CharField(160)
    url_port = IntegerField(null=True)
    url_path = CharField(160)
    url_query = TextField(null=True)
    url_hash = TextField(null=True)
    http_method = CharField(10)
    http_headers = TextField()
    http_body = TextField(null=True)
    create_at = DateTimeField()