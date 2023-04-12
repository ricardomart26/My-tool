from ptapi42 import Api42
from pprint import pprint as pp

api = Api42(requests_per_second=7, log_lvl='WARNING', raises=True)

def debug(msg:str, obj: list):
    print(msg)
    pp(obj[0])
    

    
