from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime
import os
import random
from home import models

# Create your views here.
def index(request):
    context = {}
    if request.GET.get("invalidusr"):
        context["invalidusr"] = "Invalid Email or Password!"
    
    if request.session.get("email"):
        email = request.session.get("email")
        context["login"] = 1
        user = models.user.objects.filter(email=email)
        context["name"] = user[0].name
        context["profile_img"] = user[0].profile_img
        context["email"] = email

    packages = models.package.objects.all()
    context["packages"] = packages
    context["rating"] = [1,2,3,4,5]
    
    return render(request,"index.html", context)

def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    userInfo = models.user.objects.filter(email=email)
    if len(userInfo) > 0:
        if check_password(password, userInfo[0].password):
            request.session["email"] = email
            return redirect("/")
        else:
            return redirect("/?invalidusr=true")
    else:
        return redirect("/?invalidusr=true")

def logout(request):
    del request.session["email"]
    return redirect("/")

def profilePage(request):
    if request.session.get("email"):
        email = request.session.get("email")
        user = models.user.objects.get(email=email)
        booking = models.booking.objects.filter(user=user.id)
        packages = models.package.objects.all()
        context = {
            "packages":packages,
            "booking":booking,
            "user":user
        }
        return render(request, "profile.html", context)
    else:
        return redirect("/")
    
def settings_Page(request):
    if request.session.get("email"):
        email = request.session.get("email")
        user = models.user.objects.get(email=email)
        context = {
            "user":user,
        }
        return render(request, "edit.html", context)
    else:
        return redirect("/")

def settings_edit(request):
    if request.session.get("email"):
        email = request.session.get("email")
        name = request.POST.get("name")
        country = request.POST.get("country")
        user = models.user.objects.get(email=email)
        user.name = name
        user.country = country
        if request.FILES['profile_img']:
            profile_img = request.FILES['profile_img']
            file_ext = profile_img.name.split('.')[-1]
            new_file_name = f'p-{user.id}.{file_ext}'
            upload_dir = os.path.join(settings.BASE_DIR, 'static/images/user/')
            new_file_path = os.path.join(upload_dir, new_file_name)
            
            if user.profile_img != 'images/user/profile.png':
                old_file_path = os.path.join(settings.BASE_DIR, 'static/', user.profile_img)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            
            with open(new_file_path, 'wb+') as destination:
                for chunk in profile_img.chunks():
                    destination.write(chunk)
            
            user.profile_img = '/static/images/user/'+new_file_name
        user.save()
        
        return redirect("/profile/")
    else:
        return redirect("/")

def contact(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    subject = request.POST["subject"]
    message = request.POST["message"]
    models.contact(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message).save()
    return HttpResponse("<script>alert('Thank you for contacting us you will receive an reply email soon');open('/','_self');</script>")

# Signup
def signup(request):
    context = {}
    if request.GET.get("emailUsed"):
        context["emailUsed"] = 1
    return render(request, "signup.html", context)

def signup_request(request):
    # Getting Form data
    firstName = request.POST.get("firstName")
    lastName = request.POST.get("lastName")
    name = firstName + ' ' + lastName
    email = request.POST.get("email")
    country = request.POST.get("country")
    password = request.POST.get("password")

    # Checking all users for same email case
    Users = models.user.objects.all()
    invalidEmail = False
    for n in range(len(Users)):
        if Users[n].email == email:
            invalidEmail = True
            break

    # Redirecting if email exists
    if invalidEmail:
        return redirect("/signup/?emailUsed=true")
    else:
        # Deleting old OTP if exist
        OTPs = models.signup.objects.filter(email=email)
        if OTPs.exists():
            OTPs.delete()
        # Creating new user record
        otp = ""
        for n in range(6):
            otp += str(random.randint(0,9))
        
        newOTP = models.signup(name=name, email=email, OTP=otp, password=make_password(password), country=country)
        newOTP.save()
        send_mail(
            'Vista Pakistan Email Verification',
            f"Hey {firstName} {lastName}! Thanks for choosing Vista Pakistan. Here is the OTP for your Email Verification: {otp}. Please don't share it with some else. Thanks again for joining us.",
            'moeezrazaseven@gmail.com',
            [email],
            fail_silently=False,
        )
        # newUser = home.models.user(name = f"{firstName} {lastName}", email = email, password = password, country = country, profile_img = "/static/images/user/profile.svg")
        # newUser.save()

        return redirect(f"/signup/email-verification/?email={email}")

def signup_otp_page(request):
    email = request.GET.get("email")
    invalid = ""
    if request.GET.get("invalid"):
        invalid = "You have entered an invalid OTP, Try Again!"
    context = {
        "email" : email,
        "invalid" : invalid
    }
    return render(request, "emailVerify.html", context)

def otp_verify(request):
    email = request.GET.get("email")
    otp = ""
    otp += str(request.POST.get("digit-1"))
    otp += str(request.POST.get("digit-2"))
    otp += str(request.POST.get("digit-3"))
    otp += str(request.POST.get("digit-4"))
    otp += str(request.POST.get("digit-5"))
    otp += str(request.POST.get("digit-6"))

    OTPs = models.signup.objects.filter(email=email)
    for n in OTPs:
        if otp == n.OTP:
            name = n.name
            password = n.password
            country = n.country
            newUser = models.user(name = name, email = email, password = password, country = country, profile_img = "/static/images/user/profile.svg")
            newUser.save()
            OTPs.delete()
            request.session["email"] = email
            return redirect("/")
        else:
            return redirect(f"/signup/email-verification/?email={email}&invalid=true")

# Forget Password
def forget_password(request):
    context = {"error":False}
    if request.GET.get("error"):
        context["error"] = True

    return render(request, "forget.html", context)

def forget_password_request(request):
    email = request.POST.get("email")
    user = models.user.objects.filter(email=email)
    if len(user) > 0:
        OTP_already = models.otp.objects.filter(email=email)
        if len(OTP_already) > 0:
            OTP_already.delete()
        otp = ""
        for i in range(6):
            otp += str(random.randint(0,9))
        
        newOTP = models.otp(email=email, OTP=otp)
        newOTP.save()
        send_mail(
            'Vista Pakistan Password Reset',
            f"Hey! Here is the OTP for your password reset: {otp}. Please don't share it with some else. If you haven't make this request then ignore it. Thanks for joining us and trusting us.",
            'moeezrazaseven@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect(f"/forget/verify/?email={email}")
    else:
        return redirect("/forget/?error=1")

def forget_otp_page(request):
    email = request.GET.get("email")
    context = {
        "email" : email,
        "passReset" : 1
    }
    if request.GET.get("invalid"):
        context["invalid"] = "You have entered an invalid OTP, Try Again!"
    return render(request, "emailVerify.html", context)

def otp_check(request):
    email = request.GET.get("email")
    enterOTP = ""
    enterOTP += str(request.POST.get("digit-1"))
    enterOTP += str(request.POST.get("digit-2"))
    enterOTP += str(request.POST.get("digit-3"))
    enterOTP += str(request.POST.get("digit-4"))
    enterOTP += str(request.POST.get("digit-5"))
    enterOTP += str(request.POST.get("digit-6"))
    sendedOTP = models.signup.objects.filter(email=email)
    if sendedOTP[0].OTP == enterOTP:
        request.session["otp"] = sendedOTP[0].OTP
        # return render(request, "newPassword.html", context)
        return redirect(f"/forget/new-password/?email={email}")
    else:
        return redirect(f"/forget/verify/?email={email}&invalid=true")

def new_password(request):
    email = request.GET.get("email")
    savedOTP = models.otp.objects.filter(email=email)
    if request.session["otp"] and len(savedOTP) > 0:
        html = ""
        if savedOTP[0].OTP == request.session["otp"]:
            context = {
                "email" : email
            }
            return render(request, "newPassword.html", context)
        else:
            html = """
                <html>
                <head>
                <title>Session expired</title>
                </head>
                <body>
                <script>
                alert("Invalid URL, You are not allowed to open this page.");
                open("/", "_self");
                </script>
                </body>
                </html>
                """
        return HttpResponse(html)
    else:
        html = """
            <html>
            <head>
            <title>Session expired</title>
            </head>
            <body>
            <script>
            alert("Your OTP session has been expired, Please try again!");
            open("/", "_self");
            </script>
            </body>
            </html>
            """
        return HttpResponse(html)

def new_password_set(request):
    password = request.POST.get("password")
    email = request.GET.get("email")
    savedOTP = models.otp.objects.filter(email=email)
    if request.session.get("otp") and savedOTP:
        html = ""
        if savedOTP[0].OTP == request.session["otp"]:
            userList = models.user.objects.all()
            user = None
            for u in userList:
                if u.email == email:
                    user = u
                    break
            user.password = make_password(password)
            print(user)
            user.save()
            del request.session["otp"]
            savedOTP.delete()
            return redirect("/")
        else:
            html = """
                <html>
                <head>
                <title>Session expired</title>
                </head>
                <body>
                <script>
                alert("Invalid URL, You are not allowed to open this page.");
                open("/", "_self");
                </script>
                </body>
                </html>
                """
        return HttpResponse(html)
    else:
        html = """
            <html>
            <head>
            <title>Session expired</title>
            </head>
            <body>
            <script>
            alert("Your OTP session has been expired, Please try again!");
            open("/", "_self");
            </script>
            </body>
            </html>
            """
        return HttpResponse(html)

# Package
def packagePage(request):
    if request.session.get("email"):
        email = request.session.get("email")
        package_id = request.GET.get("id")
        
        # Get the current user
        user = models.user.objects.get(email=email)
        
        # Get the package details
        package = models.package.objects.get(id=package_id)
        
        # Get the bookings for the package
        bookings = models.booking.objects.filter(package=package.id)
        
        # Get all reviews for the package's bookings
        reviews = models.review.objects.filter(booking__in=bookings)
        
        context = {
            "name": user.name,
            "profile_img": user.profile_img,
            "package": package,
            "rating": [1, 2, 3, 4, 5],
            "reviews": reviews,
            "bookings": bookings,
        }
        return render(request, "package.html", context)
    else:
        return HttpResponse("""
            <html>
            <script>
                alert("You need to login first!");
                open("/", "_self");
            </script>
            <html>
        """)

def booking(request):
    if request.session.get("email"):
        email = request.session.get("email")
        package = request.GET.get("package")
        persons = request.POST.get("persons")
        arrival = request.POST.get("date")
        user = models.user.objects.filter(email=email)
        
        Packages = models.package.objects.filter(id=package)
        inStock = Packages[0].stock
        days = Packages[0].days
        arrival = datetime.strptime(arrival, '%Y-%m-%d').date()
        start_date = arrival - timedelta(days=days)

        Bookings = models.booking.objects.filter(package=package, arrival__lte=arrival, arrival__gte=start_date)
        members = 0
        for booking in Bookings:
            members += booking.members
        
        if members + int(persons) <= inStock:
            booking = models.booking(package=package, user=user[0].id, arrival=arrival, members=persons, payment="/static/images/receipts/no_receipt.html", verify=False)
            booking.save()
            send_mail(
                "Vista Pakistan Package Booking",
                "Thanks for choosing us You're package has been received.",
                'moeezrazaseven@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect(f"/package/payment/?booking={booking.id}")
        else:
            return render(request, "booking.html", context={"booked":False})
    else:
        return redirect("/")
    
def paymentPage(request):
    bookingID = request.GET.get("booking")
    book = models.booking.objects.filter(id=bookingID)
    Packages = models.package.objects.filter(id=book[0].package)
    amount = float(Packages[0].price) * float(book[0].members)
    context = {"booked":True, "price":amount, "booking":bookingID}
    return render(request, "booking.html", context=context)

def payment(request):
    if request.method == 'POST' and request.FILES['receipt']:
        bookingID = request.GET.get("booking")
        book = get_object_or_404(models.booking, id=bookingID)

        if book.payment != "/static/images/receipts/no_receipt.html":
            os.remove(book.payment)

        receipt = request.FILES["receipt"]
        upload_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'receipts')
        file_name = str(bookingID)+'.'
        file__ext = receipt.name.split('.')[-1]
        fs = FileSystemStorage(location=upload_dir, base_url='/static/images/receipts/')
        fs.save(file_name+file__ext, receipt)
        book.payment="/static/images/receipts/"+file_name+file__ext
        book.save()
        return HttpResponse("<script>alert(\"Payment succecced!\\nLet the bank verification complete\");open(\"/\",\"_self\");</script>")
    else:
        return HttpResponse(f"<script>alert(\"Something went wrong!\\nPlease try again\");open(\"/package/payment/?booking={bookingID}\",\"_self\");</script>")
    
def review(request):
    if request.session.get("email"):
        email = request.session.get("email")
        booked = request.GET.get("booking")
        stars = int(request.POST.get("stars"))
        comment = request.POST.get("comment")

        # Create and save the review
        new_review = models.review(rating=stars, booking=booked, comment=comment)
        new_review.save()

        # Get the booking and package
        booking = models.booking.objects.get(id=booked)
        package = models.package.objects.get(id=booking.package)

        # Filter reviews related to the specific package
        bookings = models.booking.objects.filter(package=package.id)
        reviews = models.review.objects.filter(booking__in=bookings)

        # Calculate the average rating
        num_of_review = reviews.count()
        sum_of_stars = sum(review.rating for review in reviews)
        average = sum_of_stars / num_of_review if num_of_review > 0 else 0

        # Update the package rating and save
        package.rating = average
        package.save()
        send_mail(
            "Vista Pakistan Package Review",
            "Thanks for giving Review. You're resonse will be sticly noticed.",
            'moeezrazaseven@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("/profile/")
    else:
        return redirect("/")