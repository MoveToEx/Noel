from django.urls import path
from . import views

app_name = 'zone'

urlpatterns = [
    path('', view=views.home, name='home'),
    path('<uuid:post_id>/', view=views.detail, name='detail'),
    path('<uuid:post_id>/comment/', view=views.comment, name='comment'),
    path('new/', view=views.new, name='new')
]