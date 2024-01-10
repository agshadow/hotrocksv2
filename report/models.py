from django.db import models

# Create your models here.

class IncidentTypeChoice(models.TextChoices):
    INJURY = "I"
    HAZARD = "H"
    VARIATION = "V"
    NONCONFORMANCE = "N"
    IMPROVEMENT = "M"
    OTHER = "O"

    
class IncidentReport(models.Model):
    incident_type = models.CharField(max_length=1, choices=IncidentTypeChoice.choices)
    incident_date = models.DateTimeField()
    site = models.CharField(max_length=50)
    date_reported = models.DateField(auto_now=True, null=True)
    reported_by = models.CharField(max_length=50)
    reported_to = models.CharField(max_length=50, null=True)
    witness_name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=300)
    root_cause = models.CharField(max_length=300, null=True)
    action_taken = models.CharField(max_length=300, null=True)
    sign_off = models.CharField(max_length=50)
    sign_off_date = models.DateField()
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #add multiple pictures
    #add rest of fields
    
    def __str__(self):
        return (f"Incident Report: (\nid={self.id}\n"\
        f"incident_type={self.incident_type}\n"\
        f"incident_date={self.incident_date}\n"\
        f"site={self.site}\n"\
        f"description={self.description}\n"\
        f")"
        )

    class Meta:
        ordering = ["incident_date",]


class IncidentReportFiles(models.Model):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100,blank=True, null=True)
    file = models.FileField(blank=True, null=True)