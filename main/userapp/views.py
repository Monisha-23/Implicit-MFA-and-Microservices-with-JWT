from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse
from numpy.lib.function_base import select
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .serializers import *
from .models import *
import hashlib
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect, render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from PIL import Image
import imagehash
from .models import *
import tkinter as tk
from hashlib  import md5
from django.contrib.auth import logout
from django.contrib import messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import random
import json
from django.contrib.auth import login,logout
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required


# Create your views here.
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('sniff.red.23@gmail.com', 'sniffer_23')

def check(lst):
    if(len(set(lst)) == len(lst)):
        print(lst)
    else:
       create()

def create():
    a = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
    global lst
    lst = [0,0,0,0,0,0,0]
    for i in range(len(lst)):
        if i == 0:
            p = random.randint(1,25)
            lst.insert(0,p)
        else:
            if lst[i-1] in a[0]:
                x = random.choice(a[1])
                lst[i] = x
            elif lst[i-1] in a[1]:
                r = random.choice([0,2])
                x = random.choice(a[r])
                lst[i] = x
            elif lst[i-1] in a[2]:
                r = random.choice([1,3])
                x = random.choice(a[r])
                lst[i] = x
            elif lst[i-1] in a[3]:
                r = random.choice([2,4])
                x = random.choice(a[r])
                lst[i] = x
            elif lst[i-1] in a[4]:
                x = random.choice(a[3])
                lst[i] = x
    check(lst)

class App:
    def __init__(self,root):
        self.root = root
        self.left = False
        self.right = False
        self.middle = False
        

        f = tk.Frame(width=200,height=200,bg="black")
        f.pack()

        f.bind("<Button-1>",self.onAnyofTwoPressed)
        f.bind("<Button-2>",self.onAnyofTwoPressed)
        f.bind("<Button-3>",self.onAnyofTwoPressed)
        f.bind("<Double-Button-1>",self.doublePressed)
        f.bind("<Double-Button-2>",self.doublePressed)
        f.bind("<Double-Button-3>",self.doublePressed)
        f.bind("<ButtonRelease-1>",self.resetPressedState)
        f.bind("<ButtonRelease-2>",self.resetPressedState)
        f.bind("<ButtonRelease-3>",self.resetPressedState)
        f.bind("<MouseWheel>", self.mouse_wheel)
    
    def onAnyofTwoPressed(self,event):
        if event.num == 1:
            print("Left Pressed")
            ar.append(11)
        if event.num == 3:
            print("Right Pressed")
            ar.append(13)
        if event.num == 2:
            print("Middle Pressed")
            ar.append(12)
        

    def doublePressed(self,event):
        if event.num == 1:
            print("Left Double Pressed")
            ar.append(21)
        if event.num == 3:
            print("Right Double Pressed")
            ar.append(23)
        if event.num == 2:
            print("Middle Double Pressed")
            ar.append(22)

    def resetPressedState(self,event):
        self.left = False
        self.right = False
        self.middle = False

    def mouse_wheel(self,event):
        count = 0
        if event.num == 5 or event.delta == -120:
            count -= 1
            ar.append(count)
        if event.num == 4 or event.delta == 120:
            count += 1
            ar.append(count)
        label['text'] = count

def home(request):
    return render(request,"choose.html")
    
def signup1(request):
    if request.method == 'GET':
        return render(request,'signup1.html')
    else:
        myfile = request.FILES['myfile']
        username = request.POST.get('username')
        email = request.POST.get('email')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        hash = imagehash.average_hash(Image.open(myfile))
        mes = str(hash)
        res = hashlib.md5(mes.encode())
        user = MyUser.objects.create(username=username,document=uploaded_file_url,hashcode=res.hexdigest(),email=email)
        user.save()
        return redirect("signup2",user.id)

           
def signup2(request,id):
    user = get_object_or_404(MyUser,id=id)
    return render(request,"signup2.html",{'user':user})


def mouse(request,id):
    user = get_object_or_404(MyUser,id=id)
    root = tk.Tk()
    global label
    global ar
    ar = []
    label = tk.Label(root,font=('courier', 18, 'bold'), width=10)
    label.pack(padx=10, pady=10)
    app = App(root)
    root.after(30000, lambda: root.destroy())
    root.mainloop()
    print(ar)
    return redirect("fill",user.id)


def fill(request,id):
    user = get_object_or_404(MyUser,id=id)
    if request.method == 'POST':
        m = ''
        if (len(ar)) > 0:
            for i in range(len(ar)):
                    m += str(ar[i])
            a = md5(m.encode("utf-8")).hexdigest()
            user.mouse = a
            user.save()  
            url = 'http://127.0.0.1:5000/api/api/register'
            myobj = {
                    "username": user.username,
                    "password": user.hashcode,
                    "email":user.email
            }
            x = requests.post(url, data = myobj)
            print(x.text)
            login(request,user)
            return redirect('index',user.id)
        else:
            messages.error(request,"Clicks not detected !")
        return redirect('signup2',user.id)
    else:
        return redirect('signup2',user.id)     


def login1(request):
    if request.method == 'GET':
        return render(request,'login1.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        if MyUser.objects.filter(username=username,email=email).exists():
            user = MyUser.objects.get(username=username,email=email)
            if 'mouse' in request.POST:
                return redirect('login2',user.id)
            elif 'image' in request.POST:
                return redirect('login3',user.id)
            else:
                messages.error(request,"Please upload correct image")
            return redirect('login1')
        else:
            messages.error(request,"Username doesn't exists !")  
            return redirect('login1')


def login2(request,id):
    user = get_object_or_404(MyUser,id=id)
    return render(request,"login2.html",{'user':user})

def login3(request,id):
    user = get_object_or_404(MyUser,id=id)
    if request.method == "GET":
        return render(request,"login3.html",{'user':user})
    else:
        myfile = request.FILES['myfile']
        hash = imagehash.average_hash(Image.open(myfile))
        mes = str(hash)
        res = hashlib.md5(mes.encode())
        res = res.hexdigest()
        if user.hashcode == res:
            login(request,user)
            return redirect('index',user.id)
        else:
            messages.error(request,"Please Upload Correct Image!")
        return redirect('login3',user.id)

def mouse_check(request,id):
    user = get_object_or_404(MyUser,id=id)
    root = tk.Tk()
    global label
    global ar
    ar = []
    label = tk.Label(root,font=('courier', 18, 'bold'), width=10)
    label.pack(padx=10, pady=10)
    app = App(root)
    root.after(30000, lambda: root.destroy())
    root.mainloop()
    return redirect("check",user.id)

def check(request,id):
    user = get_object_or_404(MyUser,id=id)
    if request.method == 'POST':
        # ar = []
        m = ''
        if (len(ar)) > 0:
            for i in range(len(ar)):
                m += str(ar[i])
            a = md5(m.encode("utf-8")).hexdigest()
            if user.mouse == a:
                login(request,user)
                return redirect('index',user.id)
            else:
               messages.error(request,"Incorrect Clicks!")
            return redirect('login2',user.id) 
        else:
            messages.error(request,"No Clicks Detected!")
        return redirect('login2',user.id)
    else:
        return redirect('login2',user.id)   

@login_required
def verify_mail(request,id):
    user = get_object_or_404(MyUser,id=id)
    return render(request,"mail.html",{'user':user})

# @login_required
def index(request,id):
    user = get_object_or_404(MyUser,id=id)
    return render(request,"home.html",{'user':user})

@login_required
def logoutuser(request,id):
    user = get_object_or_404(MyUser,id=id)
    logout(request)
    return redirect('home')

def create(lst):
    a = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
    for i in range(len(lst)):
        if i == 0:
            p = random.randint(1,25)
            lst.insert(0,p)
        else:
            if lst[i-1] in a[0]:
                x = random.choice(a[1])
                lst[i] = x
            elif lst[i-1] in a[1]:
                r = random.choice([0,2])
                x = random.choice(a[r])
                lst[i] = x
            elif lst[i-1] in a[2]:
                r = random.choice([1,3])
                x = random.choice(a[r])
                lst[i] = x
            elif lst[i-1] in a[3]:
                r = random.choice([2,4])
                x = random.choice(a[r])
                lst[i] = x
            elif lst[i-1] in a[4]:
                x = random.choice(a[3])
                lst[i] = x
    if(len(set(lst)) != len(lst)):
        return create(lst)
    else:
        return lst 

def send_email(request,id,subject="Python Notification",text=""):
    user = get_object_or_404(MyUser,id=id)
    l = [0,0,0,0]
    ls = create(l)
    print(ls)
    o = '-'.join(str(v) for v in ls)
    user.otp = o
    user.save()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text)) 
    msg = ("Hello,there. \n  " + o + "This is your OTP.")
    to = [user.email]
    smtp.sendmail(from_addr="sniff.red.23@gmail.com",to_addrs=to, msg=msg)
    print(request,"Email sent")
        
@login_required
def pattern(request,id):
    user = get_object_or_404(MyUser,id=id)
    if request.method == 'POST':
        val = request.POST.get("value")
        val = val + "-0"
        count = 0
        if user.otp == val:
            user.otp = ""
            user.save()
            url = 'http://127.0.0.1:5000/token/'
            myobj = {
                "username": user.username,
                "password": user.hashcode,
            }
            x = requests.post(url, data = myobj)
            da = json.loads(x.text)
            ur = 'http://127.0.0.1:5000/api/token/refresh'
            myob = {
                     "refresh" : da['refresh']
            }
            y = requests.post(ur, data = myob)
            data = json.loads(y.text)
            return render(request,"list_acc.html",{'user':user,'data':data})
        else:
            messages.error(request,"No Clicks Detected!")
        return render(request,"pattern.html",{'user':user})
    else:
       return render(request,"pattern.html",{'user':user})



class UserAPIView(APIView):
    def get(self,request):
        users = MyUser.objects.all()
        return Response([self.formatUser(p) for p in users])

    def formatUser(self,user):
        accounts  = requests.get('http://127.0.0.1:5000/api/users/%d/accounts' % user.id).json()
        return {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'accounts': accounts
        }

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@login_required
def user_create(request, pk):
    profile = get_object_or_404(MyUser, pk=pk)
    serializer = UserSerializer(profile)
    return render(request,'account.html',{'profile':profile,'serializer':serializer})

@login_required
def user_post(request,pk):
    profile = get_object_or_404(MyUser, pk=pk)
    post_id = request.POST.get("post_id")
    acc_num = request.POST.get("acc_num")
    id_pro = request.POST.get("id_pro")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    url = 'http://127.0.0.1:5000/api/accounts'
    myobj = {
            "post_id": post_id,
            "acc_holder": acc_num,
            "phone":phone,
            "email":email,
            "address":address,
            "proof":id_pro,
            "type":request.POST['type'],
        }
    x = requests.post(url, data = myobj)
    data = json.loads(x.text)
    if x.status_code == 400:
        messages.error(request,"Your Account Has Not Been Created. Please Try Again !")
    else:
        messages.success(request,"Your Account Has Been Created !")
    return render(request,'account.html',{'profile':profile,'data':data})

@login_required
def login_acc(request,pk):
    profile = get_object_or_404(MyUser, pk=pk)
    if request.method == "GET":
        return render(request,'login_acc.html',{'profile':profile})
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        if MyUser.objects.filter(username=username,email=email).exists():
            user = MyUser.objects.get(username=username,email=email)
            send_email(request,user.id)
            return redirect('pattern',user.id)
        else:
            messages.error("Invalid Credentials !")
    return render(request,'login_acc.html',{'profile':profile})


