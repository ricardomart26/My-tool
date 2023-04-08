from django.db import models

# Create your models here.
class Achievement(models.Model):
    achievement_name = models.CharField(max_length=200)
    nbr_of_success = models.IntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.achievement_name
    
class Student(models.Model):
    username = models.CharField(max_length=20)
    achievements = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="achievements") 

    def __str__(self):
        return self.username

