from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from .models import *
import urllib.request
import requests

from .forms import ProductForm
from decimal import Decimal

from django.shortcuts import render_to_response
from django.template import RequestContext

import datetime
import json
import requests

from django.contrib.auth import logout


API_URL = "http://api.openweathermap.org/data/2.5/weather?q=Dhaka,BD&APPID=2bd83722546b07c43439188c5de4eba0"

# Create your views here.

SESSION_ID = "ABC"




def handler404(request, *args, **argv):
    response = render_to_response('YBAdminApp/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('YBAdminApp/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def bkList(request):

    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')
    else:
        bookingObj = Booking.objects.all().order_by('-EntryDate').using('yamahan')
        page = request.GET.get('page', 1)
        paginator = Paginator(bookingObj, 10)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        bookingList = list(bookingObj)
        today = datetime.date.today()
        day = today.day
        month = today.strftime("%B")
        year = today.year
        print(today)
        resp = requests.get(url=API_URL)
        data = resp.json()
        print(data['main']['temp'])
        temp = data['main']['temp'] - 273.15
        weatherDesc = data['weather'][0]['description']
        print(weatherDesc)
        humidity = data['main']['humidity']
        print('userid')
        userId = request.session['UserId']
        print(userId)

    return render(request, 'YBAdminApp/bookingList.html',
                  {'bookingList': books, 'day': day, 'month': month, 'year': year, 'temp': temp,
                   'desc': weatherDesc, 'humidity': humidity, 'userId': userId})

def Home(request):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')
    else:

        productObj = Product.objects.all().order_by('-EntryDate').using('yamahan')
        bookingCount = Booking.objects.using('yamahan').count()
        approveBookingCount = Booking.objects.filter(BookingStatus='Approve').using('yamahan').count()
        pendingBookingCount = Booking.objects.filter(BookingStatus='Pending').using('yamahan').count()
        revertBookingCount = Booking.objects.filter(BookingStatus='Revert').using('yamahan').count()
        cancelBookingCount = Booking.objects.filter(BookingStatus='Cancel').using('yamahan').count()
        page = request.GET.get('page', 1)
        print('page')
        print(page)

        paginatorPr = Paginator(productObj,10)

        productList = list(productObj)
        #form = ProductForm()
        context = {
            'a': 5
        }
        today = datetime.date.today()
        day = today.day
        month = today.strftime("%B")
        year = today.year
        print(today)
        resp = requests.get(url=API_URL)
        data = resp.json()
        print(data['main']['temp'])
        temp = data['main']['temp'] - 273.15
        weatherDesc = data['weather'][0]['description']
        print(weatherDesc)
        humidity = data['main']['humidity']
        print('userid')
        userId = request.session['UserId']
        print(userId)
        dataCheck = 0
        if(int(page) > 1):
            dataCheck = 1
    return render(request, 'YBAdminApp/index.html',
                  {'bookingCount':bookingCount,'approveBookingCount':approveBookingCount,'pendingBookingCount':pendingBookingCount,
                   'revertBookingCount':revertBookingCount,'cancelBookingCount':cancelBookingCount,
                   'day': day, 'month': month, 'year': year, 'temp': temp,
                   'desc': weatherDesc, 'humidity': humidity, 'userId':userId,'productList':productList,'dataCheck':dataCheck})


def login(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        userObj = YamahaUser.objects.using('yamahan').filter(UserId=userid).filter(Password=password).first()

        print(userObj)

        if userObj is not None and userObj.IsAdmin=='1':
            request.session['uid'] = userObj.Id
            request.session['UserId'] = userid
            request.session['Password'] = password
            request.session['UserName'] = userObj.UserName
            print(userObj.IsAdmin)
            if userid == 'admin':
                request.session['userstatus'] = 'admin'
            else:
                request.session['userstatus'] = 'general'
            if not request.session.session_key:
                request.session.save()
            global SESSION_ID
            print("Login started with session_id = " + SESSION_ID)
            print(request.session['UserId'])
            return HttpResponseRedirect('Home')
        else:
            return render(request, 'YBAdminApp/login.html',
                          {'message': 'Login Failed. Please contact system administrator.',
                           'PageTitle': 'Login Failed'})

    return render(request, 'YBAdminApp/login.html', {'message': '', 'PageTitle': 'Login'})


def product(request):

    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')

    if request.method == 'POST' and request.FILES['productImage1']:
        print(settings.STATIC_URL)
        fs = FileSystemStorage(location=settings.MEDIA_URL)
        productImage1 = request.FILES['productImage1']
        filename = fs.save(productImage1.name, productImage1)
        uploaded_file_url = fs.url(filename)
        ProductName = request.POST.get('productName')
        ProductColor = request.POST.get('productColor')
        ProductPrice = int(request.POST.get('productPrice'))  # Decimal
        MinBookingPrice = int(request.POST.get('productMinPrice'))  # Decimal
        Stock = int(request.POST.get('productStock'))  # INteger
        Status = request.POST.get('status')
        EntryDate = request.POST.get('productActiveDate')
        productLastDate = request.POST.get('productLastDate')

        print('Status')
        print(Status)

        pr = Product(ProductName=ProductName, ProductColor=ProductColor, ProductPrice=ProductPrice,
                     MinBookingPrice=MinBookingPrice, Stock=Stock, Status=Status, ProductImage1= '/media/'+filename,
                     EntryDate=EntryDate,LastBookingDate=productLastDate)

        pr.save(using='yamahan')

        return HttpResponseRedirect('/YBAdminApp/Home/')



def booking_detail(request,booking_id):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')
    #print(booking_id)
    bookingObj = Booking.objects.all().using('yamahan').filter(Id=booking_id).values('UserId__UserName','UserId__UserId','Id','UserId','ProductId__ProductName','BookingStatus','DepositAmount','EntryDate','Remarks')
    bookingPaySlipObj = BookingPaySlip.objects.all().using('yamahan').filter(BookingId=booking_id).values('Id','AccountNo','BranchName','PaySlipDoc')
    DealerLocationObj = DealerLocation.objects.all().using('yamahan').values('Id','DealerCode','DistrictId__DistrictName')
    bookingList = list(bookingObj)
    dealerLocationList = list(DealerLocationObj)
    print(bookingObj[0]['UserId'])
    RegisteredUserObj = RegisteredUser.objects.all().using('yamahan').filter(Email=bookingObj[0]['UserId__UserId']).values('Mobile','Email','DistrictId__DistrictName')
    RegisteredUserList = list(RegisteredUserObj)
    print('Registered')
    print(RegisteredUserList)
    print(bookingList[0])
    bookingPaySlipList = list(bookingPaySlipObj)
    print('BookingPaySlip')
    print(bookingPaySlipList)
    return render(request, 'YBAdminApp/bookingDetail.html',{'bookingList': bookingList,'bookingPaySlipList':bookingPaySlipList,'RegisteredUserList':RegisteredUserList,'dealerLocationList':dealerLocationList})

def product_detail(request,product_id):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')
    print(product_id)

    productObj = Product.objects.all().using('yamahan').filter(Id=product_id).values('Id','ProductName','ProductColor','ProductPrice','MinBookingPrice','Stock','Status','ProductImage1','LastBookingDate')
    productList = list(productObj)

    print(productList[0])
    lastBDate = productList[0]['LastBookingDate'].strftime('%Y-%m-%d')


    print('helllo')
    return render(request,'YBAdminApp/productDetail.html',{'productList': productList,'lastBDate':lastBDate})


def SendSMS(number, text):
   data = {'smstext': text,
           'number': number}
   r = requests.post(url='http://192.168.100.8/fifaabecab/Authenticate/sendSMS', data=data)
   return


def bookingUpdate(request):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')

    if request.method == 'POST':
        BookingId = request.POST.get('BookingId')
        BookingStatus = request.POST.get('BookingStatus')
        UserId = request.session['UserId']
        if(BookingStatus=='Approve'):
            DeliveryDate = request.POST.get('DeliveryDate')
            DPoint = request.POST.get('DeliveryPoint')

            date_time_obj = datetime.datetime.strptime(DeliveryDate, '%Y-%m-%d')
            print(date_time_obj)
            bId = Booking.objects.filter(Id=BookingId).using('yamahan')[0]
            dlId = DealerLocation.objects.filter(Id=int(DPoint)).using('yamahan')[0]
            yUser = YamahaUser.objects.filter(UserId=str(UserId)).using('yamahan')[0]

            sDate = datetime.datetime(int(DeliveryDate.split('-')[0]), int(DeliveryDate.split('-')[1]),
                                      int(DeliveryDate.split('-')[2]), 0, 0, 0, 000)

            bookingUserId = Booking.objects.filter(Id=BookingId).values('UserId').using('yamahan')[0]
            yamahaRegId = YamahaUser.objects.filter(Id=bookingUserId['UserId']).values('RegsUserId').using('yamahan')[0]
            mobileRegUser = RegisteredUser.objects.filter(Id=yamahaRegId['RegsUserId']).values('Mobile').using('yamahan')[0]

            dealerLocObj = DealerLocation.objects.filter(Id=DPoint).values('DLRPoint','FullLocation').using('yamahan')[0]
            dlrP = dealerLocObj['DLRPoint']
            dlrLoc = dealerLocObj['FullLocation']
            mobileNo = mobileRegUser['Mobile']

            text='Your YAMAHA Booking has been approved. Delivery Date: '+DeliveryDate+' Dealer Point: '+dlrP+' Address: '+dlrLoc
            m='01799993209'
            data = {'smstext': text,'number': m}
            SendSMS(mobileNo,text)
            print(data)

            #r = requests.post(url='http://192.168.100.10/fifaabecab/Authenticate/sendSMS', data=data)

            print('bookingUserId')
            print(mobileNo)
            

            dp = DeliveryPoint(BookingId=bId,DeliveryDate=sDate,IsDelivered='N',EntryBy=yUser,DealerLocationId=dlId)
            dp.save(using='yamahan')
            prId = Booking.objects.filter(Id=BookingId).using('yamahan').values('ProductId')
            
            prStock = Product.objects.filter(Id=prId[0]['ProductId']).using('yamahan').values('Stock')

            newStock = prStock[0]['Stock']-1
            Product.objects.filter(Id=prId[0]['ProductId']).using('yamahan').update(Stock=newStock)



        Booking.objects.filter(Id=BookingId).using('yamahan').update(BookingStatus=BookingStatus)
        return HttpResponseRedirect('Home')


def bkSearch(request):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')

    if request.method == 'POST':
        BookingStatus = request.POST.get('BookingStatus')

        bookingObj = Booking.objects.filter(BookingStatus=BookingStatus).order_by('-EntryDate').using('yamahan')

        bookingList = list(bookingObj)


        today = datetime.date.today()
        day = today.day
        month = today.strftime("%B")
        year = today.year
        print(today)
        resp = requests.get(url=API_URL)
        data = resp.json()
        print(data['main']['temp'])
        temp = data['main']['temp'] - 273.15
        weatherDesc = data['weather'][0]['description']
        print(weatherDesc)
        humidity = data['main']['humidity']
        print('userid')
        userId = request.session['UserId']
        print(userId)


        return render(request, 'YBAdminApp/bookingList.html',
                      {'bookingList': bookingList, 'day': day, 'month': month, 'year': year, 'temp': temp,
                       'desc': weatherDesc, 'humidity': humidity, 'userId': userId})



def productUpdate(request):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')
    if request.method == 'POST' or (request.method == 'POST' and request.FILES['productImage1']):
        ProductId = request.POST.get('ProductId')
        ProductName = request.POST.get('ProductName')
        ProductColor = request.POST.get('ProductColor')
        ProductPrice = request.POST.get('ProductPrice')
        MinBookingPrice = request.POST.get('MinBookingPrice')
        Stock = request.POST.get('Stock')
        Status = request.POST.get('status')
        productLastDate = request.POST.get('productLastDate')

        print('productLastDate')
        print(productLastDate)
        print('Status')
        print(Status)
        if Status is not None:
            Status=1
        else:
            Status=0

        if 'productImage1' in request.FILES:
            print('Both')
            fs = FileSystemStorage(location=settings.MEDIA_URL)
            productImage1 = request.FILES['productImage1']
            filename = fs.save(productImage1.name, productImage1)
            Product.objects.filter(Id=ProductId).using('yamahan').update(ProductName=ProductName,
                                                                         ProductColor=ProductColor,
                                                                         ProductPrice=ProductPrice,
                                                                         MinBookingPrice=MinBookingPrice,
                                                                         Stock=Stock, Status=Status, LastBookingDate=productLastDate,
                                                                         ProductImage1='/media/' + filename)
        else:
            Product.objects.filter(Id=ProductId).using('yamahan').update(ProductName=ProductName,
                                                                         ProductColor=ProductColor,
                                                                         ProductPrice=ProductPrice,
                                                                         MinBookingPrice=MinBookingPrice, Stock=Stock,Status=Status,LastBookingDate=productLastDate)

        return HttpResponseRedirect('Home')


def message_detail(request,booking_id):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')
    UserId = request.session['UserId']
    UserName = request.session['UserName']
    uid = request.session['uid']

    bookingObj = Booking.objects.all().using('yamahan').filter(Id=booking_id)
    messageObj = Inbox.objects.all().using('yamahan').filter(BookingId=booking_id).values('From__UserName','Id')
    messId = Inbox.objects.all().using('yamahan').filter(BookingId=booking_id).values('Id')

    print('len')
    print(len(messageObj))
    mailBox=[]
    for i in range (len(messageObj)):
        mailBox += InboxDetail.objects.filter(InboxId__Id=messId[i]['Id']).values('Message', 'InboxId__Id').using('yamahan')

    print(mailBox)
    bookingList = list(bookingObj)
    messageList = list(messageObj)
    print(messageList)

    return render(request, 'YBAdminApp/messageDetail.html', {'bookingList': bookingList,'messageList':messageList,'mailBox':mailBox, 'UserName':UserName,'UserId':UserId,'uid':uid})

def messageSend(request):
    if 'UserId' not in request.session:
        return HttpResponseRedirect('login')

    if request.method == 'POST':
        From_id = request.POST.get('FromID')
        To_id = request.POST.get('ToID')

        print('TO_ID')
        print(To_id)

        tID = YamahaUser.objects.filter(Id=To_id).using('yamahan')
        fID = YamahaUser.objects.filter(Id=From_id).using('yamahan')

        print(tID)

        BookingId = request.POST.get('BookingId')
        MessageDetail = request.POST.get('MessageDetail')

        bId = Booking.objects.filter(Id=BookingId).using('yamahan')

        inbox = Inbox(From_id=From_id,To_id=To_id,BookingId=bId[0])
        inbox.save(using='yamahan')
        inboxId = Inbox.objects.filter(Id=inbox.Id).using('yamahan')

        inboxDetail = InboxDetail(Message=MessageDetail,InboxId=inboxId[0],EntryBy=fID[0])
        inboxDetail.save(using='yamahan')
        return HttpResponseRedirect('Home')


def logoutuser(self):
    # print('userid')
    print(self.session['UserId'])

    if 'UserId' not in self.session: return HttpResponseRedirect('login')
    # # Session logout record keeping
    # global SESSION_ID

    self.session.flush()
    self.session.clear()
    del self.session
    #print(self.session)

    # try:
    #     print(request.session['UserId'])
    #
    #     del request.session
    #     # del request.session['uid']
    #     # del request.session['UserId']
    #     # del request.session['Password']
    #     # del request.session['UserName']
    #     print('del')
    # except KeyError:
    #     print('keyerror')
    #     print(request.session.session_key)
    #     pass

    return HttpResponseRedirect('login')
