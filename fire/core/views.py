# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
from bs4 import BeautifulSoup #html v python X
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import SaveChas
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import email
import json
from django.contrib.auth import logout as django_logout
import logging

logger = logging.getLogger(__name__)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY,
)

def base_view(request):
    return render(request, 'base.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if 'remember' in request.POST:
                request.session.set_expiry(2592000)
            else:
                request.session.set_expiry(0)
            if '@' in username and '.' in username:
                user.role = 'barber'
            elif username == 'Admin':
                user.role = 'admin'
                user.picture = None
            else:
                user.role = 'user'
                user.picture = None
                
            user.save()
            login(request, user)
            return redirect('home_view')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'}, status=401)
    else:
        return render(request, 'login.html')

def singup_view(request):
    if request.method =='POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if len(firstname) > 50 or len(lastname) > 50 or len(username) > 50:
            return render(request, 'singup.html', {'error': 'Firstname, lastname, and username must be 50 characters or less'}, status=401)
        if len(password) < 6 or len(password1) < 6:
            return render(request, 'singup.html', {'error': 'Password must be at least 6 characters long'}, status=401)
        if '@' in username:
            return render(request, 'singup.html', {'error': 'Username cannot contain @'}, status=401)
        if password == password1:
            if not User.objects.filter(username=username).exists():
                user = User(firstname=firstname, lastname=lastname, username=username, saved=None, bio=None, picture=None)
                user.set_password(password) 
                user.save()
                return redirect('home_view')
            else:
                return render(request, 'singup.html', {'error': 'Username already exists'}, status=401)
        else:
            return render(request, 'singup.html', {'error': 'Passwords do not match'}, status=401)
        
    else:
        return render(request, 'singup.html')

def save_chas_view(request):
    if request.method == 'POST':
        barbers = User.objects.filter(role='barber')  # vzimame vsichki barberi 
        html = render_to_string('save_chas.html', {'request': request})
        soup = BeautifulSoup(html, 'html.parser') #tyrsene v html
        print("POST data:", request.POST)
        phone = request.POST.get('phone')
        phone = f'+359{phone}' if len(phone) == 9 else None
        if not phone:
            return render(request, 'save_chas.html', {'error': 'Invalid phone number'}, {'barbers': barbers}, status=400)
        date = request.POST.get('date')
        time = request.POST.get('time')
        if request.user.is_authenticated:
            first_input = soup.find(id='firstname')
            if first_input:
                first_input.decompose()  # removing the input field from the HTML
            last_input = soup.find(id='lastname')
            if last_input:
                last_input.decompose()
            firstname = request.user.firstname
            lastname = request.user.lastname
        else:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')  
        barber_id = request.POST.get('barber_id')  # Get barber_id instead of barber_name 
        print("barber_id:", barber_id) 
        if request.method == 'POST':
            SaveChas.objects.create(     # zapazvame v bazata danni
                phone=phone,
                date=date,
                time=time,
                firstname=firstname,
                lastname=lastname,
                barber=User.objects.filter(id=barber_id).first() if barber_id else None
            )
            return render(request, 'save_chas.html', {'success': 'Appointment saved successfully!', 'barbers': barbers}) 
    else:
        barbers = User.objects.filter(role='barber')
        return render(request, 'save_chas.html', {'barbers': barbers}) 

def remove_chas_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        user = request.user if request.user.is_authenticated else None
        firstname = user.firstname
        lastname = user.lastname
        chas = SaveChas.objects.get(phone=phone, date=date, time=time, firstname=firstname, lastname=lastname)
        barber = User.objects.get(firstname = chas.barber.firstname, lastname = chas.barber.lastname)
        email.send_email(barber, chas)
        chas.delete()
        return render(request, 'save_chas.html', {'success': 'Appointment removed successfully!'})
    else:
        return render(request, 'save_chas.html', {'error': 'Invalid request'}, status=400)
    
def display_saved_chas_view(request):
    user = request.user
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    if not day or not month or not year:
        logger.warning("Invalid request") 
        
    else:
        day = int(day)
        month = int(month)
        year = int(year)
        
        chas = SaveChas.objects.filter(
            date__day = day,
            date__month = month,
            date__year = year
        )
        chasove = []
        for chas in chas:
            den = chas.date.strftime('%d.%m.%Y')
            hours = chas.time.strftime('%H')
            barber_id = chas.barber.id
            chas_user_id = chas.user.id if chas.user else None
            firstname = chas.firstname
            lastname = chas.lastname
            chasove.append({"date": den, "hour": hours, "barber_id": barber_id, "user_id": chas_user_id, "firstname": firstname, "lastname": lastname})
        return JsonResponse({'chasove': chasove}, status=200)

def add_barber_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        picutre = request.FILES.get('picture')
        bio = request.POST.get('bio')
        if not User.objects.filter(username=username).exists():
            user = User(firstname=firstname, lastname=lastname, username=username, saved=None, bio=bio, picture=picutre)
            user.set_password(password) 
            user.role = 'barber'
            user.save()
            return render(request, 'home.html', {'alert': 'Barber added successfully!'})
        else:
            return render(request, 'home_admin.html', {'error': 'Username already exists'}, status=409)
        
    return render(request, 'home_admin.html', {'error': 'Not saved'})

def remove_barber_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            barber = User.objects.get(username=username, role='barber')
            barber.delete()
            return render(request, 'home.html', {'alert': 'Barber removed successfully!'})
        except Exception as e:
            return render(request, 'home.html', {'error': f'Error removing barber: {str(e)}'}, status=401)
        
def logout(request):        
    if request.user.is_authenticated:
        django_logout(request)
    return redirect('login_view')
            
def home_view(request):
    barbers = User.objects.filter(role='barber')
    return render(request, 'home.html', {'barbers': barbers})

def home_admin_view(request):
    return render(request, 'home_admin.html')

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_message = body.get('message')
        barbers = User.objects.filter(role='barber')
        barber_bios = ""
        for barber in barbers:
            bio = barber.bio if barber.bio else "Няма налична информация за този фризьор."
            barber_bios += f"{barber.firstname} {barber.lastname}: {bio}\n"

        system_prompt = f"""
            Роля: Ти си AI асистент във фризьорски салон, който говори и отговаря на български език. Помагаш на клиентите с информация и записване на часове.

            Инструкции:

            1. Поздравявай клиентите учтиво и питай с какво можеш да им помогнеш.
            2. Предоставяй точна информация за услугите на салона — подстригване, бръснене, стилизиране и специални процедури, както и техните цени.
            3. Информирай за налични промоции и отстъпки.
            4. Представяй профилите на фризьорите — техния опит, специалности и препоръки от клиенти.
            5. Препоръчвай подходящ фризьор според нуждите и предпочитанията на клиента.
            6. Помагай при записване на час — предлагай свободни часове и събирай необходимата информация (име, желан фризьор, услуга).
            7. Отговаряй на често задавани въпроси относно работното време, политики за анулация и начини на плащане.
            8. Давай съвети за грижа и поддръжка след подстригване или процедура.
            9. Насърчавай клиентите да оставят обратна връзка и предлагай допълнителни услуги или продукти според предишните им посещения.
            10. Винаги бъди учтив, професионален и ясен.
            11. Вземай под внимание българските традиции и предпочитания относно прически и грижа за косата.
            12. Ако не разбираш нещо, учтиво помоли за пояснение.
            13. Завършвай разговора с благодарност и покана клиентът да се върне при нужда.
            Барбери:
            {barber_bios} 
                    """

        try:
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"

        return JsonResponse({'reply': reply})
    
    return render(request, 'chat.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        return JsonResponse({'status': 'success', 'message': message})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})







