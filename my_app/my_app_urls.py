from django.urls import path, include
from my_app import views
from my_app.configurations.swagger import schema_view

urlpatterns = [
  path('user_prfile/',views.profile_view),
  path('user/',views.user),
  path('admin_role/',views.admin),
  path('oidc/', include('mozilla_django_oidc.urls')),
  path('', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),

]
