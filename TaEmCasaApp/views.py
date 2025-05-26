from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Negocio
from django.contrib import messages
from geopy.geocoders import Nominatim
import ssl
import certifi
from django.core.mail import send_mail
from django.conf import settings
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
    local = geolocator.geocode(endereco, timeout=None)
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
        if n.permitido:
            enderecos.append({
                'id' : n.id,
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
    raio = request.POST.get('raio')

    if request.GET.getlist('tipo'):
        tipos = request.GET.getlist('tipo')
    if request.GET.get('raio'):
        raio = request.GET.get('raio')
        
    return render(request, 'app.html', {'tipos' : tipos, 'raio' : raio})

import smtplib
import ssl
import certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(request, nome, email_destino, negocio):
    assunto = f'Informações sobre o negócio {negocio.nome}'
    corpo = f"""
    Olá, {nome}!

    Aqui estão as informações sobre o negócio:

    📝 {negocio.nome}, {negocio.tipo}
    📍 {negocio.rua}, {negocio.numero}, {negocio.cidade} - {negocio.estado}
    📞 {negocio.telefone_wpp}
    🌐 {negocio.instagram_or_website}
    📧 {negocio.email}

    Descrição:
    {negocio.descricao}
        """

    remetente = 'fernandobarreto864@gmail.com'
    senha = 'xgem nlic iojw ytwc'
    destinatario = email_destino

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    context = ssl.create_default_context(cafile=certifi.where())

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls(context=context)
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatario, msg.as_string())
            messages.success(request, "E-mail enviado com sucesso!")
    except Exception as e:
        messages.error(request, "Houve uma falha no envio do e-mail")


def login_validate(request):
    negocioid = request.GET.get("negocio")
    negocio = Negocio.objects.get(id=negocioid)
    nome = request.POST.get("nome")
    email = request.POST.get("email")

    enviar_email(request, nome, email, negocio)

    query = request.GET.get('query')
    return redirect(f'/taemcasa/app/{query}')

def receber_email(request, nome, email, telefone, mensagem):
    assunto = f'O usuario {nome}, de email {email} e telefone {telefone} entrou em contato!'
    corpo = f"""
    - {nome}

    {mensagem}
        """

    remetente = 'fernandobarreto864@gmail.com'
    senha = 'xgem nlic iojw ytwc'
    destinatario = 'fernandobarreto864@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    context = ssl.create_default_context(cafile=certifi.where())

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls(context=context)
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatario, msg.as_string())
            messages.success(request, "E-mail enviado com sucesso!")
    except Exception as e:
        messages.error(request, "Houve uma falha no envio do e-mail")

def contato_validate(request):
    nome = request.POST.get("nome")
    email = request.POST.get("email")
    telefone = request.POST.get("telefone")
    mensagem = request.POST.get('mensagem')

    receber_email(request, nome, email, telefone, mensagem)

    return redirect('/taemcasa/app')
