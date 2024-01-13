from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import date, datetime, timedelta
from crewcal.models import DateEntry

def home(request):
    if request.method == "GET":
        if (request.GET.get("datefrom") and request.GET.get("dateto")):
            datefrom = date.fromisoformat(request.GET.get("datefrom"))
            dateto = date.fromisoformat(request.GET.get("dateto"))
            
        else:
            datetimefrom = datetime.now()
            dateto = datetimefrom + timedelta(days=7)
            dateto  = dateto.date()
            datefrom  = datetimefrom.date()
        
        jobs = DateEntry.objects.filter(date__range=[datefrom, dateto])

    else: # PUT
        pass
    
    data = {
        "datefrom" : datefrom,
        "dateto" : dateto,
        "jobs" : jobs,
    }
    return render(request, "calhome.html", data)

@login_required
def restricted_page(request):
    data = {
        'title' : 'Restricted Page',
        'content' : '<h1>You are logged in</h1>',
    }
    
    return render(request, "general.html", data)