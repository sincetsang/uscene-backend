from django.urls import path
from django.contrib import admin

from . import views
from .views import validator

app_name = 'api'
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('heyos', validator.ValidatorApiView.as_view(), name="heyos"),
    # path('heyos/undeploy', validator.ValidatorUndeployApiView.as_view(), name="validators_undeploy"),
]
