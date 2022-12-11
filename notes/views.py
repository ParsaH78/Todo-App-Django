from rest_framework import generics
from rest_framework.views import APIView
from .models import Note
from .serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import NoteUserWritePermission
from rest_framework.permissions import IsAuthenticated


class NoteList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner=user.id)
    

class CreateNote(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    
class NotesDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, NoteUserWritePermission]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NotesUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, NoteUserWritePermission]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NotesDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, NoteUserWritePermission]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
