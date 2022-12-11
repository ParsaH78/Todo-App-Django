from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreateNote.as_view(), name='create'),
    path('all', views.NoteList.as_view(), name='all'),
    path('detail/<str:pk>', views.NotesDetailAPIView.as_view(), name='detail'),
    path('update/<str:pk>', views.NotesUpdateAPIView.as_view(), name='update'),
    path('delete/<str:pk>', views.NotesDestroyAPIView.as_view(), name='delete'),

]