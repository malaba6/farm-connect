from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="FarmConnect API",
        default_version='v1',
        description="API documentation for FarmConnect",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@farmconnect.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_settings = {
    'DEFAULT_INFO': openapi.Info(
        title="FarmConnect API",
        default_version='v1',
        description="API documentation for FarmConnect",
    ),
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

