from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CustomUser, FileFieldForm
from folium import plugins
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import folium
import ee
ee.Initialize()


class home(TemplateView):
    template_name = 'AppWeb/map.html'

    # Define a method for displaying Earth Engine image tiles on a folium map.
    def get_context_data(request):
        figure = folium.Figure()
        
        #create Folium Object
        m = folium.Map(location=[4, -65], zoom_start = 6)

        #add map to figure
        m.add_to(figure)

        
        #select the Dataset Here's used the MODIS data
        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                  .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
                  .first())
        modisndvi = dataset.select('NDVI')

        #Styling 
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        
        #add the map to the the folium map
        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
       
        #GEE raster data to TileLayer
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'NDVI',
                    overlay = True,
                    control = True
                    ).add_to(m)

        
        #add Layer control
        m.add_child(folium.LayerControl())
       
        #figure 
        figure.render()
         
        #return map
        return {"map": figure}

def index(request):
	return render(request, 'AppWeb/index.html')

def register_user(request):
    data = { 'form': CustomUser()}
    if request.method == 'POST':
        formulario = CustomUser(data = request.POST)
        if formulario.is_valid():
            formulario.save()

            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "El usuario a sido creado satisfactoriamente")

            return redirect(to = "home")

        data["form"] = formulario    
    return render(request, 'registration/registration.html',data)

def group(request):
    return render(request, 'AppWeb/group.html')

def upload(request):
    context = {}
    if request.method == 'POST':
        upload_file = request.FILES['Archivo']
        fs = FileSystemStorage()
        fs.save(upload_file.name, upload_file)
        name = upload_file.name
        size = upload_file.size
        context['name'] = name
        context['size'] = size
    return render(request, 'AppWeb/upload.html', context)