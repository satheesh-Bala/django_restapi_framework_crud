from home import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.personViewSets, basename='user')

urlpatterns = [
    path('viewsets/',include(router.urls)),
    path('index/',views.index),
    path('person/',views.PersonManuplate),
    path('login/',views.Login),
    path('personapiview/',views.PersonAPIview.as_view()),
    path('registeruser/',views.RegisterUser.as_view()),
    path('loginuser/',views.LoginUser.as_view())
]
