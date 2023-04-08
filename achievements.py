from ptapi42 import Api42
from pprint import pprint as pp

api = Api42(requests_per_second=7, log_lvl='WARNING', raises=True)

def debug(msg:str, obj: list):
    print(msg)
    pp(obj[0])
    

achievements_list = api.get('achievements', {"campus_id": 38})

debug("achievements_list", achievements_list)

for achievement in achievements_list:
    print(f'achievement name: {achievement["name"]}\n\
nbr of success: {achievement["nbr_of_success"]}')
    campus_list = achievement['campus']
    print('campus name:', end=" ")
    for campus in campus_list:
        print(campus, end=", ")
    print('\n')
    
