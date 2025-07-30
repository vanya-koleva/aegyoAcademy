from django.urls import path

from common.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]