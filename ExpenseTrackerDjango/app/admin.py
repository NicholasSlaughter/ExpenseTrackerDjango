from django.contrib import admin
from .models import Category, Period, Expense, Alert

#User Name: Admin
#Password: tRiumph84

#admin.site.register(ApplicationUser)
admin.site.register(Expense)
admin.site.register(Alert)
admin.site.register(Category)
admin.site.register(Period)