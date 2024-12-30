
from django.urls import path
from.import views

urlpatterns = [
    path('logoutpath',views.userlogout,name="logout"),
    path('check_login',views.check_login),
    path('user_register',views.user_register),
    path('',views.landing_theatre),
    
    path('user_display',views.user_display),
    path('user_movie_view/<int:userid>/<int:movieid>/<int:theatreid>',views.user_movie_view),
    path('user_movie_order',views.user_movie_order),
    path('user_movie_booking',views.user_movie_booking,name='user_movie_booking'),
    path('user_movie_ticket/<int:id>',views.user_movie_ticket),
    path('download_movie_ticket/<int:booking_id>',views.download_movie_ticket, name='download_movie_ticket'),
    path('user_movie_review/<int:userid>/<int:movieid>',views.user_movie_review),
    
    path('admin_display',views.admin_display),
    path('admin_theatre_display',views.admin_theatre_display),
    path('admin_theatre_add',views.admin_theatre_add),
    path('admin_theatre_delete/<int:id>',views.admin_theatre_delete),
    path('admin_theatre_edit/<int:id>',views.admin_theatre_edit),
    path('admin_movie_display',views.admin_movie_display),
    path('admin_movie_add',views.admin_movie_add),
    path('admin_movie_delete/<int:id>',views.admin_movie_delete),
    path('admin_movie_edit/<int:id>',views.admin_movie_edit),
    path('admin_movie_bookings', views.admin_movie_bookings),
    
    path('theatre_movie_display',views.theatre_movie_display),
    path('theatre_movie_bookings', views.theatre_movie_bookings),
    path('theatre_movie_search', views.theatre_movie_search),
    path('theatre_status_check/<int:bookingid>',views.theatre_status_check)
  
]
