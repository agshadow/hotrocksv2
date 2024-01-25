from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from report.models import IncidentReport, IncidentTypeChoice, IncidentReportFiles
from django.core.paginator import Paginator
import io

import uuid
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core import serializers
from report.forms import IncidentReportForm, ReadOnlyIncidentReportForm, UpdateIncidentReportForm, \
    IncidentReportFileForm

def _get_items_per_page(request):
    # Determine how many items to show per page, disallowing <1 or >50
    items_per_page = int(request.GET.get("items_per_page", 10))
    if items_per_page < 1:
        items_per_page = 10
    if items_per_page > 50:
        items_per_page = 50

    return items_per_page

def _get_page_num(request, paginator):
    # Get current page number for Pagination, using reasonable defaults
    page_num = int(request.GET.get("page", 1))

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    return page_num

def list_reports(request):
    all_reports = IncidentReport.objects.all().order_by("incident_date")
    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_reports, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)
    data = {
        "reports": page.object_list,
        "page": page,
    }

    return render(request, "list_reports.html", data)

def view_report(request, report_id=0):
    if report_id != 0:
        report = get_object_or_404(IncidentReport, id = report_id)
    
    if request.method == "GET":
        if report_id == 0:
            form = IncidentReportForm()
        else:
            form = IncidentReportForm(instance=report)

    else: #POST
        if report_id == 0:
            #report = IncidentReport.objects.create(
             #   incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
              #  sign_off_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),)
            report = IncidentReport()
        form = IncidentReportForm(request.POST, request.FILES, instance=report)

        if form.is_valid():
            report = form.save()

    #report.incident_type = IncidentTypeChoice(report.incident_type).label
    data = {
        "form": form,
    }
    return render(request, "view_report.html", data)

def pdf_report(request, report_id):
    # Create a file-like buffer to receive PDF data.
    if report_id != 0:
        report = get_list_or_404(IncidentReport, id = report_id)
    else:
        return redirect("list_reports")
    data = serializers.serialize( "python", report )
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(20, 800, f"Incident Report:  {data[0]['pk']}")
    hval=780
    for key,value in data[0]['fields'].items():
        if key == "incident_type":
            value = IncidentTypeChoice(value).label
        p.drawString(20, hval, f"{key} : {value}")
        hval -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')

def new_report(request):

    if request.method == "GET": 
        incident_report_form = IncidentReportForm()
        incident_report_file_form = IncidentReportFileForm()
    else: #POST      
        incident_report_form = IncidentReportForm(request.POST, request.FILES)



        if incident_report_form.is_valid() :
            incident_report_form = incident_report_form.save()
            report = IncidentReport.objects.get(id = incident_report_form.id)
            if request.FILES != {}:
                f = request.FILES['file'].name
                request.FILES['file'].name = str(uuid.uuid4())
                #incident_report_file_form = IncidentReportFileForm(request.POST, request.FILES, instance=report)
                IncidentReportFiles.objects.create(
                    incident_report = report,
                    filename = f, 
                    file=request.FILES['file'])
            return redirect("list_reports")
        
    data = {
        "incident_report_form": incident_report_form,
        "incident_report_file_form" : incident_report_file_form,
    }
    return render(request, 'new.html', data)

def detail(request, report_id):
    report = get_object_or_404(IncidentReport, id = report_id)
    files = IncidentReportFiles.objects.filter(incident_report = report)
    form = ReadOnlyIncidentReportForm(instance=report)
           
    data = {
        "form": form,
        "files": files,
    }
    return render(request, 'detail.html', data)


def update(request, report_id):
    report = get_object_or_404(IncidentReport, id = report_id)
    
    if request.method == "GET":
        form = UpdateIncidentReportForm(instance=report)
    else: # POST
        form = UpdateIncidentReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect("list_reports")
           
    data = {
        "form": form,
    }
    return render(request, "update.html", data)


def delete(request, report_id):
    report = get_object_or_404(IncidentReport, id=report_id)
    report.delete()
    return redirect("list_reports")


def delete_confirmation(request, report_id):
    report = get_object_or_404(IncidentReport, id=report_id)
    report.incident_type = IncidentTypeChoice(report.incident_type).label
    data = {
        'report' : report
    }
    return render(request, "delete_confirmation.html", data)
