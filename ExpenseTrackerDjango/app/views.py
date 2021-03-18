"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import * 

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def EnterExpense(request):
    assert isinstance(request, HttpRequest)

    if request.method=="POST":
        if request.POST.get('category_name') and request.POST.get('expense_amount'):
            expense_to_save = Expense()
            expense_to_save.amount = request.POST.get('expense_amount')
            expense_to_save.date = datetime.now()
            expense_to_save.category = Category.objects.get(name=request.POST.get('category_name'))
            try:
                expense_to_save.save()
                categories_to_display = Category.objects.all()
                return render(
                    request,
                    'app/EnterExpense.html',
                    {
                        'title':'Enter Expense',
                        'message':'Where you enter expenses',
                        'year':datetime.now().year,

                        'expense': Expense,
                        'category': categories_to_display,
                        }
                    )
            except:
                print("Error can't save")
    else:
        categories_to_display = Category.objects.all()
        return render(
            request,
            'app/EnterExpense.html',
            {
                'title':'Enter Expense',
                'message':'Where you enter expenses',
                'year':datetime.now().year,

                'expense': Expense,
                'category': categories_to_display,
                }
            )

def History(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/History.html',
        {
            'title':'Expense History',
            'message':'Where you view your history of expenses',
            'year':datetime.now().year,
            }
        )

def ViewAlerts(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ViewAlerts.html',
        {
            'title':'View Alerts',
            'message':'Where you view your alerts',
            'year':datetime.now().year,
            }
        )

def AddAlerts(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/AddAlerts.html',
        {
            'title':'Create Alert',
            'message':'Where you create a new alert',
            'year':datetime.now().year,
            }
        )