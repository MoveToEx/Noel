from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', view=views.index, name='index'),
    path('<int:post_id>/', view=views.post, name='post'),
    path('<int:post_id>/comment/', view=views.comment, name='comment'),
    path('new/', view=views.new, name='new')
]
