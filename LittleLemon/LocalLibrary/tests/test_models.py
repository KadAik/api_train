from django.test import TestCase
from LocalLibrary.models import Author
# Author model

class AuthorModelTest(TestCase):
    """ Test Author model """
    
    # This method executes once to setup data to all test methods
    # Those data won't be modified by the methods during tests
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        # Here the db is populated with one record
        Author.objects.create(first_name = "Kad", last_name = "AIK")
     
    # This method is called before each test method execution and helps build
    # fresh data for use by each method. After each test method execution, TestCase tears down
    # all the data so that each test method always get a fresh copy of it. As TestCase automatically
    # tears down, no need to defien the tearDown method when subclassing TestCase   
    def setUp(self):
        return super().setUp()
    
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, "first name")
    
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')
        
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)
        
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)
        
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        expected_url = f"/catalog/authors/{author.id}/"
        generated_url = author.get_absolute_url()
        self.assertEqual(generated_url, expected_url)