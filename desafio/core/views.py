import unicodedata
from desafio.core.forms import UploadForm
from desafio.core.models import UploadFile
from django.db.models import Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r
from django.utils.timezone import now


def home(request):
    return render(request, 'index.html')


def billing_file(import_name):
    files = UploadFile.objects.filter(import_name=import_name).aggregate(billing=Sum(F('item_price')*F('purchase_count')))
    return files['billing']


def save_file(request):
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        data = request.FILES['file']
        file_name = data.name
        import_name = file_name + str(now())[:19]
        data = data.read().decode('utf-8').split('\n')
        list_content_file = []
        for line in data[1:]:
            upload_file = UploadFile()
            # Normalize content line
            line = unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode('utf-8').lower().split('\t')
            upload_file.unpack_line(tuple(line), import_name)
            list_content_file.append(upload_file)

        UploadFile.bulk_insert(list_content_file)

        #calcula receita bruta
        value_billing = billing_file(import_name)
        return render(request, 'upload.html', {'form': form, 'receita': value_billing, 'file_name': file_name})

    return render(request, 'upload.html', {'form': UploadForm()})

def upload(request):
    form = UploadForm()
    if request.method == 'POST':
        return save_file(request)

    return render(request, 'upload.html', {'form': form})