from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import date, datetime, timedelta
from crewcal.models import DateEntry
from crewcal.utils import transpose_dates, get_calendar_for_date_range

def home(request):
    return render(request, "home.html")

@login_required
def cal_home(request):
    #if request.method == "GET" and request.GET.get("goto"):
    #    print(f"has goto: {request.GET.get('goto')}")
    if request.method == "GET":
        if (request.GET.get("datefrom") and request.GET.get("dateto")):
            datefrom = date.fromisoformat(request.GET.get("datefrom"))
            dateto = date.fromisoformat(request.GET.get("dateto"))
        else:
            datetimefrom = datetime.now()
            dateto = datetimefrom + timedelta(days=7)
            dateto  = dateto.date()
            datefrom  = datetimefrom.date()
        
        if (request.GET.get('goto')):
            if request.GET.get('goto') == "prev_week":
                datefrom = datefrom - timedelta(days=7)
                dateto = dateto - timedelta(days=7)
            elif request.GET.get('goto') == "next_week":
                datefrom = datefrom + timedelta(days=7)
                dateto = dateto + timedelta(days=7)
        
        #get jobs which belong to users workgroup
        jobs = DateEntry.objects.filter(
            job__company_workgroup = request.user.userprofile.company_workgroup
            ).filter(
                date__range=[datefrom, dateto]
                ).order_by('date').order_by('crew')
        #rebuild the data structure to display per crew
        jobs_transposed_by_crew ={
            '0':
                transpose_dates(datefrom),
            '1':  
                get_calendar_for_date_range(request, datefrom, dateto),
                
            }




        profile = request.user.userprofile
    else: # PUT
        pass
    
    data = {
        "datefrom" : datefrom,
        "dateto" : dateto,
        "jobs" : jobs,
        "jobs_transposed_by_crew" : jobs_transposed_by_crew,

    }
    return render(request, "calhome.html", data)

@login_required
def restricted_page(request):
    data = {
        'title' : 'Restricted Page',
        'content' : '<h1>You are logged in</h1>',
    }
    
    return render(request, "general.html", data)