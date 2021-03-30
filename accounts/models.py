import os
import uuid
from os.path import splitext
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

alphanumeric = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters are allowed.')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


def unique_file_path(instance, filename):
    instance.original_file_name = filename
    base, ext = splitext(filename)
    newname = "%s%s" % (uuid.uuid4(), ext)
    return os.path.join('photos', newname)


class Semester(models.Model):
    sem = (
    ('Btech 1st', 'Btech 1st'), ('Btech 2nd', 'Btech 2nd'), ('Btech 3rd', 'Btech 3rd'), ('Btech 4th', 'Btech 4th'),
    ('Btech 5th', 'Btech 5th'), ('Btech 6th', 'Btech 6th'), ('Btech 7th', 'Btech 7th'), ('Btech 8th', 'Btech 8th'))

    semester = models.CharField(blank=True, null=True, max_length=10, choices=sem)
    id = models.IntegerField(blank=True, unique=True, primary_key=True)

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def __str__(self):
        return self.semester


class Subject(models.Model):
    id = models.AutoField
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=10, validators=[alphanumeric])
    description = models.TextField(max_length=1000)
    img = models.ImageField(upload_to=unique_file_path, default="")

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.subject_name


class Unit(models.Model):
    uni = (('Unit 1', 'Unit 1'), ('Unit 2', 'Unit 2'), ('Unit 3', 'Unit 3'), ('Unit 4', 'Unit 4'), ('Assignment', 'Assignment'))

    unit = models.CharField(blank=True, null=True, max_length=10, choices=uni)
    id = models.IntegerField(blank=True, unique=True, primary_key=True)

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return self.unit


class Notes(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    date = models.DateField(auto_now_add=True)
    file_upload = models.FileField(upload_to=unique_file_path)
    uploaded_by = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.name