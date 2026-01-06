from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.html import format_html

# Create your models here.

class Room(models.Model):
    ROOM_CATEGORIES = (
        ('APART1', 'APART SIMPLE 1'),
        ('APART2', 'APART SIMPLE 2'),
        ('APART3', 'APART SIMPLE 3'),
        ('APART4', 'APART SIMPLE 4'),
        ('APART5', 'APART SIMPLE 5'),
        ('APART P', 'APART PREMIUM'),
        ('APART P2', 'APART PREMIUM 2'),
        ('APART E', 'APART INCLUSIVO'),
        ('CASA1', 'CASA 1'),
        ('CASA2', 'CASA 2'),
        ('CASA3', 'CASA 3'),
        ('CASA4', 'CASA 4'),
        ('HOSTEL', 'HOSTEL'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=10, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    capacity = models.IntegerField()
    description = models.TextField(default="Default description")  # Nuevo campo para la descripción
    wifi = models.CharField(max_length=2, default="Si")
    cochera = models.CharField(max_length=10, default="Si")

    def __str__(self):
        return f'{self.number}. {dict(self.ROOM_CATEGORIES)[self.category]} Beds = {self.beds} People = {self.capacity}'
    
   # def mostrar_imagen(self):
   #     if self.imagen:
   #         return format_html('<img src="{}" width="100" height="100" />'.format(self.imagen.url))
   #     else:
   #         return ""
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    
    def __str__(self):
        return f'Reservaste el día {self.check_in.strftime("%d-%b-%Y %H:%M")} hasta {self.check_out.strftime("%d-%b-%Y %H:%M")}, comunicate a tráves del email o numero en contacto'

    
    
    
    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category
    
    def get_cancel_booking_url(self):
        return reverse_lazy('app:CancelBookingView', args=[self.pk,])
    
    
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")  # Relación con Room
    image = models.ImageField(upload_to="images/")  # Carpeta para las imágenes # Descripción opcional para la imagen

    def mostrar_imagen(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(self.image.url))
        return "No image"


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title