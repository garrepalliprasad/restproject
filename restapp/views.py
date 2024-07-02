from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from rest_framework import status

@api_view(['GET','POST','PUT','DELETE'])
def student(request,id=None):
    if request.method=='GET':
        if id is None:
            students=Student.objects.all()
            students_serialized=StudentSerializer(students,many=True)
            return Response(students_serialized.data,status=status.HTTP_200_OK)
        else:
            try:
                student=Student.objects.get(id=id)
                student_serialized=StudentSerializer(student)
                return Response(student_serialized.data,status=status.HTTP_200_OK)
            except Student.DoesNotExist:
                return Response('Student with given id does not exist',status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='POST':
        student_deserialized=StudentSerializer(data=request.data)
        if student_deserialized.is_valid():
            student_deserialized.save()
            return Response(request.data,status=status.HTTP_201_CREATED)
        return Response('Can not create new student',status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='PUT':
        if id is not None:
            try:
                student=Student.objects.get(id=id)
                student_deserialized=StudentSerializer(student,data=request.data)
                if student_deserialized.is_valid():
                    student_deserialized.save()
                    return Response(request.data,status=status.HTTP_200_OK)
                return Response(student_deserialized.errors,status=status.HTTP_404_NOT_FOUND)
            except Student.DoesNotExist:
                return Response('Student with given id not exist',status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Student id Required to update',status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        if id is not None:
            try:
                student=Student.objects.get(id=id)
                student.delete()
                return Response('Student Deleted',status=status.HTTP_204_NO_CONTENT)
            except Student.DoesNotExist:
                return Response('Student with given id not exist',status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Student id required to delete',status=status.HTTP_400_BAD_REQUEST)
        



