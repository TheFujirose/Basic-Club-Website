from django.contrib import admin
from .models import SponsorshipTier, Benefit, Sponsor, Sponsorship, SponsorshipPackage

@admin.register(SponsorshipTier)
class SponsorshipTierAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)
    search_fields = ("name",)
    ordering = ("name",)


class SponsorshipInline(admin.TabularInline):
    # Edit a sponsor's sponsorships on the sponsor's own page
    model = Sponsorship
    extra = 1
    fields = ("name", "tier")


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    inlines = (SponsorshipInline,)


class SponsorshipPackageInline(admin.TabularInline):
    # Edit the benefits included in a sponsorship, per year, on the sponsorship's own page
    model = SponsorshipPackage
    extra = 1
    fields = ("year", "benefit")


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ("name", "sponsor", "tier")
    list_filter = ("tier",)
    search_fields = ("name", "sponsor__name")
    ordering = ("sponsor__name", "name")
    list_select_related = ("sponsor", "tier")

    inlines = (SponsorshipPackageInline,)


@admin.register(SponsorshipPackage)
class SponsorshipPackageAdmin(admin.ModelAdmin):
    list_display = ("sponsorship", "benefit", "year")
    list_filter = ("year", "sponsorship__tier", "benefit")
    search_fields = ("sponsorship__name", "sponsorship__sponsor__name", "benefit__name")
    ordering = ("-year", "sponsorship__name")
    list_select_related = ("sponsorship", "sponsorship__sponsor", "benefit", "year")
