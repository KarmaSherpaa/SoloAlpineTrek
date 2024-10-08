from django.contrib import admin
from .models import Destination, Image, Activity, Package, Booking , DayDescription
# Register your models here.

class ImageInline(admin.TabularInline):  # Inline for adding images
    model = Image
    extra = 1  # Number of extra inline forms to display

class DestinationAdmin(admin.ModelAdmin):
    inlines = [ImageInline]  # Add ImageInline to the Destination admin


admin.site.register(Destination, DestinationAdmin)

admin.site.register(Activity)
admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(DayDescription)