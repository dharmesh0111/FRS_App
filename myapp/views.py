from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Invoice
from django.urls import reverse


# Create your views here


#user name for access aproval1 and aproval2 page
User1 = "approvalUser1"
User2 = "approvalUser2"

def index(request):
    return render(request,"login.html")


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        us = request.POST['username']
        e = request.POST['email']
        n = request.POST['name']
        pas = request.POST['password']

        user = User.objects.filter(username=us)
        mil = User.objects.filter(email=e)

        if user.exists():
            messages.error(request, "username already taken!")
            return redirect('/register')

        if mil.exists():
            messages.error(request, "Email id already exists!")
            return redirect('/register')

        u = User.objects.create(email=e, first_name=n, username=us)
        u.set_password(pas)
        u.save()
        messages.error(request, 'Account created successfully')
        return redirect('/login')


def login_page(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username!')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password!')
            return redirect('/login')

        else:
            login(request, user)
            messages.error(request, 'Logged in successfully!')
            if str(request.user) == User1:
                return redirect("/invoices/")
            if str(request.user) == User2:
                return redirect("/invoices/approval2/")
            else:
                messages.error(request, 'user dont have access!!')
                return redirect("/login")


def logout_page(request):
    logout(request)
    messages.error(request, 'Logged out successfully')
    return redirect('/')

def invoice(request):
    if request.user.is_authenticated:
        if str(request.user) == User1:
            # User is logged in, fetch all invoices
            invoices = Invoice.objects.all()

            # Calculate the subtotal or use the updated value
            for invoice in invoices:
                # Check if the `sub_total` has been updated manually
                if not invoice.sub_total:  # If sub_total is empty or None
                    invoice.sub_total = invoice.invoice_amt + invoice.tds
                    invoice.save()
                    
            
            return render(request, 'approval1.html', {'invoices': invoices})
        else:
            messages.error(request, "approval1 only has access.")
            return redirect("/")
    else:
        # Redirect unauthenticated users to the login page
        messages.error(request, "Please log in to access the invoice page.")
        return redirect('/login')

    

def statusAPP1(request, id, code):
    # Fetch the invoice record using the ID
    invoice = get_object_or_404(Invoice, id=id)
    mess =""
    
    # Update the 'approval1' column based on the button pressed
    if code == 1:
        # Approve the invoice
        invoice.approval1 = "Approved"
        mess = "aproval succesfull"
    else:
        # Reject the invoice
        invoice.approval1 = "Rejected"
        mess = "aproval rejected"

    
    # Save the updated invoice record
    invoice.save()
    messages.error(request, mess)
    # Redirect back to the invoice list page
    return redirect('http://127.0.0.1:8000/invoices/')


def statusAPP2(request, id, code):
    # Fetch the invoice record using the ID
    invoice = get_object_or_404(Invoice, id=id)
    mess = ""

    # Update the 'approval2' column based on the button pressed
    if code == 1 :
        # Approve the invoice
        invoice.approval2 = "Approved"
        mess = "Approval successful"
    else:
        # Reject the invoice
        invoice.approval2 = "Rejected"
        mess = "Approval rejected"

    # Save the updated invoice record
    invoice.save()

    # Display success or failure message
    messages.error(request, mess) if code == "1" else messages.warning(request, mess)

    # Redirect to the invoice list page using reverse
    return redirect("http://127.0.0.1:8000/invoices/approval2/")


def aproval2(request):
    if request.user.is_authenticated:
        if(str(request.user) ==User2):
            invoices = Invoice.objects.filter(approval1 = "Approved")
            return render(request,"approval2.html",{'invoices': invoices})
        else:
            messages.error(request, "approval2 only has the access")
            return redirect("/")

def comment(request, id):
    # Fetch the invoice object based on the given id
    invoice = get_object_or_404(Invoice, id=id)
    
    if request.method == "POST":
        # Get the comment from the POST request
        user_comment = request.POST.get('comment', '').strip()
        if user_comment:  # Ensure comment is not empty
            # Update the commentsAPP1 column in the database
            invoice.commentsAPP1 = user_comment
            invoice.save()
            messages.error(request, "Comment updated successfully for Approval 1.")
        else:
            messages.error(request, "Comment cannot be empty for Approval 1.")
        return redirect(reverse('invoices'))  # Replace 'invoices' with your named URL for the invoices page
    else:
        # For GET requests, handle Approval 2 comments
        user_comment = request.GET.get('comment', '').strip()
        if user_comment:  # Ensure comment is not empty
            # Update the commentsAPP2 column in the database
            invoice.commentsAPP2 = user_comment
            invoice.save()
            messages.error(request, "Comment updated successfully for Approval 2.")
        else:
            messages.error(request, "Comment cannot be empty for Approval 2.")
        return redirect("http://127.0.0.1:8000/invoices/approval2/")  # Replace 'invoices_approval2' with your named URL
    


def subAmt(request, id):
    # Fetch the invoice object based on the given ID
    invoice = get_object_or_404(Invoice, id=id)
    
    if request.method == "POST":
        # Get the subamt value from the POST request
        user_subamt = request.POST.get('subamt', '').strip()
        if user_subamt:  # Ensure the value is not empty
            try:
                # Update the sub_total column in the database
                invoice.sub_total = float(user_subamt)
                invoice.save()
                messages.error(request, "Sub Total updated successfully!")
            except ValueError:
                messages.error(request, "Invalid input. Please enter a valid number.")
        else:
            messages.error(request, "Sub Total cannot be empty.")
    
    return redirect(reverse('invoices'))  # Redirect to the invoices page