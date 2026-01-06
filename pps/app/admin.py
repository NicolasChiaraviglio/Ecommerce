from django.contrib import admin
from .models import Room, Booking, RoomImage, News
from django.utils.html import format_html


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 11  # Número de imágenes adicionales en blanco al agregar una habitación
    readonly_fields = ('mostrar_imagen',)  # Vista previa de las imágenes

    def mostrar_imagen(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.image.url))
        return "No image"
    mostrar_imagen.short_description = "Vista previa"


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'category', 'beds', 'capacity')
    inlines = [RoomImageInline]  # Incluye las imágenes en la página del modelo Room

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_preview')  # Muestra el título y la fecha en el panel
    search_fields = ('title', 'content')  # Permite buscar por título y contenido

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.image.url))
        return "No image"
    image_preview.short_description = 'Image Preview'


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking)
admin.site.register(News, NewsAdmin)

