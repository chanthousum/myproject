from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from my_app.my_serializers.product_serializer import ProductSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from my_app.models import Category, Product
# Create your views here.
@api_view(['GET'])
def get_product_all(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
@swagger_auto_schema(method='POST', request_body=ProductSerializer)
@api_view(['POST'])
def create_product(request):
    product = Product()
    product.name = request.data['name']
    product.barcode = request.data['barcode']
    product.sell_price=request.data['sell_price']
    product.unit_in_stock=request.data['unit_in_stock']
    product.photo=request.data['photo']
    product.category_id=request.data['category']
    if product.photo!=None and product.photo!="":
        data = {
            "name": product.name,
            "barcode": product.barcode,
            "sell_price": product.sell_price,
            "unit_in_stock": product.unit_in_stock,
            "photo": product.photo,
            "category": product.category_id,
        }
    else:
        data = {
            "name": product.name,
            "barcode": product.barcode,
            "sell_price": product.sell_price,
            "unit_in_stock": product.unit_in_stock,
            "photo":"",
            "category": product.category_id,
        }
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def find_by_id(request, id):
    product=Product.objects.filter(id=id).first()
    if product is None:
        return JsonResponse({'error': f'Product not found with id:{id}'})
    serializer = ProductSerializer(product)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


name = openapi.Parameter('name',openapi.IN_QUERY,description="Search categories by name (like)",type=openapi.TYPE_STRING)
@swagger_auto_schema(method='get',manual_parameters=[name],responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
def find_by_name(request):
    name=request.query_params.get('name')
    if name is None:
        return JsonResponse({'error': f'Product not found with name:{name}'})
    products=Product.objects.filter(name__icontains=name)
    if products.count() == 0:
        return JsonResponse({'error': f'Product not found with name:{name}'})
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def paginate(request):
    paginator = PageNumberPagination()
    paginator.page_size=5
    products = Product.objects.all()
    result_page=paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
name = openapi.Parameter('name',openapi.IN_QUERY,description="Search categories by name (like)",type=openapi.TYPE_STRING)
@swagger_auto_schema(method='get',manual_parameters=[name],responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
def paginate_search_by_name(request):
    name=request.query_params.get('name')
    if name is None:
        return JsonResponse({'error': f'Product not found with name:{name}'})
    paginator = PageNumberPagination()
    paginator.page_size=5
    products = Product.objects.filter(name__icontains=name)
    result_page=paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['DELETE'])
def delete_by_id(request, id):
    product=Product.objects.filter(id=id).first()
    if product is None:
        return JsonResponse({'message': f'Product not found with id:{id}'})
    if product.photo:
        product.photo.delete()
    product.delete()
    return JsonResponse({'message': f'Product deleted successfully'})

@swagger_auto_schema(method='put', request_body=ProductSerializer)
@api_view(['PUT'])
def update_by_id(request, id):
    product_existing=Product.objects.filter(id=id).first()
    if product_existing is None:
        return JsonResponse({'message': f'Product not found with id:{id}'})
    product_existing.name = request.data['name']
    product_existing.barcode = request.data['barcode']
    product_existing.sell_price = request.data['sell_price']
    product_existing.unit_in_stock = request.data['unit_in_stock']
    fileName= request.data['photo']
    product_existing.category_id = request.data['category']
    if product_existing.photo:
        if fileName!="" :
            product_existing.photo.delete()
            data = {
                "name": product_existing.name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "photo":fileName,
                "category": product_existing.category_id,
            }
        else:
            data = {
                "name": product_existing.name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "category": product_existing.category_id,
            }
    else:
        if fileName != "":
            data = {
                "name": product_existing.name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "photo": fileName,
                "category": product_existing.category_id,
            }
        else:
            data = {
                "name": product_existing.name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "category": product_existing.category_id,
            }

    serializer = ProductSerializer(product_existing,data=data)
    if serializer.is_valid():
        serializer.save()
        data={"message": "Product updated successfully","data":serializer.data}
        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

