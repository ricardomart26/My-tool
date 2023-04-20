from ptapi42 import Api42
import datetime
from achievements.models import Student, Achievement
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()
api: Api42 = Api42(requests_per_second=7, log_lvl='DEBUG')
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


def getAchievementUsersForCampus():
    user_ids: list = [user['id'] for user in users if 'id' in user]

    url = f'achievements_users'
    params: dict = {
        'filter' : {
            'user_id' : user_ids
        }
    }
    return api.get(url=url, params=params)

def get_achievements() -> None:
    getCampusId()
    getAllUsersFrom42Cursus()
    achievement_list = api.get('achievements', {"campus_id": campus_id})
    print("Finished getting achievements")
    for user in users:
        student: Student = Student(
            username=user["login"], 
            email=user["email"], 
            user_id=user["id"]
        )
        student.save()

        for achievement in achievement_list:
            if not achievement['nbr_of_success']:
                achievement['nbr_of_success'] = 0
            achievement_record = Achievement(
                student=student,
                achievement_id=achievement['id'],
                achievement_name=achievement['name'],
                nbr_of_success=achievement['nbr_of_success'],
                description=achievement['name'],
                completed=False
            )
            achievement_record.save()

    
    achievement_user_from_campus: list[dict] = getAchievementUsersForCampus()
    all_students: list[Student] = Student.objects.all()
    for achievement_user in achievement_user_from_campus:            
        for student in all_students: 
            if student.user_id == achievement_user['user_id']:
                achievement_found: Achievement = student.achievements.all().filter(achievement_id=achievement_user['id'])
                achievement_found.completed = True
    
        # print(f"Starting user {user['login']} achievements")
        # completed_achievement: list[int] = []
        # achievement_of_user_list: list[dict] = api.get(f"achievements_users?filter[user_id]={user['id']}")
        # pprint(achievement_of_user_list)
        # print("Finished geting achievements users for this user")
        # print("Created student for Student module")
        # for achievement in achievement_of_user_list:
        #     achievement_info = api.get(f"achievements/{achievement['achievement_id']}")
        #     if not achievement['nbr_of_success']:
        #         achievement['nbr_of_success'] = 0
        #     achievement_record.save()
        #     completed_achievement.append(achievement["id"])
        # print("Finished completed achievements")
        # for achievement in achievements_list:
        #     if achievement['id'] in completed_achievement:
        #         continue
        #     if not achievement['nbr_of_success']:
        #         achievement['nbr_of_success'] = 0
        #     # pprint(achievement)
        #     achievement_info = api.get(f"achievements/{achievement['id']}")
        #     achievement_record = Achievement(
        #         student=student,
        #         achievement_id=achievement['id'],
        #         achievement_name=achievement_info['name'],
        #         nbr_of_success=achievement['nbr_of_success'],
        #         description=achievement_info['description'],
        #         completed=False
        #     )
        #     achievement_record.save()
        # print("Finished non completed achievements")
        # print(f"Finished student {user['login']} achievements")
        # pprint(student.achievements.all())
    
    print("Finished creating students with achievements!")

