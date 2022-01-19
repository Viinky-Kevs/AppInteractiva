from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import glob
from django.forms.forms import Form
import pandas

class CustomUser(UserCreationForm):
	
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1','password2']
		widgets = {
			'field' : forms.TextInput(attrs={'class':'myfield'})
		}

SUPLIERS =(
    ("MODIS", "MODIS"),
    ("Landsat", "Landsat"),
    ("Sentinel", "Sentinel"),
)

class SuplierForm(forms.Form):
    Proveedor = forms.ChoiceField(choices = SUPLIERS)

MODIS = [("MODIS/006/MCD43A4","Reflectancia ajustada diaria (500m)"),
        ("MODIS/006/MCD43A3", "Albedo (500m)"), 
        ("MODIS/006/MCD43A2", "Calidad Albedo (500m)"), 
        ("MODIS/006/MOD09GQ", "Reflectancia de la superficie global (250m)"), 
        ("MODIS/006/MOD10A1", "Cobertura de nieve global (500m)"), 
        ("MODIS/006/MOD11A1", "Temperatura de la superficie de la tierra (1km)"), 
        ("MODIS/006/MOD09GA", "Reflectancia de la superficie global (1km y 500m)"), 
        ("MODIS/006/MODOCGA", "Reflectancia del oceano (1km)"), 
        ("MODIS/006/MOD14A1", "Anomalias termales y fuego diario (1km)"), 
        ("MODIS/006/MCD43A1", "BRDF - Parámetros del modelo Albedo (500m)"), 
        ("MODIS/006/MCD15A3H", "Índice de área foliar"), 
        ("MODIS/006/MOD09Q1", "Reflectancia de la superficie global (250m)"), 
        ("MODIS/006/MOD09A1", "Reflectancia de la superficie global (500m)"), 
        ("MODIS/006/MOD11A2", "Temperatura de la superficie de la tierra (1km)"), 
        ("MODIS/006/MOD14A2", "Anomalias termales (1km)"),
        ("MODIS/006/MOD17A2H", "Productividad primaria bruta (500m)"), 
        ("MODIS/006/MOD16A2", "Evapotranspiración neta (500m)"), 
        ("MODIS/006/MOD13Q1", "Índices de vegetación (250m)"), 
        ("MODIS/006/MOD13A1", "Índices de vegetación (500m)"), 
        ("MODIS/006/MOD13A2", "Índices de vegetación (1km)"), 
        ("MODIS/006/MCD64A1", "Área quemada (500m)"), 
        ("MODIS/006/MOD08_M3", "Atmósfera producto global"), 
        ("MODIS/006/MCD12Q1", "Cobertura superficial anual (500M)"), 
        ("MODIS/006/MOD17A3H", "Producción neta primaria (500m)"), 
        ("MODIS/006/MOD44W", "Mascara de agua derivada de MODIS y SRTM (250m)") 
        ]

class MODISForm(forms.Form):
    Colecciones_de_MODIS = forms.ChoiceField(choices = MODIS)

MCD43A4 = [('Nadir_Reflectance_Band1','Banda 1'),
            ('Nadir_Reflectance_Band2','Banda 2'),
            ('Nadir_Reflectance_Band3','Banda 3'),
            ('Nadir_Reflectance_Band4','Banda 4'),
            ('Nadir_Reflectance_Band5','Banda 5'),
            ('Nadir_Reflectance_Band6','Banda 6'),
            ('Nadir_Reflectance_Band7','Banda 7'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band1', 'BRDF banda 1'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band2', 'BRDF banda 2'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band3', 'BRDF banda 3'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band4', 'BRDF banda 4'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band5', 'BRDF banda 5'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band6', 'BRDF banda 6'),
            ('BRDF_Albedo_Band_Mandatory_Quality_Band7', 'BRDF banda 7')
            ]

class MCD43A4Form(forms.Form):
    bandas = forms.ChoiceField(choices = MCD43A4)

files = glob.glob('./media/*')
options = []
for i in files:
    dir_f = i
    a = dir_f.split('/')
    b = a[2].split('.')
    options.append((b[0],a[2]))

class FilesAnalysis(forms.Form):
    files_n = forms.ChoiceField(choices = options, label = "Archivos disponibles")