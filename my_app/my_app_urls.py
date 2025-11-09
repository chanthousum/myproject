from django.urls import path, include
from my_app import views
from my_app.configurations.swagger import schema_view
from my_app.controllers import product_views, category_views

urlpatterns = [
    path('user_prfile/', views.profile_view),
    path('user/', views.user),
    path('admin_role/', views.admin),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('', schema_view.with_ui('swagger',

                                 cache_timeout=0), name='schema-swagger-ui'),
    # -----------route product------------------
    path("api/v1/product/", product_views.get_product_all),
    path("api/v1/product", product_views.create_product),
    path("api/v1/product/find_by_id/<id>", product_views.find_by_id),
    path("api/v1/product/find_by_name/", product_views.find_by_name),
    path("api/v1/product/paginate/", product_views.paginate),
    path("api/v1/product/paginate_search_by_name/", product_views.paginate_search_by_name),
    path("api/v1/product/delete_by_id/<id>", product_views.delete_by_id),
    path("api/v1/product/update_by_id/<id>", product_views.update_by_id),
    path("api/v1/category/get_category_all/",category_views.get_category_all),
    path("api/v1/category/create", category_views.create_category),

]
