from django.db import models
    

class Student(models.Model):
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, default="No email")
    
    def __str__(self):
        return self.username

# Create your models here.
class Achievement(models.Model):
    achievement_id = models.IntegerField(default=0)
    achievement_name = models.CharField(max_length=200)
    nbr_of_success = models.IntegerField()
    description = models.TextField(default="No description", max_length=500)
    completed = models.BooleanField(default=False)
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name="achievements",
        default=None
    ) 

    def __str__(self):
        return self.achievement_name