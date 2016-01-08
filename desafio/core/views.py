import csv
import unicodedata
from desafio.core.forms import UploadForm
from desafio.core.models import UploadFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum, F
from django.shortcuts import render, resolve_url as r
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from six import StringIO


def home(request):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'index.html')

    return HttpResponseRedirect(r('upload'))


def billing_file(import_name):
    files = UploadFile.objects.filter(import_name=import_name).aggregate(billing=Sum(F('item_price')*F('purchase_count')))
    return files['billing']


def save_file(request):
    form = UploadForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, 'upload.html', {'form': UploadForm()})

    data = request.FILES['file']
    file_name = data.name
    import_name = file_name + str(now())[:19]
    data = data.read().decode('utf-8').split('\n')
    list_content_file = []
    for line in data[1:]:
        reader = csv.DictReader(StringIO(line), delimiter='\t', quoting=csv.QUOTE_NONE)
        fields = tuple(unicodedata.normalize('NFKD', r)
                           .encode('ASCII', 'ignore')
                           .decode('utf-8').lower() for r in reader.fieldnames)
        upload_file = UploadFile()
        upload_file.unpack_line(fields, import_name)
        list_content_file.append(upload_file)

    UploadFile.bulk_insert(list_content_file)

    #calcula receita bruta
    value_billing = billing_file(import_name)

    return render(request, 'upload.html', {'form': form, 'receita': value_billing, 'file_name': file_name})


@login_required()
def upload(request):
    form = UploadForm()
    if request.method == 'POST':
        return save_file(request)

    return render(request, 'upload.html', {'form': form})