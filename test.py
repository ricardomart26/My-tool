from ptapi42 import Api42
from dotenv import load_dotenv
from pprint import pprint as pp

load_dotenv()

api: Api42 = Api42(requests_per_second=7, log_lvl='DEBUG')
campus_id: int = 38

url = "cursus_users"    
params: dict = { 
    'cursus_id' : 21,
    'filter' : {
        'campus_id' : campus_id
        }
    }        
users_unfiltered = api.get(url=url, params=params)

pp(users_unfiltered[0])

achievement_list = api.get('achievements', {"campus_id": campus_id})
pp(achievement_list[0])
