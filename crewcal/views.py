from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import date, timedelta
from crewcal.models import DateEntry, Job

from crewcal.utils import (
    transpose_dates,
    get_calendar_for_date_range,
    start_of_week,
    check_if_date_is_sunday,
    _get_items_per_page,
    _get_page_num,
)

from crewcal.forms import DateEntryForm, JobForm, DateEntryForm1, DateEntryForm2


def home(request):
    return render(request, "home.html")


@login_required
def cal_home(request):
    # if request.method == "GET" and request.GET.get("goto"):
    #    print(f"has goto: {request.GET.get('goto')}")
    if request.method == "GET":
        if request.GET.get("datefrom"):
            print("has datefrom ")
            datefrom = date.fromisoformat(request.GET.get("datefrom"))
            if not check_if_date_is_sunday(datefrom):
                datefrom = start_of_week(datefrom)
            dateto = datefrom + timedelta(days=7)
            print(f"datefrom: {datefrom}  dateto: {dateto}")
        else:
            today = date.today()
            datefrom = start_of_week(today)

            dateto = datefrom + timedelta(days=7)

        if request.GET.get("goto"):
            if request.GET.get("goto") == "prev_week":
                datefrom = datefrom - timedelta(days=7)
                dateto = dateto - timedelta(days=7)
            elif request.GET.get("goto") == "next_week":
                datefrom = datefrom + timedelta(days=7)
                dateto = dateto + timedelta(days=7)

        # get jobs which belong to users workgroup
        jobs = (
            DateEntry.objects.filter(
                job__company_workgroup=request.user.userprofile.company_workgroup
            )
            .filter(date__range=[datefrom, dateto])
            .order_by("date")
            .order_by("crew")
        )
        # rebuild the data structure to display per crew
        jobs_transposed_by_crew = {
            "0": transpose_dates(datefrom),
            "1": get_calendar_for_date_range(request, datefrom, dateto),
        }

    else:  # PUT
        pass

    data = {
        "datefrom": datefrom,
        "dateto": dateto,
        "jobs": jobs,
        "jobs_transposed_by_crew": jobs_transposed_by_crew,
    }
    return render(request, "calhome.html", data)


@login_required
def restricted_page(request):
    data = {
        "title": "Restricted Page",
        "content": "<h1>You are logged in</h1>",
    }

    return render(request, "general.html", data)


def cal_update(request, job_id):
    if request.method == "GET":
        if request.GET.get("datefrom") and request.GET.get("dateto"):
            job = get_object_or_404(DateEntry, id=job_id)
            form = DateEntryForm(instance=job)
        else:
            raise Http404("Dates not valid")

    else:  # POST
        job = get_object_or_404(DateEntry, id=job_id)
        form = DateEntryForm(request.POST, instance=job)
        if form.is_valid():
            form.save()

            parm = f"?datefrom={request.GET['datefrom']}"
            return redirect(reverse("cal_home") + parm)

    data = {
        "form": form,
    }
    return render(request, "update.html", data)


@login_required
def create_job(request):
    if request.method == "GET":
        initial_values = {
            "company_workgroup": request.user.userprofile.company_workgroup
        }
        job_form = JobForm(initial=initial_values)
    else:  # POST
        job_form = JobForm(request.POST)

        if job_form.is_valid():
            job_form = job_form.save()
            return redirect("view_jobs")

    data = {
        "heading": "Create Job",
        "form": job_form,
    }
    return render(request, "create.html", data)


def get_sunday(d):
    """Return the Sunday of the week containing the date d."""
    return d - timedelta(days=d.weekday() + 1 if d.weekday() != 6 else 0)


@login_required
def create_shift(request):
    if request.method == "POST":
        date_form = DateEntryForm1(request.POST, user=request.user)
        if date_form.is_valid():
            date_form.save_multiple_entries()
            # Extract the submitted date from the form data
            submitted_date = date_form.cleaned_data["date"]

            # Redirect to the calendar home page with the submitted date
            return redirect(
                reverse("cal_home") + f"?datefrom={submitted_date.isoformat()}"
            )
    else:
        date_form = DateEntryForm1(user=request.user)

    data = {
        "heading": "Create Date",
        "form": date_form,
    }
    return render(request, "create_shift.html", data)


def job_search(request):
    search_term = request.GET.get("search_term", "")
    jobs = Job.objects.filter(name__icontains=search_term)
    job_list = [{"id": job.id, "name": job.name, "number": job.number} for job in jobs]
    return JsonResponse({"jobs": job_list})


@login_required
def create_date_entry(request):
    if request.method == "POST":
        form = DateEntryForm2(request.user, request.POST)
        if form.is_valid():
            # Save the form and handle the success logic
            date_entry = form.save()
            return redirect("success_view")  # Redirect to a success view or URL
    else:
        form = DateEntryForm2(request.user)

    return render(request, "create_date_entry.html", {"form": form})


def view_jobs(request):
    all_jobs = Job.objects.filter(
        company_workgroup=request.user.userprofile.company_workgroup
    ).order_by("name")
    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_jobs, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)
    data = {
        "reports": page.object_list,
        "page": page,
    }

    return render(request, "view_jobs.html", data)


def update_job(request, report_id):
    pass


def delete_job(request, report_id):
    pass


@login_required
def read_shift(request):
    # all_shifts = DateEntry.objects.all().order_by("date")
    # objects.filter(company_workgroup=request.user.userprofile.company_workgroup).
    user_profile = request.user.userprofile
    all_shifts = DateEntry.objects.filter(
        job__company_workgroup=user_profile.company_workgroup
    ).order_by("date")

    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_shifts, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)
    data = {
        "reports": page.object_list,
        "page": page,
    }

    return render(request, "read_shift.html", data)


def update_shift(request, report_id):
    pass


@login_required
def delete_shift(request, report_id):
    # Retrieve the DateEntry object or return a 404 error if not found
    shift = get_object_or_404(DateEntry, id=report_id)

    # Ensure the user is allowed to delete this shift
    user_profile = request.user.userprofile
    if shift.job.company_workgroup != user_profile.company_workgroup:
        messages.error(request, "You do not have permission to delete this shift.")
        return redirect("read_shift")  # Redirect to the shifts list or appropriate page

    # If the user has permission, delete the shift
    shift.delete()
    messages.success(request, "Shift deleted successfully.")
    return redirect("read_shift")  # Redirect to the shifts list or appropriate page
