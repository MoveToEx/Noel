from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', view=views.my, name='my'),
    path('edit/', view=views.edit, name='edit'),
    path('login/', view=views.login, name='login'),
    path('logout/', view=views.logout, name='logout'),
    path('register/', view=views.register, name='register'),
    path('<int:user_id>/', view=views.user, name='user')
]
