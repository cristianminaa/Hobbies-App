"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from hobbiesApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('profile/', profile, name='profilePage'),
    path('profile/<int:id>', profile, name="profilePage"),
    path('hobbies/', hobbies, name='hobbiesPage'),
    path('commonhobbies/', commonhobbies, name='commonhobbiesPage'),
    path('user/', user_api, name="user api"),
    path('user/<int:id>', user_api, name="user api"),
    path('health/', health),
    path('testPage/', test, name='test'),
    path('admin/', admin.site.urls),
    path('api/hobbies', hobbies_api, name='hobbies api'),
    path('api/similarhobbies', similar_hobbies_api, name='similar hobbies api'),
    path('api/filterbycity', filter_by_city, name='filter by city api'),
    path('api/filterbyusername', filter_by_username,
         name='filter by username api'),
    path('api/filterbyage', filter_by_age, name='filter by age api'),
    path('search/', search, name='search'),
    path('send_friend_request/',
         send_friend_request, name='send friend request'),
    path('accept_friend_request/',
         accept_friend_request, name='accept friend request'),
    path('friend_request/',
         friend_request_api, name='friend request api'),
    path('similarHobbies/', similarHobbies, name='similarHobbies'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
