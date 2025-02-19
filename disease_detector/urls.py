from django.urls import path
from .views import home, home1, image_predict_crop_view

urlpatterns = [
    path('', home, name='home'),
    path('index2/', home1, name='home1'),
    path('image_predict_crop/', image_predict_crop_view, name='image_predict_crop'),
    path('predict_image/', image_predict_crop_view, name="predict_image"),  # New route
]

