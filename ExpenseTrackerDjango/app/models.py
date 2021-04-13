"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class ApplicationUser(models.Model):
 #   email = models.EmailField(max_length=254,null=False)
  #  password = models.CharField(max_length=50,null=False)
   # first_name=models.CharField(max_length=50,null=False)
    #last_name=models.CharField(max_length=50,null=False)

class Category(models.Model):
    name = models.CharField(max_length=50,null=False)

    #String representation of the Category object
    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.FloatField(max_length=20,null=False)
    date = models.DateTimeField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=0)

class Period(models.Model):
    name = models.CharField(max_length=50,null=False)

    #String representation of the Period object
    def __str__(self):
        return self.name

class Alert(models.Model):
    max_amount = models.FloatField(max_length=20,null=False)
    current_amount = models.FloatField(max_length=20,null=False)
    period_start_date = models.DateTimeField(null=False,default="1111-11-11 11:11")
    period_end_date = models.DateTimeField(null=False,default="1111-11-11 11:11")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
