from django.test import TestCase
from models import ProgrammingPath
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from django.utils.text import slugify

class ProgrammingPathTest(TestCase):

    def setUp(self) -> None:
        logo_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        path_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.programming_path = ProgrammingPath.objects.create(name="Python",
         about="Just Python language", logo_image= logo_image, path_image=path_image)

    def check_slug(self) -> None:
        self.assertTrue(self.programming_path.slug , slugify(self.programming_path.name))

    # def get_context(self):
    #     request = RequestFactory().get('/')
    #     view = MainBookView()
    #     view.setup(request)
    #     view.object_list = view.get_queryset()
    #     context = view.get_context_data()
    #     return context

    # def test_call_view_load(self):
    #     response = self.client.get(reverse("book-view"))
    #     self.assertTemplateUsed(response, 'Book_organizer/books.html')

    # def test_authors_set_in_context(self):
    #     context = self.get_context()
    #     self.assertIn('authors', context)

    # def test_books_set_in_context(self):
    #     context = self.get_context()
    #     self.assertIn('books', context)
