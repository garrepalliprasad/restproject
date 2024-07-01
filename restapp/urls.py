from django.urls import path
from . import views
urlpatterns=[
    path('student/<int:id>/',views.StudentAPI.as_view(),name='student'),
    path('student/',views.StudentAPI.as_view(),name='student'),
]