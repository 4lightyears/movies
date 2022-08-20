from django.urls import path

from . import views


urlpatterns = [
    path('<int:movie_id>', views.detail, name='detail'),
    path('<int:movie_id>/create', views.create_review, name='create_review'),
    path('<int:review_id>/update', views.update_review, name='update_review'),
    path('<int:review_id>/delete', views.delete_review, name='delete_review'),
]
