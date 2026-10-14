from django.db import models
from members import models as member

class SponsorshipTier(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Benefit(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sponsorship(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sponsor = models.ForeignKey(
        Sponsor,
        on_delete=models.RESTRICT
    )
    tier = models.ForeignKey(
        SponsorshipTier,
        on_delete=models.RESTRICT
    )  
    def __str__(self):
        return self.name

class SponsorshipPackage(models.Model):
    id = models.BigAutoField(primary_key=True)
    benefit = models.ForeignKey(
        Benefit,
        on_delete=models.RESTRICT
    )
    sponsorship = models.ForeignKey(
        Sponsorship,
        on_delete=models.RESTRICT
    )
    year = models.ForeignKey(
        member.Competition_Year,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return str(self.benefit) + " " + str(self.sponsorship) + " (" + str(self.year) + ")"