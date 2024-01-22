from datetime import date, timedelta

from crewcal.models import DateEntry

def transpose_dates(datefrom = date.today()):
    transposed = {}
    
    for x in range(0,8):
        if x == 0:
            transposed.update({str(x) : ""})
        else:
            transposed.update({str(x): 
                               (datefrom + timedelta(days=x-1))
                               .strftime("%a, %b %d").replace(" 0"," ")
            })
    #print("exiting transpose_dates()")
    #print (transposed)

    return transposed

def get_calendar_for_date_range(request, datefrom = date.today(), dateto = date.today()):
    #print(f"user profileworkgroup: {request.user.userprofile.company_workgroup}")
    jobs = DateEntry.objects.filter(
    job__company_workgroup = request.user.userprofile.company_workgroup
    ).filter(
        date__range=[datefrom, dateto]
        ).order_by('date').order_by('crew')
    #print(f"----------jobs {datefrom} - {dateto}------------")
    #get unique crews from data
    crews = []
    for job in jobs:
        if job.crew not in crews:
            #print(f"{job.crew} not in crews")
            crews.append(job.crew)
    #print(f"crews : {crews}")
    jobs_to_return = {}

    for counter, crew in enumerate(crews):
        #print(counter)
        crew_jobs={"0":crew}
        for n in range(int((dateto - datefrom).days) + 1):
            current_date= datefrom + n * timedelta(days=1)
            #print(f"{n+1}", current_date.strftime("%Y-%m-%d"))
            job_name=""
            for job in jobs:
                if job.date == current_date and job.crew == crew:  
                    #print(f"found job : {job.job.name} - {job.date}")
                    job_name = job.job.name
            crew_jobs.update({str(n+1): job_name})
        #print (counter,crew_jobs)  
        jobs_to_return.update( {str(counter) : crew_jobs})
    #print(jobs_to_return)
    return jobs_to_return