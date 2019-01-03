from django.db import models
from django.db import connection, connections
import json
import datetime
import urllib
from sqlserver_ado.fields import LegacyDateField, LegacyDateTimeField
from sqlserver_ado.fields import DateField, DateTimeField, TimeField

from django.db import models
from django.db import connection, connections

from django.urls import reverse,reverse_lazy

# Create your models here.

class District(models.Model):
    Id = models.AutoField(primary_key=True, db_column='DistrictID')
    DistrictCode = models.CharField(max_length=50, db_column='DistrictCode')
    DistrictName = models.CharField(max_length=100, db_column='DistrictName', null=False)
    DivisionId = models.IntegerField(db_column='DivisionID', null=False)

    class Meta:
        managed = False
        db_table = 'district'

    def __str__(self):
        return '{}, {}'.format(self.Id, self.DistrictName)

class DealerLocation(models.Model):
   Id = models.AutoField(primary_key=True, db_column='Id')
   DealerCode = models.CharField(max_length=50, db_column='DealerCode')
   DLRPoint = models.CharField(max_length=200, db_column='DLRPoint')
   NameOfDealer = models.CharField(max_length=200, db_column='NameOfDealer')
   OwnerContactNo = models.CharField(max_length=200, db_column='OwnerContactNo')
   LocationCode = models.CharField(max_length=200, db_column='LocationCode')
   Latitude = models.DecimalField(decimal_places=8, max_digits=18, db_column='Latitude')
   Longitude = models.DecimalField(decimal_places=8, max_digits=18, db_column='Longitude')
   Email = models.CharField(max_length=100, db_column='Email')
   FullLocation = models.CharField(max_length=100, db_column='FullLocation')
   DistrictId = models.ForeignKey(District, db_column='DistrictId', on_delete=models.CASCADE)

   class Meta:
       managed = False
       db_table = 'DealerLocation'

   def __str__(self):
       return '{}, {}'.format(self.Id, self.DealerCode)



class Product(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    ProductName = models.CharField(max_length=50, db_column='ProductName', null=False)
    ProductColor = models.CharField(max_length=50, db_column='ProductColor', null=False)
    ProductPrice = models.DecimalField(max_digits=10,decimal_places=0, db_column='ProductPrice', null=False)
    MinBookingPrice = models.DecimalField(max_digits=10,decimal_places=0, db_column='MinBookingPrice', null=False)
    Stock = models.IntegerField(db_column='Stock', null=False)
    Status = models.CharField(max_length=10,db_column='Status',null=False)
    ProductImage1 = models.CharField(max_length=255, db_column='ProductImage1', null=False)
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    LastBookingDate = models.DateTimeField(auto_now_add=False, db_column='LastBookingDate')

    def get_absolute_url(self):
        return reverse('YBAdminApp:product_detail', kwargs={'product_id':self.Id})

    class Meta:
        managed = False
        db_table = 'Product'

    def __str__(self):
        return '{}, {}'.format(self.Id, self.ProductName, self.ProductPrice, self.MinBookingPrice)


class ProductBookingPeriod(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Period = models.IntegerField(db_column='Period', null=False)
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    ProductId = models.ForeignKey(Product, db_column='ProductId', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ProductBookingPeriod'

    def __str__(self):
        return '{}, {}'.format(self.Id, self.Period, self.ProductId, self.EditDate)


class RegisteredUser(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    UserName = models.CharField(max_length=255, db_column='UserName')
    Mobile = models.CharField(max_length=255, db_column='Mobile')
    Email = models.CharField(max_length=255, db_column='Email', unique=True)
    IsUsed = models.CharField(max_length=10, db_column='IsUsed', default='N')
    Status = models.CharField(max_length=10, db_column='Status', default='1')
    Remark = models.CharField(max_length=255, db_column='Remark', default='1')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    DistrictId = models.ForeignKey(District, db_column='DistrictId', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'RegisteredUser'

    def __str__(self):
        return '{}, {}'.format(self.Id, self.UserName, self.Mobile, self.Mobile, self.Email)


class OTPMessage(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    OtpCode = models.CharField(max_length=255, db_column='OtpCode')
    IsUsed = models.CharField(max_length=10, db_column='IsUsed', default='N')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    RegisteredUser = models.ForeignKey(RegisteredUser, db_column='RegisteredUser', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'OTPMessage'


class YamahaUser(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    UserId = models.CharField(max_length=255, db_column='UserId')
    UserName = models.CharField(max_length=255, db_column='UserName')
    Password = models.CharField(max_length=255, db_column='Password')
    IsAdmin = models.CharField(max_length=10, db_column='IsAdmin', default='0')
    Status = models.CharField(max_length=10, db_column='Status', default='Y')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    RegsUserId = models.ForeignKey(RegisteredUser, db_column='RegsUserId', on_delete=models.CASCADE,default=100)

    class Meta:
        #managed = False
        db_table = 'YamahaUser'


class DepositBankInfo(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    BankAccountName = models.CharField(max_length=255, db_column='BankAccountName')
    AccountNo = models.CharField(max_length=255, db_column='AccountNo')
    BranchName = models.CharField(max_length=255, db_column='BranchName')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    class Meta:
        managed = False
        db_table = 'DepositBankInfo'


class Booking(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    UserId = models.ForeignKey(YamahaUser, db_column='UserId', on_delete=models.CASCADE)
    IsAgree = models.CharField(max_length=5, db_column='IsAgree')
    ProductId = models.ForeignKey(Product, db_column='ProductId', on_delete=models.CASCADE)
    BookingStatus = models.CharField(max_length=100, db_column='BookingStatus', default='Pending')
    DepositAmount = models.DecimalField(decimal_places=8, max_digits=10, db_column='DepositAmount', null=False)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    Remarks = models.CharField(max_length=255, db_column='Remarks', default='1')


    def get_absolute_url(self):
        return reverse('YBAdminApp:booking_detail', kwargs={'booking_id':self.Id})

    def get_absolute_url_message(self):
        return reverse('YBAdminApp:message_detail', kwargs={'booking_id': self.Id})


    class Meta:
        managed = False
        db_table = 'Booking'

class BookingPaySlip(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    BankAccountName = models.CharField(max_length=255, db_column='BankAccountName')
    AccountNo = models.CharField(max_length=255, db_column='AccountNo')
    BranchName = models.CharField(max_length=255, db_column='BranchName')
    DepositBank = models.ForeignKey(DepositBankInfo, db_column='DepositBankId', on_delete=models.CASCADE)
    PaySlipDoc =  models.CharField(max_length=255, db_column='PaySlipDoc', null=False)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    BookingId =  models.ForeignKey(Booking, db_column='BookingId', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'BookingPaySlip'


class DeliveryPoint(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    BookingId = models.ForeignKey(Booking, db_column='BookingId', on_delete=models.CASCADE)
    IsDelivered = models.CharField(max_length=100, db_column='IsDelivered', default='N')
    DeliveryDate = models.DateTimeField(auto_now_add=True, db_column='DeliveryDate')
    EntryBy = models.ForeignKey(YamahaUser, db_column='EntryBy', on_delete=models.CASCADE)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    DealerLocationId = models.ForeignKey(DealerLocation, db_column='DealerLocation', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'DeliveryPoint'


class Inbox(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    From = models.ForeignKey(YamahaUser, db_column='From_id', on_delete=models.CASCADE)
    To = models.ForeignKey(YamahaUser, related_name="Inbox_To", on_delete=models.CASCADE)
    BookingId = models.ForeignKey(Booking, db_column='BookingId', on_delete=models.CASCADE)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    class Meta:
        managed = False
        db_table = 'Inbox'


class InboxDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Message = models.CharField(max_length=255, db_column='MessageDetail')
    InboxId = models.ForeignKey(Inbox, db_column='InboxId', on_delete=models.CASCADE)
    EntryBy = models.ForeignKey(YamahaUser, db_column='EntryBy', on_delete=models.CASCADE)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    class Meta:
        managed = False
        db_table = 'InboxDetail'
