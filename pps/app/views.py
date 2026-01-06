from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking, News
from .forms import AvailabilityForm
from app.booking_functions.availability import check_availability
from app.booking_functions.get_room_cat_url_list import get_room_cat_url_list
from app.booking_functions.get_room_category_human_format import get_room_category_human_format
from app.booking_functions.get_available_rooms import get_available_rooms
from app.booking_functions.book_room import book_room
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin





def RoomListView(request):
    room_category_url_list = get_room_cat_url_list()
     
    context={
        'room_list': room_category_url_list,
    }
    return render(request, 'index.html',context)
    
class BookingListView(LoginRequiredMixin, SuccessMessageMixin,ListView):
    model = Booking
    template_name="booking_list_view.html"
    success_message = "Reserva realizada exitosamente."
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list
        
    
class RoomDetailView(View):
    def get(self, request,*args, **kwargs):
        category = self.kwargs.get('category', None)
        human_format_room_category = get_room_category_human_format(category)
        form = AvailabilityForm()
        
         # Obtener habitaciones de la categoría
        rooms = Room.objects.filter(category=category)
        
        room_images = []
        for room in rooms:
            images = room.images.all()  # Obtener las imágenes de la habitación
            room_images.append((room, images))  # Agregar la habitación y sus imágenes como tupla


        
        if human_format_room_category is not None:
            context={
                'room_category': human_format_room_category,
                'form': form,
                'rooms': rooms,
                'room_images': room_images,  # Pasar imágenes al contexto
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category no existe')
        
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            available_rooms = get_available_rooms(category, data['check_in'], data['check_out'])
            
        if available_rooms:
            # Reservar la primera habitación disponible
            booking = book_room(request, available_rooms[0], data['check_in'], data['check_out'])        
            
            # Redirigir al usuario a la página de listado de reservas
            return redirect(reverse_lazy('app:BookingListView'))  # Asegúrate de que el nombre coincida en urls.py
        else:
            # Mostrar mensaje de error si no hay habitaciones disponibles
            return HttpResponse('Esta categoria de habitaciones está reservada, prueba otra')
        #else:
            # Manejo de formulario no válido
        #    return render(request, 'room_detail_view.html', {
        #        'form': form,
        #        'error_message': 'Formulario no válido. Por favor, revisa los datos ingresados.',
        #    })
            
            
                
    #def post(self, request, *args, **kwargs):
    #    category = self.kwargs.get('category', None)
    #    form = AvailabilityForm(request.POST)
        
    #    if form.is_valid():
    #        data = form.cleaned_data

    #    available_rooms = get_available_rooms(category, data['check_in'], data['check_out'])
        
    #    if available_rooms is not None:
    #        booking = book_room(request, available_rooms[0], data['check_in'], data['check_out'])        
    #        return HttpResponse(booking)
    #    else:
    #        return HttpResponse('Esta categoria de habitaciones está reservada, prueba otra')
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('app:BookingListView')
        

class NewsListView(ListView):
    model = News
    template_name = 'news.html'  # Especifica el template
    context_object_name = 'noticias'  # Nombre del contexto en el template

