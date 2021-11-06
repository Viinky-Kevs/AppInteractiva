from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from os import listdir

from .forms import CustomUser, SuplierForm, MODISForm
from agrointeractivo.settings import MEDIA_ROOT

import folium
import ee

def config(request):
    data = {}
    form = SuplierForm()

    if request.method == 'POST':
        formulario = SuplierForm(data = request.POST)
        if formulario.is_valid():
            reason = formulario.cleaned_data['Proveedor']
            reason = dict(formulario.fields['Proveedor'].choices)[reason]
            
            if reason == "MODIS":
                data = {}
                form = MODISForm()
                data['MODIS'] = form
                data['form'] = "MODIS"
                return render(request, 'AppWeb/config.html', data)
            else:
                data['MODIS'] = reason
                return render(request, 'AppWeb/config.html', data)
    data["form"] = form
    return render(request, 'AppWeb/config.html', data)


## Módulo de mapa interactivo

class home(TemplateView):
    ee.Initialize()
    template_name = 'AppWeb/map.html'
    
    def data_get(request, self, *args, **kwargs):
        self.form = SuplierForm(request.POST or None)
        return super().data_get(request, *args, **kwargs)

    def get_context(self, *args, **kwargs):
        return {'form': self.form}
    
    def get_context_data(request):

        figure = folium.Figure()
        
        worldmap = folium.Map(location=[4, -76.7], zoom_start = 6)

        worldmap.add_to(figure)

        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                  .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
                  .first())
        selectdata = dataset.select('NDVI')
 
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48']}

        map_id_dict = ee.Image(selectdata).getMapId(vis_paramsNDVI)
       
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'NDVI',
                    overlay = True,
                    control = True
                    ).add_to(worldmap)

        worldmap.add_child(folium.LayerControl())
 
        figure.render()

        return {"map": figure}

## Inicio de página
def index(request):
	return render(request, 'AppWeb/index.html')

## Registro de usuario
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

## Módulo de semillero
def group(request):
    return render(request, 'AppWeb/group.html')

## Módulo de cargar archivos
@login_required(login_url='/accounts/login/')
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
    
    context['files'] = listdir(MEDIA_ROOT)

    return render(request, 'AppWeb/upload.html', context)

