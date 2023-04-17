from ptapi42 import Api42
import datetime
from achievements.models import Student, Achievement
from dotenv import load_dotenv
from pprint import pprint as pp
load_dotenv()
api: Api42 = Api42(requests_per_second=7)
# campus_name = input("Campus name: ").lower()
campus_name = "lisboa"

campus_id = ""
users = []

def getCampusId():
    print("\nGetting Campus ID...")

    url = f'campus/{campus_name}'    
    global campus_id
    campus_id = api.get(url=url)['id']


def getAllUsersFrom42Cursus():
    print("\nGetting 42 Cursus Users...")

    url = "cursus_users"    
    params: dict = { 
        'cursus_id' : 21,
        'filter' : {
            'campus_id' : campus_id
            }
        }        
    users_unfiltered = api.get(url=url, params=params)

    for user in users_unfiltered:
        if user['user']['kind'] != 'admin' or user['user']['staff?'] == False:
            if user['blackholed_at'] != None:
                blackholed_at = datetime.datetime.strptime(user['blackholed_at'].split(".")[0], '%Y-%m-%dT%H:%M:%S')
                if blackholed_at < datetime.datetime.now():
                    continue 
            user_info = {
                "login": user['user']['login'],
                "id": user['user']['id'],
                "email": user['user']["email"]
                }
            users.append(user_info)

def get_achievements() -> None:
    getCampusId()
    getAllUsersFrom42Cursus()
    for user in users:
        print(f"Starting user {user['login']} achievements")
        achievements_list = api.get('achievements', {"campus_id": campus_id})
        completed_achievement: list[int] = []
        achievement_of_user_list: list[dict] = api.get(f"achievements_users?filter[user_id]={user['id']}")
        pp(achievement_of_user_list)
        print("Finished geting achievements users for this user")
        achievement_record : list[Achievement] = []
        print("Created student for Student module")
        for achievement in achievement_of_user_list:
            achievement_record.append(Achievement(
                achievement_id=achievement['achievement_id'],
                achievement_name=achievement['achievement_name'],
                nbr_of_success=achievement['nbr_of_success'],
                description=achievement['description'],
                completed=True
            ))
            completed_achievement.append(achievement["id"])
        print("Finished completed achievements")
        for achievement in achievements_list:
            if achievement['id'] in completed_achievement:
                continue
            achievement_record.append(Achievement(
                achievement_id=achievement['achievement_id'],
                achievement_name=achievement['achievement_name'],
                nbr_of_success=achievement['nbr_of_success'],
                description=achievement['description'],
                completed=False
            ))
        student: Student = Student.objects.get_or_create(
            username=user["login"], 
            email=user["email"], 
            user_id=user["id"]
        )
        print("Finished non completed achievements")
        for achievement in achievement_record:
            student.achievement_set.add(achievement)
        student.save()
        print(f"Finished student {user['login']} achievements")
    print("Finished creating students with achivements!")

