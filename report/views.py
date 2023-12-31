from django.shortcuts import render, get_object_or_404, get_list_or_404
from report.models import IncidentReport, IncidentTypeChoice
from django.core.paginator import Paginator
from datetime import datetime, timezone
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core import serializers
from report.forms import IncidentReportForm

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
        print("----------------IN GET ----------------")
        if report_id == 0:
            print("--------new report created")
            form = IncidentReportForm()
        else:
            print("--------using existing form")
            form = IncidentReportForm(instance=report)

    else: #POST
        print("----------------IN POST ----------------")
        print(f"report id: {report_id}")
        if report_id == 0:
            print("--------new report about to create")
            #report = IncidentReport.objects.create(
             #   incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
              #  sign_off_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),)
            report = IncidentReport()
            print("--------new report created")
            print(report)
        print(f"print report again: {report}")
        form = IncidentReportForm(request.POST, request.FILES, instance=report)

        print(f"check if form valid {form.is_valid()}")
        if form.is_valid():
            report = form.save()
            print("saved form")

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
    print(report)
    data = serializers.serialize( "python", report )
    print(data[0])
    print(data[0]['fields'].get('incident_type'))
    print(f"incident type label hard coded: {IncidentTypeChoice('I').label}")
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(20, 800, f"Incident Report:  {data[0]['pk']}")
    hval=780
    for key,value in data[0]['fields'].items():
        if key == "incident_type":
            print(f"incident type: {key}:{value}")
            value = IncidentTypeChoice(value).label
            print(f"value: {value}")
        p.drawString(20, hval, f"{key} : {value}")
        print (f"{key} : {value} : {hval}")
        hval -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')