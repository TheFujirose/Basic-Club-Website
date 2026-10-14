from django.db import models


class Institution(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Program(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # We don't want to delete if child rows exist
    institution = models.ForeignKey(Institution, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    graduation_date = models.DateField()
    image_url = models.URLField()
    program = models.ForeignKey(
        Program,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.name

class Platform(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    icon = models.URLField()

    def __str__(self):
        return self.name

class Student_Socials(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Socials belong to the student, so remove them with the student
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    # Don't delete a platform while students still link to it
    platform = models.ForeignKey(
        Platform,
        on_delete=models.RESTRICT
    )
    profile_url = models.URLField()

    class Meta:
        verbose_name = "Student Social"
        verbose_name_plural = "Student Socials"

class Discipline(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Competition_Year(models.Model):
    year = models.SmallIntegerField(primary_key=True)

    class Meta:
        verbose_name = "Competition Year"
        verbose_name_plural = "Competition Years"

    def __str__(self):
        return str(self.year)

class Skill(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skills_Used(models.Model):
    # Plain id instead of a composite key so the admin can register it
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.ForeignKey(Competition_Year, on_delete=models.RESTRICT)
    skill = models.ForeignKey(Skill, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Skills Used"
        verbose_name_plural = "Skills Used"
        # A student lists each skill once per year
        constraints = (
            models.UniqueConstraint(
                fields=("student", "year", "skill"),
                name="unique_skills_used_student_year_skill",
            ),
        )

    def __str__(self):
        return f"{self.student} - {self.skill} ({self.year})"

class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Participation(models.Model):
    # Plain id instead of a composite key so the admin can register it
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.ForeignKey(Competition_Year, on_delete=models.RESTRICT)
    discipline = models.ForeignKey(Discipline, on_delete=models.RESTRICT)
    # Optional; left blank for members without a specific role.
    # Don't delete a role while roster entries still use it
    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participation"
        # A student is on the roster once per year
        constraints = (
            models.UniqueConstraint(
                fields=("student", "year"),
                name="unique_club_roster_student_year",
            ),
        )

    def __str__(self):
        return f"{self.student} ({self.year})"
