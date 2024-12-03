from gtts import gTTS
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework.exceptions import NotFound
from django.core.serializers.json import DjangoJSONEncoder
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Book, Chapter, Section, Shloka
from .serializers import BookSerializer, ChapterSerializer, SectionSerializer, ShlokaSerializer, RegisterSerializer, UserSerializer 
from .filters import BookFilterSet, ChapterFilterSet, SectionFilterSet
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import os

User = get_user_model()

# View for registering new users
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)  # Allows unauthenticated access

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # This will raise a 400 error if validation fails
        user = self.perform_create(serializer)
        return Response({
            "user": serializer.data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

# Custom token serializer to add custom claims
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email  # Optionally include email
        token['is_admin'] = user.is_staff
        return token

# View to obtain JWT tokens
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# View for retrieving the authenticated user's profile
class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

# Function-based views
def book_list(request):
    books = Book.objects.all().values('id', 'book_number', 'book_name', 'book_image')
    books = list(books)
    for book in books:
        if book['book_image']:
            book['book_image'] = request.build_absolute_uri(book['book_image'])
    return JsonResponse(books, safe=False)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    chapters = Chapter.objects.filter(book=pk).values('id', 'chapter_number', 'chapter_name', 'chapter_image')
    chapters = list(chapters)
    for chapter in chapters:
        chapter['chapter_image'] = chapter['chapter_image'].url if chapter['chapter_image'] else None

    response_data = {
        'book': {
            'id': book.id,
            'book_number': book.book_number,
            'book_name': book.book_name,
            'book_image': book.book_image.url if book.book_image else None,
            'book_slider': book.book_slider.url if book.book_slider else None
        },
        'chapters': chapters
    }
    return JsonResponse(response_data)

def book_chapters(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    chapters = Chapter.objects.filter(book=book).values('id', 'chapter_number', 'chapter_name', 'chapter_image')
    chapters = list(chapters)
    for chapter in chapters:
        if chapter['chapter_image']:
            chapter['chapter_image'] = request.build_absolute_uri(chapter['chapter_image'])

    response_data = {'chapters': chapters}
    return JsonResponse(response_data, encoder=DjangoJSONEncoder)

def chapter_detail(request, book_pk, pk):
    chapter = get_object_or_404(Chapter, pk=pk, book_id=book_pk)
    sections = Section.objects.filter(chapter=chapter).values('id', 'section_number', 'section_name', 'section_image')
    sections = list(sections)
    for section in sections:
        section['section_image'] = section['section_image'].url if section['section_image'] else None

    shlokas = Shloka.objects.filter(chapter=chapter).values('id', 'shloka_number', 'shlok_text', 'chapter', 'section')

    response_data = {
        'chapter': {
            'id': chapter.id,
            'chapter_number': chapter.chapter_number,
            'chapter_name': chapter.chapter_name,
            'chapter_image': chapter.chapter_image.url if chapter.chapter_image else None,
            'chapter_slider': chapter.chapter_slider.url if chapter.chapter_slider else None,
            'book': chapter.book_id
        },
        'sections': sections,
        'shlokas': list(shlokas)
    }
    return JsonResponse(response_data)

def section_detail(request, chapter_pk, pk):
    section = get_object_or_404(Section, pk=pk, chapter_id=chapter_pk)
    shlokas = Shloka.objects.filter(section=section).values('id', 'shloka_number', 'shlok_text', 'chapter', 'section')
    
    response_data = {
        'section': {
            'id': section.id,
            'section_number': section.section_number,
            'section_name': section.section_name,
            'section_image': section.section_image.url if section.section_image else None,
            'chapter': section.chapter_id
        },
        'shlokas': list(shlokas)
    }
    return JsonResponse(response_data)

def shloka_detail(request, pk):
    shloka = get_object_or_404(Shloka, pk=pk)
    response_data = {
        'shloka': {
            'id': shloka.id,
            'shloka_number': shloka.shloka_number,
            'shlok_text': shloka.shlok_text,
            'chapter': shloka.chapter_id,
            'section': shloka.section_id,
        }
    }
    return JsonResponse(response_data)

# ViewSets for REST API
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilterSet

class ChapterViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_pk')
        if book_id:
            return Chapter.objects.filter(book_id=book_id)
        return Chapter.objects.all()

    def retrieve(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_pk')
        if book_id:
            queryset = self.get_queryset()
            chapter = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
            serializer = self.get_serializer(chapter)
            return Response(serializer.data)
        raise NotFound(detail="Book ID not found in request.")

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SectionFilterSet

class ShlokaViewSet(viewsets.ModelViewSet):
    serializer_class = ShlokaSerializer
    queryset = Shloka.objects.all()
    lookup_field = 'pk'
    
    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        chapter_pk = self.kwargs.get('chapter_pk')
        if book_pk and chapter_pk:
            return Shloka.objects.filter(chapter__book__id=book_pk, chapter__id=chapter_pk)
        return Shloka.objects.none()

    @action(detail=True, methods=['get'])
    def play_audio(self, request, *args, **kwargs):
        shloka = self.get_object()
        shlok_text = shloka.shlok_text

        try:
            tts = gTTS(text=shlok_text, lang='en')
            tmp_file = 'shloka.mp3'
            tts.save(tmp_file)

            with open(tmp_file, 'rb') as audio_file:
                response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = 'inline; filename="shloka.mp3"'
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        finally:
            # Cleanup temporary audio file
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

        return response
