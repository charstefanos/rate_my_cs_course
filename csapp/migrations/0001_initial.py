# Generated by Django 2.2.3 on 2020-03-14 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(max_length=1000)),
                ('year_in_university', models.CharField(choices=[('Undergraduate', (('UNDERGRAD_1YEAR', 'Undergraduate (year 1)'), ('UNDERGRAD_2YEAR', 'Undergraduate (year 2)'), ('UNDERGRAD_3YEAR', 'Undergraduate (year 3)'), ('UNDERGRAD_4YEAR', 'Undergraduate (year 4)'))), ('Postgraduate', (('POSTGRAD', 'Postgraduate'),))], max_length=32)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('current_student', models.BooleanField()),
                ('year_of_studies', models.CharField(blank=True, choices=[('Undergraduate', (('UNDERGRAD_1YEAR', 'Undergraduate (year 1)'), ('UNDERGRAD_2YEAR', 'Undergraduate (year 2)'), ('UNDERGRAD_3YEAR', 'Undergraduate (year 3)'), ('UNDERGRAD_4YEAR', 'Undergraduate (year 4)'))), ('Postgraduate', (('POSTGRAD', 'Postgraduate'),))], max_length=32, null=True)),
                ('contact', models.BooleanField(blank=True, null=True)),
                ('courses', models.ManyToManyField(blank=True, to='csapp.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='CourseRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', models.IntegerField(default=0)),
                ('lecturer_rating', models.IntegerField(default=0)),
                ('engagement', models.IntegerField(default=0)),
                ('informative', models.IntegerField(default=0)),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csapp.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csapp.UserProfile')),
            ],
            options={
                'verbose_name': 'Course Rating',
                'verbose_name_plural': 'Course Ratings',
            },
        ),
    ]
