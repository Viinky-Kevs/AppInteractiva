from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from os import listdir
from IPython.display import HTML

from .forms import CustomUser, SuplierForm, MODISForm, MCD43A4Form, FilesAnalysis
from Prueba.settings import MEDIA_ROOT

import folium
import ee
import pandas as pd
import matplotlib.pyplot as plt


def config(request):
    data = {}
    form = SuplierForm()

    if request.method == 'POST':
        formulario = SuplierForm(data = request.POST)
        if formulario.is_valid():
            reason = formulario.cleaned_data['Proveedor']
            reason = dict(formulario.fields['Proveedor'].choices)[reason]
            
            formulario_1 = MODISForm(data = request.POST)
            if reason == "MODIS":
                data = {}
                form = MODISForm()
                data['MODIS'] = form
                data['form'] = "MODIS"
                if formulario_1.is_valid():
                    reason_1 = formulario.cleaned_data['Proveedor']
                    reason_1 = dict(formulario.fields['Proveedor'].choices)[reason_1]
                    data['producto_s'] = reason_1
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
    
    def get_context_data(request):

        suplier = []
        product = []
        band = []
        date_i = []
        date_f = []

        if len(band) == 0:
            band_name = 'NDVI'
        else:
            band_name = band[0]
        
        if len(date_i) == 0:
            initial_date = '2021-06-01'
        else:
            initial_date = date_i[0]
        
        if len(date_f) == 0 :
            last_date = '2021-12-01'
        else:
            last_date = date_f[0]
        
        if len(product) == 0:
            product_name = 'MODIS/006/MOD13Q1'
        else:
            product_name = product[0]
        
        if len(suplier) == 0:
            suplier_name = 'MODIS'
        else:
            suplier_name = suplier[0]

        figure = folium.Figure()
        
        worldmap = folium.Map(location=[4, -76.7], zoom_start = 6)

        worldmap.add_to(figure)

        dataset = (ee.ImageCollection(product_name)
                  .filter(ee.Filter.date(initial_date, last_date))
                  .first())
        selectdata = dataset.select(band_name)
 
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

        return {"map": figure, 
                "band_name": band_name,
                "fecha_i": initial_date,
                "fecha_f": last_date,
                "producto": product_name,
                "proveedor": suplier_name}

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

@login_required(login_url='/accounts/login/')
def analysis(request):
    context = {}
    form = FilesAnalysis()
    root = './media/'
    
    if request.method == 'POST':
        formulario = FilesAnalysis(data = request.POST)

        if formulario.is_valid():
            reason = formulario.cleaned_data['files_n']
            reason = dict(formulario.fields['files_n'].choices)[reason]
            
            file_name = str(root + reason)
            type_of = reason.split('.')
            if type_of[1] == 'csv':
                d = pd.read_csv(file_name)
                dd = d.head()
                context['table'] = d
                lista1 = []
                for j in range(len(dd)):
                    lista1.append([])
                    for i in dd:
                        lista1[j].append(dd[i][j])
                context['content'] = lista1
                context['statistics'] = d.describe().transpose()
                lista = []
                for j in range(len(d.describe().transpose())):
                    lista.append([])
                    for i in d.describe().transpose():
                        lista[j].append(d.describe().transpose()[i][j])
                context['lista'] = lista
                
                return render(request, 'AppWeb/analysis.html', context)
            elif type_of[1] == 'xlsx':
                d = pd.read_excel(file_name)
                context['table'] = d
                dd = d.head()
                lista1 = []
                for j in range(len(dd)):
                    lista1.append([])
                    for i in dd:
                        lista1[j].append(dd[i][j])
                context['content'] = lista1

                context['statistics'] = d.describe().transpose()
                lista = []
                for j in range(len(d.describe().transpose())):
                    lista.append([])
                    for i in d.describe().transpose():
                        lista[j].append(d.describe().transpose()[i][j])
                context['lista'] = lista
                return render(request, 'AppWeb/analysis.html', context)
    
    context['form'] = form

    return render(request, 'AppWeb/analysis.html', context)
