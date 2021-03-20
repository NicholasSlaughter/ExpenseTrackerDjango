"""
Definition of views.
"""

from datetime import datetime, timedelta
import pytz
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib import messages
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
            #try:
            expense_to_save.save()

            alerts_to_update = Alert.objects.filter(category=expense_to_save.category)

            if alerts_to_update.exists():
                amount_to_update = float(expense_to_save.amount)
                utc=pytz.UTC
                today = datetime.now()
                today = utc.localize(today)

                for alert in alerts_to_update:
                    #Sets the new period start date
                    if alert.period_end_date < today:
                        new_start_of_period = datetime.now()
                        if(alert.period.name == "Week"):
                            if new_start_of_period.weekday() != 6:
                                new_start_of_period = new_start_of_period + timedelta(days= (6-new_start_of_period.weekday()))
                                new_start_of_period = new_start_of_period - timedelta(days=7)

                                alert.period_start_date = new_start_of_period
                                alert.period_end_date = new_start_of_period + timedelta(days=6)

                                alert.current_amount = amount_to_update
                        elif(alert.period.name == "Month"):
                            if new_start_of_period.day != 1:
                                new_start_of_period = datetime(new_start_of_period.year,new_start_of_period.month,day=1,hour=1,minute=1,second=1)

                                alert.period_start_date = new_start_of_period
                                alert.period_end_date = datetime(year=new_start_of_period.year,month=(new_start_of_period.month+1),day=1,hour=1,minute=1,second=1)

                                alert.current_amount = amount_to_update
                        else:
                            if new_start_of_period.month != 1 and new_start_of_period.day != 1:
                                new_start_of_period = datetime(year=new_start_of_period.year,month=1,day=1,hour=1,minute=1,second=1)

                                alert.period_start_date = new_start_of_period
                                alert.period_end_date = datetime(year=new_start_of_period.year+1,month=new_start_of_period.month,day=1,hour=1,minute=1,second=1)

                                alert.current_amount = amount_to_update
                    else:
                        alert.current_amount += amount_to_update

                    if float(alert.current_amount) > float(alert.max_amount):
                        messages.success(request, 'You are currently over your ' + alert.period.name + 'ly limit for ' + alert.category.name)


                    alert.save()

            categories_to_display = Category.objects.all()
            return render(
                request,
                'app/EnterExpense.html',
                {
                    'title':'Enter Expense',
                    'page_message':'Where you enter expenses',
                    'year':datetime.now().year,

                    'expense': Expense,
                    'category': categories_to_display,
                    }
                )
            #except:
            #    print("Error can't save")
    else:
        categories_to_display = Category.objects.all()
        return render(
            request,
            'app/EnterExpense.html',
            {
                'title':'Enter Expense',
                'page_message':'Where you enter expenses',
                'year':datetime.now().year,

                'expense': Expense,
                'category': categories_to_display,
                }
            )

def History(request):
    assert isinstance(request, HttpRequest)

    if request.method=="POST":
        if request.POST.get('order_type'):
            expenses = Expense.objects.all()
            order_of_list = request.POST.get('order_type')
            if order_of_list == "Newest - Oldest":
                expenses = expenses.order_by('date')
            elif order_of_list == "Oldest - Newest":
                expenses = expenses.order_by('-date')
            elif order_of_list == "Highest Amount - Lowest Amount":
                expenses = expenses.order_by('-amount')
            elif order_of_list == "Lowest Amount - Highest Amount":
                expenses = expenses.order_by('amount')
            else:
                expenses = expenses.order_by('category__name')

        return render(
            request,
            'app/History.html',
            {
                'title':'Expense History',
                'message':'Where you view your history of expenses',
                'year':datetime.now().year,
                'expenses': expenses,
                'sort': order_of_list,
                'post_called': True,
                }
            )

    else:
        expenses = Expense.objects.all()
        return render(
            request,
            'app/History.html',
            {
                'title':'Expense History',
                'message':'Where you view your history of expenses',
                'year':datetime.now().year,
                'expenses': expenses,
                'sort': None,
                'post_called': False,
                }
            )

def ViewAlerts(request):
    assert isinstance(request, HttpRequest)
    alerts=Alert.objects.all()
    return render(
        request,
        'app/ViewAlerts.html',
        {
            'title':'View Alerts',
            'message':'Where you view your alerts',
            'year':datetime.now().year,
            'alerts':alerts,
            }
        )

def AddAlerts(request):
    assert isinstance(request, HttpRequest)

    if request.method=="POST":
        if request.POST.get('category_name') and request.POST.get('alert_amount') and request.POST.get('period_name'):
            period_selected = str(request.POST.get('period_name'))

            alert_to_save = Alert()
            alert_to_save.max_amount = request.POST.get('alert_amount')
            alert_to_save.current_amount = 0
            alert_to_save.period_start_date = datetime.now()

            if period_selected == "Week":
                alert_to_save.period_end_date = datetime.now() + timedelta(weeks=1)
            elif period_selected == "Month":
                alert_to_save.period_end_date = datetime.now() + timedelta(weeks=4)
            else:
                alert_to_save.period_end_date = datetime.now() + timedelta(days=365)

            alert_to_save.category = Category.objects.get(name=request.POST.get('category_name'))
            alert_to_save.period = Period.objects.get(name=request.POST.get('period_name'))
            try:
                alert_to_save.save()
                categories_to_display = Category.objects.all()
                period_to_display = Period.objects.all()
                return render(
                    request,
                    'app/AddAlerts.html',
                    {
                        'title':'Create Alert',
                        'message':'Where you create a new alert',
                        'year':datetime.now().year,

                        'alert': Alert,
                        'category': categories_to_display,
                        'period': period_to_display,
                        }
                    )
            except:
                print("Error can't save")
    else:
        categories_to_display = Category.objects.all()
        period_to_display = Period.objects.all()
        return render(
            request,
            'app/AddAlerts.html',
            {
                'title':'Create Alert',
                'message':'Where you create a new alert',
                'year':datetime.now().year,

                'alert': Alert,
                'category': categories_to_display,
                'period': period_to_display,
                }
            )