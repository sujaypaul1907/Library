from Library.forms import IssueBookForm
from django.shortcuts import redirect, render, HttpResponse
from django.template import loader
from django.urls import reverse
from Library.forms import BookForm
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author'] 
        fees = request.POST['fees']
        quantity = request.POST['quantity']

        books = Book.objects.create(name=name, author=author, fees=fees, quantity=quantity)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html")

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_members(request):
    members = Member.objects.all()
    return render(request, "view_members.html", {'members':members})

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.member_id = request.POST['name2']
            obj.fees = request.POST['fees2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*50
        books = list(models.Book.objects.filter(fees=i.fees))
        members = list(models.Member.objects.filter(user=i.member_id))
        i=0
        for l in books:
            t=(members[i].user,members[i].user_id,books[i].name,books[i].fees,issuedBooks[0].issued_date,issuedBooks[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/member_login')
def member_issued_books(request):
    member = Member.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(member_id=member[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(fees=i.fees)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>31:
            day=d-30
            fine=day*50
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request,'member_issued_books.html',{'li1':li1, 'li2':li2})

@login_required(login_url = '/member_login')
def profile(request):
    return render(request, "profile.html")

def edit_book(request, myid):  
    update_book = Book.objects.get(id=myid) 
    return render(request,'edit_book.html', {'update_book':update_book})  


def update(request, myid):      
    update2 = Book.objects.get(id=myid)
    form = BookForm(request.POST, instance = update2)  
    if form.is_valid():  
        form.save()  
        alert = True
        return redirect("/view_books/", {'alert':alert})  
    return render(request, '/edit_book.html', {'update2': update2}) 


def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def delete_member(request, myid):
    members = Member.objects.filter(id=myid)
    members.delete()
    return redirect("/view_members")



def member_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "member_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        member = Member.objects.create(user=user, phone=phone, image=image)
        user.save()
        member.save()
        alert = True
        return render(request, "member_registration.html", {'alert':alert})
    return render(request, "member_registration.html")

def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a member!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "member_login.html", {'alert':alert})
    return render(request, "member_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/view_members")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")