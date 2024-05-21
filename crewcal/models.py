from django.db import models
from django.contrib.auth.models import User


class Workgroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CompanyWorkgroup(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    workgroup = models.ForeignKey(Workgroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("company", "workgroup")

    def __str__(self):
        return f"{self.company} - {self.workgroup}"


class Job(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    company_workgroup = models.ForeignKey(CompanyWorkgroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"Job: {self.name} ({self.number}) at {self.location}"

    class Meta:
        ordering = ["name", "number"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["number"]),
        ]


class DateEntry(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date = models.DateField()
    crew = models.CharField(max_length=50)
    notes = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"DateEntry ID: {self.id}, Job: {self.job.name}, Date: {self.date}, Crew: {self.crew}"

    class Meta:
        ordering = ["date", "job__name"]
        verbose_name = "Date Entry"
        verbose_name_plural = "Date Entries"
        indexes = [
            models.Index(fields=["date"]),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_workgroup = models.ForeignKey(CompanyWorkgroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
