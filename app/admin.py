from django.contrib import admin
from .models import Book,Cart
from django.utils.html import format_html

# Register your models here.
class BoockAdmin(admin.ModelAdmin):
    list_display=("name","auther","price","description","cover_display")
    list_filter=("auther","price")
    search_fields=("name",)
    list_editable=("price",)
    
    def cover_display(self,obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="80" height="100"/>',
                obj.cover.url
            )
        return "No Image"
    cover_display.short_description = "Cover Preview"
# ---------------------------------------------
    actions=['make_free']
    
    def make_free(self,request,queryset):
        queryset.update(price=0)
        self.message_user(request,"Selected books have  been set to free")
    make_free.short_description="set selected book make free"   
        

admin.site.register(Book,BoockAdmin)
admin.site.register(Cart)