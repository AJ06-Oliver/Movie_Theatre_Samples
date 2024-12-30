from django.shortcuts import render,redirect
from.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout,get_user_model,login
# from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


# Create your views here.

razorpay_client = razorpay.Client(auth=("rzp_test_4Ex6Tyjkp79GFy", "lVGcQB0HSAttEhr7mq4AbM7Z"))


def userlogout(request):
    logout(request)
    return redirect('/check_login')


def landing_theatre(request):
    return render(request,"landing_theatre.html")


 #######################################################   DECORATORS   ##########################################################
 
 
def admin_only(view_fun): 
        
    def wrapper(*args,**kwargs): 
        # print(args)
        # print(kwargs)
        user = args[0].user #request.user
        if user.is_anonymous:
           return redirect('/check_login')
        elif user.usertype != 0:
           logout(args[0])
           return redirect('/check_login')
        else:
           return view_fun(*args,**kwargs)
    return wrapper

def theatre_only(view_fn):
    
    def wrapper(*args,**kwargs):
        user = args[0].user
        if user.is_anonymous:
            return redirect('/check_login')
        elif user.usertype != 1:
            return redirect('/check_login')
        else:
            return view_fn(*args,**kwargs)
    return wrapper


def user_only(view_fn):
    def wrapper(*args,**kwargs):
        user = args[0].user
        if user.is_anonymous:
            return redirect('/check_login')
        elif user.usertype != 2:
            return redirect('/check_login')
        else:
            return view_fn(*args,**kwargs)
    return wrapper
        
####################################################################################################################################       

def check_login(request):
  if request.method == "POST":
      email = request.POST.get('email')
      password= request.POST.get('password')
      try:
          user = CustomUser.objects.get(email = email)
          if user.check_password(password):
              login(request, user)
              if user.usertype == 0:
                  return redirect('/admin_display')
              elif user.usertype == 1:
                  return redirect('/theatre_movie_display')
              elif user.usertype == 2:
                  return redirect('/user_display')
              else:
                  return redirect('/check_login')
          else:
            print("Invalid User")    
      except user.DoesNotExist:
          print("User does not exist")
  return render(request,"check_login.html")



def user_register(request):
    
    if request.method == "POST":
        User_data = CustomUser()
        User_data .email = request.POST.get('email')
        User_data .set_password(request.POST.get('password'))        
        User_data .usertype = 2
        User_data .save()
        user_id = User_data.id        
        user_add = RegistrationTable()
        user_add.username = request.POST.get('username')
        user_add.useraddress = request.POST.get('useraddress')
        user_add.userid_id = user_id
        user_add.save()
        return redirect('/check_login')
    return render(request,"user_register.html") 



###############################################################################################################################


@theatre_only
def theatre_movie_display(request):
    userid = request.user.id
    theatre_data = Theatre.objects.get(userid=userid)
    theatre_id = theatre_data.id
    booking_data = BookingTable.objects.filter(theatreid=theatre_id)       
    return render(request,"theatre/theatre_movie_display.html",{'bookings':booking_data})

@theatre_only
def theatre_status_check(request,bookingid):
    booking_data = BookingTable.objects.get(id=bookingid)
    if request.method == "POST":
       booking_data.status = request.POST.get('status')        
       theatre_id = booking_data.theatreid_id
       theatre_data = Theatre.objects.get(id=theatre_id) 
       user_id = theatre_data.userid_id
       booking_data.save()        
       return redirect("/theatre_movie_display")
    return render(request,"theatre/theatre_status_check.html",{'bookings':booking_data})

@theatre_only
def theatre_movie_bookings(request):
    userid = request.user.id
    theatre_data = Theatre.objects.get(userid=userid)
    theatre_id = theatre_data.id
    
    booking_data = BookingTable.objects.filter(theatreid=theatre_id)
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M')
            to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M')
        
            booking_data = booking_data.filter(booking_time__range=(from_date, to_date))     
    return render(request,"theatre/theatre_movie_bookings.html",{'bookings':booking_data})

# def theatre_search_status(request):
#     booking_data = BookingTable.objects.all()
#     return render(request,"theatre/theatre_search_status.html",{'bookings':booking_data})


def theatre_movie_search(request):
    userid = request.user.id
    theatre_data = Theatre.objects.get(userid=userid)
    theatre_id = theatre_data.id
    booking_data = BookingTable.objects.filter(theatreid=theatre_id)    
    return render(request,"theatre/theatre_movie_search.html",{'bookings':booking_data})

    
##############################################################################################################################


@admin_only
def admin_display(request): 
    movie_data = MovieShow.objects.all()
    return render(request,"admin_user/admin_display.html",{'movies':movie_data}) 
@admin_only
def admin_theatre_display(request):
    Theatre_data = Theatre.objects.all()
    return render(request,"admin_user/admin_theatre_display.html",{'theatres': Theatre_data})
@admin_only
def admin_theatre_add(request):    
    if request.method == "POST":        
        users = CustomUser()
        users.email = request.POST.get('email')
        users.set_password(request.POST.get('password'))
        users.usertype = 1
        users.save()
        user_id = users.id        
        adddata = Theatre()
        adddata.theatrename = request.POST.get('theatrename')
        adddata.theatrelocation = request.POST.get('theatrelocation')
        adddata.theatredescription = request.POST.get('theatredescription')
        adddata.rating = request.POST.get('rating')
        adddata.userid_id = user_id
        adddata.save()
        
        return redirect('/admin_theatre_display')
    return render(request,"admin_user/admin_theatre_add.html")

@admin_only
def admin_theatre_edit(request,id):
    theatre_data = Theatre.objects.get(userid=id)
    if request.method == 'POST':
        user_edit = CustomUser.objects.get(id=id)
        user_edit.email = request.POST.get('email')
        user_edit.save()
        theatre_edit = Theatre.objects.get(userid=id)
        theatre_edit.theatrename = request.POST.get('theatrename')
        theatre_edit.theatrelocation = request.POST.get('theatrelocation')
        theatre_edit.theatredescription = request.POST.get('theatredescription')
        theatre_edit.rating = request.POST.get('rating')
        theatre_edit.save()
        return redirect('/admin_theatre_display')
    
    return render(request,"admin_user/admin_theatre_edit.html",{'theatres':theatre_data})

@admin_only
def admin_theatre_delete(request,id):
    theatre_delete = Theatre.objects.get(userid=id)
    theatre_delete.delete()
    delete_user = CustomUser.objects.get(id=id)
    delete_user.delete()
    return redirect('/admin_theatre_display')


@admin_only
def admin_movie_bookings(request):
    booking_data = BookingTable.objects.filter(status = 1)
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')     
        from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M')
        to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M')        
        booking_data = booking_data.filter(booking_time__range=(from_date, to_date))     
    return render(request,"admin_user/admin_movie_bookings.html",{'bookings':booking_data})
    
    
 #########################################################################################################################

@admin_only
def admin_movie_display(request):
    movie_data = MovieShow.objects.all()
    return render(request,"admin_user/admin_movie_display.html",{'movies':movie_data})

@admin_only
def admin_movie_add(request):
    theatre_data = Theatre.objects.all()
    if request.method == 'POST':
        add_movie = MovieShow()
        theatre_id = request.POST.get('theatreid')
        add_movie.theatreid = Theatre.objects.get(id=theatre_id)
        add_movie.moviename = request.POST.get('moviename')
        add_movie.moviedescription = request.POST.get('moviedescription')
        add_movie.movielanguage = request.POST.get('movielanguage')
        add_movie.moviegenere = request.POST.get('moviegenere')
        sensor_rate_list = request.POST.getlist('sensorrate')
        add_movie.sensorrate = ', '.join(sensor_rate_list)
        add_movie.image = request.POST.get('image')
        if len(request.FILES)!= 0:
            add_movie.image = request.FILES['image']
        add_movie.save()
        return redirect('/admin_movie_display')
    return render(request,"admin_user/admin_movie_add.html",{'theatres':theatre_data})

@admin_only
def admin_movie_delete (request,id):
    movie_delete = MovieShow.objects.get(id=id)
    movie_delete.delete()
    return redirect('/admin_movie_display')
    

@admin_only
def admin_movie_edit(request,id):
    movie_edit = MovieShow.objects.get(id=id)
    if request.method == "POST":
        movie_edit.moviename = request.POST.get('moviename')
        movie_edit.moviedescription = request.POST.get('moviedescription')
        movie_edit.movielanguage = request.POST.get('movielanguage')
        movie_edit.moviegenere = request.POST.get('moviegenere')
        a = request.POST.getlist('sensorrate')
        movie_edit.sensorrate = ', '.join(a)
        if len(request.FILES) != 0:
          if len(movie_edit.image)> 0:
            os.remove(movie_edit.image.path)
            movie_edit.image = request.FILES["image"]
        movie_edit.save()
        return redirect('/admin_movie_display')
    return render(request,"admin_user/admin_movie_edit.html",{'movies':movie_edit})


##################################################################################################################################

# @login_required(login_url='/check_login')
@user_only
def user_display(request):
    id = request.user.id
    register_data = RegistrationTable.objects.get(userid=id)
    booking_data = BookingTable.objects.filter(userid=id).values('movieid','status','id')
    movie_data = MovieShow.objects.all()
    movie_details=[]   
    for movie in movie_data:
        movie.user_id = register_data.userid
        movie_details.append({'movies':movie,'registrations':register_data,'bookings':booking_data})  
    return render(request,"user/user_display.html",{'movie_details':movie_details})

@user_only
def user_movie_view(request,userid,movieid,theatreid):
    user_data = CustomUser.objects.get(id=userid)
    theatre_data = Theatre.objects.get(id=theatreid)
    movie_data = MovieShow.objects.get(id=movieid)
    review_data = ReviewTable.objects.all()
    # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh:", review_data)
    if request.method == "POST":
        booking_data = BookingTable()        
        booking_data.userid_id = user_data.id
        booking_data.theatreid_id = theatre_data.id    
        booking_data.movieid_id = movie_data.id
        booking_data.status = 0
        booking_data.booking_time = request.POST.get('booking_time') 
        booking_data.save()      
        return redirect('/user_display')      
    return render(request,"user/user_movie_view.html",{'users':user_data,'movies':movie_data,'theatres':theatre_data,'reviews':review_data})



def user_movie_ticket(request,id):
    booking_data = BookingTable.objects.get(id=id)
    return render(request,"user/user_movie_ticket.html",{'bookings':booking_data})

###################################################   TICKET  ###################################################################

def download_movie_ticket(request, booking_id):
    booking_data = BookingTable.objects.get(id=booking_id)
    
    # style_1 = request.build_absolute_uri(static('css/bootstrap.css'))
    # style_2 = request.build_absolute_uri(static('bootstrap/heroes/heroes.css'))
    # image_url = request.build_absolute_uri(booking_data.movieid.image.url)

    context = {
        'bookings': booking_data,
        # 'style_1' : style_1,
        # 'style_2' : style_2,
        # 'image_url' : image_url,
    }
    html_string = render_to_string('user/user_movie_ticket.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="movie_ticket_{booking_id}.pdf"'
    HTML(string=html_string).write_pdf(response)
    return response



################################################    USER PAYMENT    ####################################################################

@csrf_exempt
def user_movie_order(request):
    userid = request.user.id
    theatreid = request.POST.get('theatreid')
    movieid = request.POST.get('movieid')
    datetime = request.POST.get('datetime')
    booking_data = BookingTable()        
    booking_data.userid_id = userid
    booking_data.theatreid_id = theatreid
    booking_data.movieid_id = movieid
    booking_data.status = 0
    booking_data.booking_time = datetime
    booking_data.save()     
    
    new_order_response = razorpay_client.order.create({
            
            "amount": 200*100,
            "currency": "INR",
            "payment_capture": "1"
            })

    response_data = {  
        "order": new_order_response
    }
    return JsonResponse(response_data) 

@csrf_exempt
def user_movie_booking(request):
    
    return redirect('/user_display')
    
    
@user_only
def user_movie_review(request,userid,movieid):
    user_data = CustomUser.objects.get(id=userid)
    movie_data = MovieShow.objects.get(id=movieid)
    if request.method == "POST":
       review_data = ReviewTable()
       review_data.userid = CustomUser.objects.get(id=userid)
       review_data.movieid = MovieShow.objects.get(id=movieid)
       review_data.reviewdescription = request.POST.get('reviewdescription')
       review_data.reviewrating = request.POST.get('reviewrating')
       review_data.save()
       return redirect('/user_display')
    return render(request,"user/user_movie_review.html",{'users':user_data,'movies':movie_data})


