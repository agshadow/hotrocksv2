from django.shortcuts import render
from report.models import IncidentReport
from django.core.paginator import Paginator


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
    print(all_reports)
    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_reports, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)
    print(f"page object list {page.object_list}")
    data = {
        "reports": page.object_list,
        "page": page,
    }

    return render(request, "list_reports.html", data)

def view_report(request, report_id):
    data = {
        "report": f"report {report_id}",
    }
    print(data)
    return render(request, "view_report.html", data)