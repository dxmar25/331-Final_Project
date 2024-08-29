from django.db import models

class User(models.Model):
    """
    This is a Django Model of the User Table

    It contains:\n
    - user: Name of the user\n
    - email: Email of the user\n
    - user_type: Specify if the user is a CUSTOMER, KITCHEN, CASHIER, MANAGER, or ADMIN\n
    - shift_start: Date Time of Shift Start of User\n
    - shift_end: Date Time 
    """
    
    # Enumeration class, where each option corresponds to a particular number
    class UserOptions(models.IntegerChoices):
        """
        Enumerated field with type of user
        """
        CUSTOMER = 0, 'Customer'
        KITCHEN = 1, 'Kitchen'
        CASHIER = 2, 'Cashier'
        MANAGER = 3, 'Manager'
        ADMIN = 4, 'Admin'

    name = models.CharField(max_length=255)
    email = models.TextField(max_length=255)
    user_type = models.IntegerField(choices=UserOptions.choices, default=UserOptions.CUSTOMER)
    shift_start = models.DateTimeField(null=True, blank=True)
    shift_end = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)

