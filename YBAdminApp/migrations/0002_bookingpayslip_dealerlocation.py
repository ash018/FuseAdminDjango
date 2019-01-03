# Generated by Django 2.0.4 on 2018-12-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YBAdminApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingPaySlip',
            fields=[
                ('Id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('BankAccountName', models.CharField(db_column='BankAccountName', max_length=255)),
                ('AccountNo', models.CharField(db_column='AccountNo', max_length=255)),
                ('BranchName', models.CharField(db_column='BranchName', max_length=255)),
                ('PaySlipDoc', models.CharField(db_column='PaySlipDoc', max_length=255)),
                ('EntryDate', models.DateTimeField(auto_now_add=True, db_column='EntryDate')),
            ],
            options={
                'managed': False,
                'db_table': 'BookingPaySlip',
            },
        ),
        migrations.CreateModel(
            name='DealerLocation',
            fields=[
                ('Id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('DealerCode', models.CharField(db_column='DealerCode', max_length=50)),
                ('DLRPoint', models.CharField(db_column='DLRPoint', max_length=200)),
                ('NameOfDealer', models.CharField(db_column='NameOfDealer', max_length=200)),
                ('OwnerContactNo', models.CharField(db_column='OwnerContactNo', max_length=200)),
                ('LocationCode', models.CharField(db_column='LocationCode', max_length=200)),
                ('Latitude', models.DecimalField(db_column='Latitude', decimal_places=8, max_digits=18)),
                ('Longitude', models.DecimalField(db_column='Longitude', decimal_places=8, max_digits=18)),
                ('Email', models.CharField(db_column='Email', max_length=100)),
                ('FullLocation', models.CharField(db_column='FullLocation', max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'DealerLocation',
            },
        ),
    ]