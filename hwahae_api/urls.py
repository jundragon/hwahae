from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_url_v1_patterns = [
    path("", include("hwahae_api.products.urls", namespace="products")),
]


schema_view = get_schema_view(
    openapi.Info(
        title="Hwahae Open API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://github.com/jundragon",
        contact=openapi.Contact(email="jjundragon88@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=schema_url_v1_patterns,
)

swagger = [
    path(
        "swagger<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hwahae_api.products.urls", namespace="products")),
] + swagger
