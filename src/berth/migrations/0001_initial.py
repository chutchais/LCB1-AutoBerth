# Generated by Django 3.2.4 on 2021-06-15 11:32

import colorfield.fields
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
            name='Service',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('color', colorfield.fields.ColorField(default='#CCFFFF', max_length=18)),
                ('move_performa', models.IntegerField(default=0, verbose_name='Move Performa')),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Deactive')], default='A', max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('start_range', models.CharField(blank=True, max_length=2, null=True, verbose_name='Excel start range')),
                ('stop_range', models.CharField(blank=True, max_length=2, null=True, verbose_name='Excel stop range')),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Deactive')], default='A', max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vessel',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('lov', models.IntegerField(default=100, verbose_name='Lenght of Vessel')),
                ('imo', models.CharField(blank=True, max_length=20, null=True, verbose_name='IMO number')),
                ('v_type', models.CharField(choices=[('VESSEL', 'Vessel'), ('BARGE', 'Barge'), ('NOTICE', 'Notice')], default='VESSEL', max_length=10, verbose_name='Vessel Type')),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Deactive')], default='A', max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voy', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('start_pos', models.IntegerField(default=50, verbose_name='Start Position')),
                ('performa_in', models.DateTimeField(blank=True, null=True)),
                ('performa_out', models.DateTimeField(blank=True, null=True)),
                ('move_performa', models.IntegerField(default=0, verbose_name='Move Performa')),
                ('move_confirm', models.BooleanField(default=False, verbose_name='Move Confirm')),
                ('eta', models.DateTimeField(blank=True, null=True, verbose_name='ETA')),
                ('etb', models.DateTimeField(blank=True, null=True, verbose_name='ETB')),
                ('etd', models.DateTimeField(blank=True, null=True, verbose_name='ETD')),
                ('qc', models.CharField(blank=True, max_length=20, null=True, verbose_name='Q')),
                ('dis_no', models.IntegerField(default=0, verbose_name='Discharge')),
                ('load_no', models.IntegerField(default=0, verbose_name='Loading')),
                ('est_teu', models.IntegerField(default=0, verbose_name='Est TEU')),
                ('vsl_oper', models.CharField(blank=True, max_length=20, null=True, verbose_name='Vsl Operator')),
                ('arrival_draft', models.CharField(blank=True, default=0, max_length=50, null=True, verbose_name='Arrival draft')),
                ('departure_draft', models.CharField(blank=True, default=0, max_length=50, null=True, verbose_name='Departure draft')),
                ('remark', models.TextField(blank=True, max_length=255, null=True)),
                ('draft', models.BooleanField(default=False, verbose_name='Saved as Draft')),
                ('text_pos', models.CharField(choices=[('R', 'Right'), ('L', 'Left'), ('T', 'Top'), ('B', 'Buttom')], default='R', max_length=1, verbose_name='Text position for Barge')),
                ('next_date', models.IntegerField(default=14, verbose_name='Next arrive date')),
                ('imp_release_date', models.DateTimeField(blank=True, null=True, verbose_name='Import Release Date')),
                ('export_cutoff_date', models.DateTimeField(blank=True, null=True, verbose_name='Export Cutoff Date')),
                ('inverse', models.BooleanField(default=False, verbose_name='Inverse 180')),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='berth.service')),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='berth.terminal')),
                ('vessel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='berth.vessel')),
            ],
        ),
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_name', models.CharField(max_length=100)),
                ('current_week', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('next_week', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('remark', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cutoff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dry_date', models.DateTimeField(blank=True, null=True, verbose_name='Dry CutOff')),
                ('reef_date', models.DateTimeField(blank=True, null=True, verbose_name='Reef CutOff')),
                ('chilled_date', models.DateTimeField(blank=True, null=True, verbose_name='Chilled CutOff')),
                ('durian_date', models.DateTimeField(blank=True, null=True, verbose_name='Durian/Longan CutOff')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('remark', models.TextField(blank=True, max_length=255, null=True)),
                ('voy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='berth.voy')),
            ],
        ),
    ]
