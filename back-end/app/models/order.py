from django.db import models
from .user import User

# completed - when completed
# in-progess - when hit send to kitchen
# cancelled - manger cancels from kitchen screen
# deleted - 

class Order(models.Model):
    """
    This is a Django Model of the Order Table

    It contains:\n
    - employee: Foregin Key of User table\n
    - total: Total price of the order\n
    - timestamp: Date and Time of the order\n
    - status: Current status of the order (In Progress, Completed, Incomplete, Deleted)\n
    """
    
    class Status(models.IntegerChoices):
        """
        Contains enumerated choices for order status
        """
        IN_PROGRESS = 0, 'In Progress'
        COMPLETED = 1, 'Completed'
        INCOMPLETE = 2, 'Incomplete'
        DELETED = 3, 'Deleted'

    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None) 
    total = models.FloatField()
    timestamp = models.DateTimeField() # char fields are usually easier to handle
    status = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)

    ## params: start = Date(), end = Date()
    ## returns [Order(), Order()...]
    # @staticmethod
    # def getOrderFromTime(start, end):   
    #     pass

