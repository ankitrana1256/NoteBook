# Generated by Django 3.1.7 on 2021-03-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_subject_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit',
            field=models.CharField(blank=True, choices=[('Unit 1', 'Unit 1'), ('Unit 2', 'Unit 2'), ('Unit 3', 'Unit 3'), ('Unit 4', 'Unit 4'), ('Assignment', 'Assignment')], max_length=10, null=True),
        ),
    ]
