from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Negocio
from django.contrib import messages
from geopy.geocoders import Nominatim
import ssl
import certifi

# Create your views here.

def home(request):
    error = request.GET.get('error')
    return render(request, "index.html", {'error': error})

def cadastro(request):
    error = request.GET.get('error')
    return render(request, 'cadastro.html', {'error': error})

def cadastro_validate(request):
    nome = request.POST.get("nome")
    email = request.POST.get("email")
    tipo = request.POST.get("tipo")
    estado = request.POST.get("estado")
    cidade = request.POST.get("cidade")
    rua = request.POST.get("rua")
    numero = request.POST.get("numero")
    numero_whatsapp = request.POST.get("numero_whatsapp")
    instagram_ou_website = request.POST.get("instagram_ou_website")
    descricao = request.POST.get("descricao")
    como_conheceu = request.POST.get("como_conheceu")
    email_existe = Negocio.objects.filter(email=email)

    ctx = ssl.create_default_context(cafile=certifi.where())
    geolocator = Nominatim(user_agent="ta_em_casa", ssl_context=ctx)
    endereco = f"USA, {estado}, {cidade}, {rua}, {numero}"
    local = geolocator.geocode(endereco)
    if local:
        latitude = local.latitude
        longitude = local.longitude
    else:
        messages.error(request, "O endereço fornecido não pôde ser localizado.")
        return redirect('/taemcasa/home')
    
    if not (nome and email and tipo and estado and cidade and rua and numero and numero_whatsapp and instagram_ou_website and descricao and como_conheceu):
        messages.error(request, "Preencha todos os campos necessários.")
        return redirect('/taemcasa/home')
    if not email_existe:
        negocio = Negocio(nome=nome, email=email, tipo=tipo, estado=estado, cidade=cidade, rua=rua, numero=numero, telefone_wpp=numero_whatsapp, instagram_or_website=instagram_ou_website, descricao=descricao, como_conheceu=como_conheceu, latitude=latitude, longitude=longitude)
        negocio.save()
        messages.success(request, "Negócio cadastrado com sucesso!")
    else:
        messages.error(request, "Email fornecido já está em uso.")
    return redirect('/taemcasa/home')

def negocios_json(request):
    negocios = Negocio.objects.all()
    enderecos = []
    for n in negocios:
        enderecos.append({
            'nome': n.nome,
            'tipo' : n.tipo,
            'estado' : n.estado,
            'cidade': n.cidade,
            'rua': n.rua,
            'numero' : n.numero,
            'email' : n.email,
            'telefone_wpp' : n.telefone_wpp,
            'descricao' : n.descricao,
            'instagram_or_website' : n.instagram_or_website,
            'latitude' : n.latitude,
            'longitude' : n.longitude
        })
    return JsonResponse(enderecos, safe=False)

def app(request):
    tipos = request.POST.getlist('tipo')
    return render(request, 'app.html', {'tipos' : tipos})

def login_validate(request):
    nome = request.POST.get("nome")
    email = request.POST.get("email")
    telefone = request.POST.get("telefone")

def contato_validate(request):
    nome = request.POST.get("nome")
    email = request.POST.get("email")
    telefone = request.POST.get("telefone")
