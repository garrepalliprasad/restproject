from django.urls import path
from . import views
urlpatterns=[
    path('student/<int:id>/',views.student,name='student'),
    path('student/',views.student,name='student'),
]