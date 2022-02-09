from django.db import models

class NotifType(models.IntegerChoices):
        campaign   = 1
        entry      = 2
        other      = 3

class Day(models.IntegerChoices):
        monday    = 1
        tuesday   = 2
        wednesday = 3
        thursday  = 4
        friday    = 5
        saturday  = 6
        sunday    = 7
        
class Frequency(models.IntegerChoices):
        pack_1    = 1
        pack_more = 2
        pack_half = 3
        few       = 4

class Currency(models.IntegerChoices):
        lira   = 1
        dollar = 2
        euro   = 3
        yen    = 4
        other  = 5
        
class SmokingType(models.IntegerChoices):
        pack_1    = 1
        pack_more = 2
        pack_half = 3
        few       = 4
        
class Brand(models.IntegerChoices):
        marlboro   = 1
        kent       = 2
        camel      = 3
        davidoff   = 4
        other      = 5

class Intensity(models.IntegerChoices):
        low       = 1
        mild      = 2
        high      = 3
        extreme   = 4
            
class AuthSource(models.TextChoices):
        google   = 'google.com'
        facebook = 'facebook.com'
        apple    = 'apple.com'
        email    = 'password'
        
class Relationship(models.IntegerChoices):
        family             = 1
        friend             = 2
        colleague          = 3
        significant_other  = 4
        other              = 5
                