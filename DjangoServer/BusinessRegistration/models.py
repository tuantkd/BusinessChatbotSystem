from django.db import models

class Companies(models.Model):
    CompanyID = models.CharField(max_length=255, primary_key=True)
    CompanyName = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    CityProvince = models.CharField(max_length=255)
    Capital = models.BigIntegerField()
    Phone = models.CharField(max_length=255)
    LegalRepresentative = models.CharField(max_length=255)
    IssuedDate = models.DateField()
    BusinessType = models.CharField(max_length=255)

class MainBusinessActivities(models.Model):
    MainActivityCode = models.IntegerField()
    MainActivityName = models.CharField(max_length=255)
    CompanyID = models.ForeignKey(Companies, on_delete=models.CASCADE)

class BusinessActivities(models.Model):
    ActivityCode = models.IntegerField()
    ActivityName = models.CharField(max_length=255)
    CompanyID = models.ForeignKey(Companies, on_delete=models.CASCADE)

class Addresses(models.Model):
    Address = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    CityProvince = models.CharField(max_length=255)
    CompanyID = models.ForeignKey(Companies, on_delete=models.CASCADE)

class Contacts(models.Model):
    Phone = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Fax = models.CharField(max_length=255)
    CompanyID = models.ForeignKey(Companies, on_delete=models.CASCADE)

class BusinessTypes(models.Model):
    TypeDescription = models.CharField(max_length=255)
    CompanyID = models.ForeignKey(Companies, on_delete=models.CASCADE)
