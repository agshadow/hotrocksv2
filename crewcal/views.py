from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import date, datetime, timedelta
from crewcal.models import DateEntry

@login_required
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
        
        #get jobs which belong to users workgroup
        jobs = DateEntry.objects.filter(
            job__company_workgroup = request.user.userprofile.company_workgroup
            ).filter(
                date__range=[datefrom, dateto]
                ).order_by('date').order_by('crew')
        #rebuild the data structure to display per crew
        jobs_transposed_by_crew ={
            '0':
                {'0':"", 
                '1': "1 feb",
                '2': "2 feb",
                '3': "3 feb",
                '4': "4 feb",
                '5': "5 feb",
                '6': "6 feb",
                '7': "7 feb",
                },
            '1': 
                {'0': 
                    {'0': "Jeff",
                    '1': "",
                    '2': "Hibiscus",
                    '3': "Hibuscus",
                    '4': "",
                    '5': "Grange",
                    '6': "Grange",
                    '7': "",
                    },
                }
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