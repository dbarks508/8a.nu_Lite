from django.db import models
from django.contrib.auth.models import User

# represents a boulder problem 
class Climb(models.Model):
    AREAS = [
        ("lcc", "Little Cottonwood Canyon"),
        ("o", "Ogden") 
    ]
    
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    area = models.CharField(max_length=3, choices=AREAS, default="lcc")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
# represents a log of a climb -> user ascending a climb
class Ascent(models.Model):
    TYPE =[
        ("o", "onsight"),
        ("f", "flash"),
        ("r", "redpoint")
    ]
    
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proposedGrade = models.CharField(max_length=10)
    type = models.CharField(max_length=1 ,choices=TYPE)
    date = models.DateField()
    comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.climb} - {self.user}"
