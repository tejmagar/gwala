from django.contrib import admin

from .models import District, LocalBody, Ward, MilkTrade, Animal

# Register your models here.


# Address
admin.site.register(District)
admin.site.register(LocalBody)
admin.site.register(Ward)

admin.site.register(MilkTrade)
admin.site.register(Animal)
