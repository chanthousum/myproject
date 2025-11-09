from django.http import HttpResponse, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from my_app.my_serializers.category_serializer import CategorySerializer
from rest_framework import status
from rest_framework.decorators import api_view

from my_app.models import Category
# Create your views here.
@api_view(['GET'])
def get_category_all(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
@swagger_auto_schema(method='POST', request_body=CategorySerializer)
@api_view(['POST'])
def create_category(request):
    category = Category()
    category.name= request.data['name']
    data = {
        "name": category.name,
    }
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

