from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginView),
    path('reg/', views.regView),
    path('index/', views.index),
    path('logout/', views.logout),
    path('regDriver/', views.regDriver),
    path('profile/', views.viewOrEditeDriver),
    path('driverQuit/', views.driverQuit),
    path('requestRide/', views.requestRide),
    path('viewRide/', views.viewRide),
    path('updateRide/<int:ride_id>/', views.updateRide),
    path('viewOrder/', views.viewOrder),
    path('driverMode/', views.driverMode),
    path('viewDriverOrder/', views.viewDriverOrder),
    path('joinOrderSearch/', views.joinOrderSearch),
    #path('joinOrder/', views.joinOrder),
    path('joinOrder/<int:ride_id>/', views.joinOrder),
    path('driverSearch/', views.driverSearch),
    path('driverConfirm/<int:ride_id>/', views.driverConfirm),
    path('driverCompleted/<int:ride_id>/', views.driverCompleted),
    path('deleteOwner/<int:ride_id>/', views.deleteOwner),
    path('deleteSharer/<int:ride_id>/', views.deleteSharer),
]