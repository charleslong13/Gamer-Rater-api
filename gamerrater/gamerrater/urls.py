from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from gamerraterapi.views import register_user, login_user
from rest_framework import routers
from gamerraterapi.views import GameView
from gamerraterapi.views.Category import CategoryView
from gamerraterapi.views.Review import GameReviewView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'game', GameView, 'game')
router.register(r'category', CategoryView, 'category')
router.register(r'reviews', GameReviewView, 'review')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]