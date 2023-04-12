from ptapi42 import Api42, Api42Request
import datetime
from pprint import pprint as pp
from achievements.models import Student, Achievement

api: Api42 = Api42()
api.requests_per_second = 5
api.log_lvl = 'DEBUG'
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

def getAchievements() -> list[dict]:
    achievements_list = api.get('achievements', {"campus_id": campus_id})
    achievements: list[dict] = []
    for achievement in achievements_list:
        if not achievement["visible"]:
            print(f"achievement: {achievement['name']} not visible")
            continue

        achievement_user_list: list[dict] = api.get(f"achivements/{achievement['achievement_id']}/achievements_users")
        users_with_achievement: list[int] = []
        for achievement_user in achievement_user_list["users"]:
            users_with_achievement.append(achievement_user["user_id"])
        achievements.append({
            "achievement_name": achievement["name"],
            "nbr_of_success": achievement["nbr_of_success"],
            "achievement_id": achievement["id"],
            "description": achievement["description"],
            "users_with_achievement": users_with_achievement
        })

    return achievements
                
getCampusId()
getAllUsersFrom42Cursus()
achievement_list: list[dict] = getAchievements()

for user in users:

    student = Student.objects.create(username=user["login"], email=user["email"], user_id=user["id"])
    student.save()
    
    for achievement in achievement_list:
        achivement_record = Achievement(
            parent=student,
            achievement_id=achievement['achievement_id'],
            achievement_name=achievement['achievement_name'],
            nbr_of_success=achievement['nbr_of_success'],
            description=achievement['description'],
        )
        if user["id"] in achievement["users_with_achievement"]:
            achivement_record.completed=True,
        else:
            achivement_record.completed=False,

# for user in achievement_users:
#     student = Student.objects.get(user_id=user["user_id"])
#     student.achievements.
# for achievement in achievement_list:

