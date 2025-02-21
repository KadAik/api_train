""" Create a basic user """
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import getpass

class Command(BaseCommand):
    help = """
    Create a classic User with default permissions.
    
    Usage
    -----
    python manage.py create_user --user-name Foo --password ****
    
    """
    
    def add_arguments(self, parser):
        # Positional argument (optional)
        parser.add_argument("p_username", type=str, nargs="?", help="Your username")

        # Named argument (optional)
        parser.add_argument("--username", type=str, help="Your username")
        
    def handle(self, *args, **kwargs):
        username  = kwargs.get("username") or kwargs.get('p_username')
        if not username:
            self.stderr.write(self.style.ERROR("Username is required!"))
            return
        
        # Check if the username already exists
        if get_user_model().objects.filter(username=username).exists():
            self.stderr.write(self.style.ERROR(f"Username '{username}' already exists. Please choose another one."))
            return
        
        self.stdout.write("Enter a password:")
        password1 = getpass.getpass()
        self.stdout.write("Confirm the password:")
        password2 = getpass.getpass()

        if password1 == password2:
            try:
                get_user_model().objects.create_user(username=username, password=password1)
                self.stdout.write(self.style.SUCCESS(f"User {username} successfully created."))
            except Exception as e:
               raise CommandError(f"Error creating user: {str(e)}")
        else:
            self.stderr.write(self.style.ERROR("Passwords mismatch ! \n Aborting ..."))