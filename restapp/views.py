from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from django.views.decorators.csrf import csrf_exempt
import io
from django.views import View
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name='dispatch')
class StudentAPI(View):
    def get(self,request,*args,id=None,**kwargs):
        if id is None:
            students=Student.objects.all()
            students_serialized=StudentSerializer(students,many=True)
            students_json=JSONRenderer().render(students_serialized.data)
            return HttpResponse(students_json,content_type='application/json',status=200)
        else:
            try:
                student=Student.objects.get(id=id)
                student_serialized=StudentSerializer(student)
                student_json=JSONRenderer().render(student_serialized.data)
                return HttpResponse(student_json,content_type='application/json',status=200)
            except Student.DoesNotExist:
                return HttpResponse('Student with given id does not exist',status=400)
    def post(self,request,*args,**kwargs):
        student_json=request.body
        student_stream=io.BytesIO(student_json)
        student_parsed=JSONParser().parse(student_stream)
        student_serialized=StudentSerializer(data=student_parsed)
        if student_serialized.is_valid():
            student_serialized.save()
            return HttpResponse(student_json,content_type='application/json',status=201)
        return HttpResponse('Can not create new student',status=400)
    def put(self,request,*args,id=None,**kwargs):
        if id is not None:
            try:
                student=Student.objects.get(id=id)
                student_json=request.body
                student_stream=io.BytesIO(student_json)
                student_parsed=JSONParser().parse(student_stream)
                student_serialized=StudentSerializer(student,data=student_parsed)
                if student_serialized.is_valid():
                    student_serialized.save()
                    return HttpResponse(student_json,content_type='application/json',status=200)
            except Student.DoesNotExist:
                return HttpResponse('Student with given id not exist',status=404)
        else:
            return HttpResponse('<h1>Student id Required to update</h1>',status=400)
    def delete(self,request,*args,id=None,**kwargs):
        if id is not None:
            try:
                student=Student.objects.get(id=id)
                student.delete()
                return HttpResponse('Student Deleted',content_type='application/json',status=204)
            except Student.DoesNotExist:
                return HttpResponse('Student with given id not exist',status=404)
        else:
            return HttpResponse('Student id required to delete',status=400)
        



