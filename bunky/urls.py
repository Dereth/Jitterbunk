from django.urls import path

from . import views

app_name = 'bunky'
urlpatterns = [
	path('', views.MainView.as_view(), name='main'),
	path('find/', views.find, name='find'),
	path('home/<int:user_id>/', views.home, name='home'),
	path('bunk/<int:user_id>/', views.bunk, name='bunk'),
	path('bunked/<int:pk>/', views.BunkedView.as_view(), name='bunked'),
]