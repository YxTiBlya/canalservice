from django.shortcuts import render
from .scripts import *
from .models import table

data = {
    'title': 'Каналсервис',
}

# стандартная функция вызова страницы с передачей в нее словаря данных
def index(request):
    db()
    Table = table.objects.all()
    data['table'] = Table
    return render(request, 'index.html', data)
