from django.views.decorators.csrf import csrf_exempt
from .models import Livro
from .serializers import LivroSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from typing import Any
 



class JSONResponse(HttpResponse):
   def __init__(self, data, **kwargs):
       content = JSONRenderer().render(data)
       kwargs['content_type'] = 'application/json'
       super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        try:
            livro_data = JSONParser().parse(request)
            serializer = LivroSerializer(data=livro_data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JSONResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def livro_detail(request, pk):
    
    livro = Livro.objects.get(pk=pk)
    
    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return JSONResponse(serializer.data)
    
    elif request.method == 'PUT':
        try:
            livro_data = JSONParser().parse(request)
            serializer = LivroSerializer(livro, data=livro_data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JSONResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        livro.delete()
    return JSONResponse(status=status.HTTP_204_NO_CONTENT)

