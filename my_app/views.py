from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required,permission_required
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    return HttpResponse(f"Welcome {request.user.username}, you are logged in via Keycloak.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
    return JsonResponse({"message":"User only"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin(request):
    return JsonResponse({"message":"Admin only"})


