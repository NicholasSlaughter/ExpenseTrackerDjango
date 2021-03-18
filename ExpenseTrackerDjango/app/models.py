"""
Definition of models.
"""

from django.db import models

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
    #application_user = models.ForeignKey(ApplicationUser,on_delete=models.CASCADE)

class Period(models.Model):
    name = models.CharField(max_length=50,null=False)

    #String representation of the Period object
    def __str__(self):
        return self.name

class Alert(models.Model):
    max_amount = models.FloatField(max_length=20,null=False)
    current_amount = models.FloatField(max_length=20,null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    #application_user = models.ForeignKey(ApplicationUser,on_delete=models.CASCADE)
