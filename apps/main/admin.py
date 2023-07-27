from django.contrib import admin

from .models import Location, Ward, Producer, Animal, AnimalType


# Register your models here.


admin.site.register(Location)
admin.site.register(Ward)
admin.site.register(Producer)
admin.site.register(Animal)
admin.site.register(AnimalType)
