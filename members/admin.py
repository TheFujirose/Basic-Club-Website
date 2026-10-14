from django.contrib import admin

from .models import (
    Participation,
    Competition_Year,
    Discipline,
    Institution,
    Platform,
    Program,
    Role,
    Skill,
    Skills_Used,
    Student,
    Student_Socials,
)

@admin.register(Discipline)
class Discipline(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(Competition_Year)
class CompetitionYearAdmin(admin.ModelAdmin):
    list_display = ("year",)


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1
    fields = ("name",)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    list_display_links = ("name",)

    fieldsets = (
        (None, {"fields": ("name",)}),
    )

    inlines=(ProgramInline,)



@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    ordering = ("name",)


class StudentSocialsInline(admin.TabularInline):
    # Edit a student's social links on the student's own page;
    # platform is a dropdown of existing Platforms (with a "+" to add one)
    model = Student_Socials
    extra = 1
    fields = ("platform", "profile_url")


class ParticipationInline(admin.TabularInline):
    # Edit a student's roster history on the student's own page
    model = Participation
    extra = 1
    fields = ("year", "discipline", "role")


class SkillsUsedInline(admin.TabularInline):
    model = Skills_Used
    extra = 1
    fields = ("year", "skill")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("student", "year", "discipline", "role")
    list_filter = ("year", "discipline", "role")
    search_fields = ("student__name", "role__name")
    ordering = ("-year", "student__name")
    list_select_related = ("student", "year", "discipline", "role")


@admin.register(Skills_Used)
class SkillsUsedAdmin(admin.ModelAdmin):
    list_display = ("student", "year", "skill")
    list_filter = ("year", "skill")
    search_fields = ("student__name", "skill__name")
    ordering = ("-year", "student__name")
    list_select_related = ("student", "year", "skill")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Columns shown on the changelist page
    list_display = ("name", "program", "graduation_date")
    list_display_links = ("name",)
    # Sidebar filters
    list_filter = ("program__institution", "program", "graduation_date")
    # Search box; "__" follows the foreign key
    search_fields = ("name", "program__name", "program__institution__name")
    ordering = ("name",)
    date_hierarchy = "graduation_date"
    # Join Program/Institution in one query instead of one query per row
    list_select_related = ("program", "program__institution")
    list_per_page = 50

    # Layout of the add/edit form
    fieldsets = (
        (None, {"fields": ("name", "program")}),
        ("Details", {"fields": ("graduation_date", "image_url")}),
    )

    inlines = (StudentSocialsInline, ParticipationInline, SkillsUsedInline)

