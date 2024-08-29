from django.db import models



# Model of menu class
class Menu(models.Model):
    """
    This is a Django Model of the Menu Table

    It contains:\n
    - name: Name of menu item\n
    - price: Price of menu item\n
    - category: Choices representing food item categories (BURGERS, BASKETS, SANDWICHES, SHAKESNSWEETS, BEVERAGES, SIDES or SAUCE\n
    - description: More details about the menu item\n
    - season_start: Start of when the menu item is in season\n
    - season_end: End of when the menu item is in season\n
    - display: Wether to display the menu item or not\n
    - image: Reference to the image of the menu item\n
    """

    class CategoryOptions(models.IntegerChoices):
        """
        Contains enumerated choices for categories
        """
        BURGERS = 0, 'Burgers'
        BASKETS = 1, 'Baskets'
        SANDWICHES = 2, 'Sandwiches'
        SHAKESNSWEETS = 3, 'Shakes n Sweets'
        BEVERAGES = 4, 'Beverages'
        SIDES = 5, 'Sides'
        SAUCE = 6, 'Sauces'

    name = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.IntegerField(choices=CategoryOptions.choices, default=CategoryOptions.BURGERS)
    description = models.TextField(null=True, blank=True)
    season_start = models.DateTimeField()
    season_end = models.DateTimeField() 
    display = models.BooleanField(default=False)
    image = models.TextField(null=True, blank=True)


    ## params: limit = max_length of list
    ## returns [Menu(), Menu()...]
    # @staticmethod
    # def getTrendyItems(limit = 10):
    #     pass
