from django.contrib import admin

from .models import District, LocalBody, Ward, Producer, Animal

# Register your models here.


# Address
admin.site.register(District)
admin.site.register(LocalBody)
admin.site.register(Ward)

admin.site.register(Producer)
admin.site.register(Animal)
