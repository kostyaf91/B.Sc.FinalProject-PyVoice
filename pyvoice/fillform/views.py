import tempfile
import socket

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, InvoiceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.template.loader import render_to_string, get_template
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import account, invoice_detail

from .string_functions import convert_string_to_list


# Create your views here.

def home(request):
    return render(request, 'fillform/dashboard.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            # print('form ', form)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        # print(context)
        return render(request, 'fillform/register.html', context)


def loginPage(request):
    current_user = request.user
    # print(current_user.id)
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            # print("request ", request)
            # print(request.user)
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            # print('USER****************', user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'fillform/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@csrf_protect
def getValues(request):
    invoice_title = request.POST.get('invoice_title')

    """user details"""
    business_Name = request.POST.get('business_Name')
    business_Email = request.POST.get('business_Email')
    business_Address = request.POST.get('business_Address')
    business_Phone = request.POST.get('business_Phone')
    business_Number = request.POST.get('business_Number')

    """client details"""
    client_Name = request.POST.get('client_Name')
    client_Email = request.POST.get('client_Email')
    client_Address = request.POST.get('client_Address')
    client_Phone = request.POST.get('client_Phone')

    """Invoice details"""
    invoiceno = request.POST.get('invoiceno')
    date = request.POST.get('date')

    """item description"""
    description = request.POST.get('hidden_item')

    amount = request.POST.get('hidden_amount')

    terms = request.POST.get('terms')

    image = request.FILES['photo']
    # print("***",image)

    invoice = invoice_detail(
        invoice_Number=invoiceno,
        user=request.user,
        client_Name=client_Name,
        client_Email=client_Email,
        client_Address=client_Address,
        client_Phone=client_Phone,
        date=date,
        table_Items=description,
        amounts=amount,
        terms=terms,
        logo=image
    )
    invoice.save()
    description = convert_string_to_list(description)
    print(invoice.logo.url)
    logourl = 'http://'+request.META['HTTP_HOST'] + invoice.logo.url
    # print(logourl)
    # print(request.META['HTTP_HOST'],'************************')

    data = {
        'invoice_title': invoice_title,
        'invoice_logo' : logourl,
        'business_Name': business_Name,
        'business_Email': business_Email,
        'business_Address': business_Address,
        'business_Phone': business_Phone,
        'business_Number': business_Number,

        'client_Name': client_Name,
        'client_Email': client_Email,
        'client_Address': client_Address,
        'client_Phone': client_Phone,

        'invoiceno': invoiceno,
        'date': date,

        'description': description,
        'amount': amount,

        'terms': terms

    }
    # print(data)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename =Invoice' + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string('fillform/PDF_HTML.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    # print(invoiceno,"invoice number", type(invoiceno))
    invoiceno = int(invoiceno)
    invoiceno += 1
    # print(invoiceno, "invoice number", type(invoiceno))
    invoiceUser = account.objects.get(username=request.user)
    # print(invoiceUser," invoiceUSer")

    invoiceUser.invoice_count = invoiceno
    invoiceUser.save()

    return response
    # return HttpResponse(data)


@login_required(login_url='login')
def generate_invoice(request):
    # print(request.META['HTTP_HOST'],'************************')
    context = {}
    user = request.user
    invoice_count = account.objects.filter(username=user).values('invoice_count')
    # print("invoice count ",invoice_count,"type ",type(invoice_count))
    invoice_count = invoice_count[0]['invoice_count']
    # print("invoice count ",invoice_count,"type ",type(invoice_count))

    invoice_count = "{0:0=5d}".format(invoice_count)

    current_user = account.objects.get(username=user)
    context['invoice_count'] = invoice_count
    context['business_Name'] = current_user.business_Name
    context['business_Email'] = current_user.business_Email
    context['business_Address'] = current_user.business_Address
    context['business_Phone'] = current_user.business_Phone
    context['business_Number'] = current_user.business_Number

    return render(request, 'fillform/generate.html', context)

    # user_invoice = invoice_detail.objects.get(user=current_user)
    # context['logo_url'] = user_invoice.logo.url

    # if request.method == "POST":
    #     form = InvoiceForm(request.POST, request.FILES)
    #     # form.fields['user'].initial = current_user
    #     print(form)
    #
    #     # print('form.user ', form.user)
    #     if form.is_valid():
    #         print("form.is_valid ", form.is_valid())
    #         form.save()
    #     else:
    #         print(form.errors)
    #     # img = form.cleaned_data.get("geeks_field")
    #     #  obj = GeeksModel.objects.create(
    #     #      title=name,
    #     #      img=img
    #     #  )
    #     #  obj.save()
    #     #  print(obj)
    #
    # else:
    #     form = InvoiceForm(initial={'user': current_user})
    #
    # # print(form)
    # context['form'] = form

    # user = request.user
    # current_user = account.objects.get(username=user)
    # form = InvoiceForm(instance=current_user)
    #
    # if request.method == 'POST':
    #     form = InvoiceForm(request.POST, request.FILES)
    #     print(form)
    #
    #     if form.is_valid():
    #         print("form.is_valid ", form.is_valid())
    #         form.save()
    #
    # user_invoice = invoice_detail.objects.get(user=current_user)
    # print("logourl ", user_invoice.logo.url)
    # context = {
    #     'business_Name': current_user.business_Name,
    #     'business_Email': current_user.business_Email,
    #     'business_Address': current_user.business_Address,
    #     'business_Phone': current_user.business_Phone,
    #     'business_Number': current_user.business_Number,
    #     'form': form,
    #     'logo_url': user_invoice.logo.url
    #
    # }
    #
    # # print(context)
    # return render(request, 'fillform/Invoice_form.html', context)


def generate_invoice_dummy(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename =Invoice' + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    # description = '[["LED ","12 watt","220","2","$440.00"],["Fan ","12 watt","1200","2","$2400.00"]]'
    # description = convert_string_to_list(description)
    # data = {'invoice_title': 'INVOICE',
    #         'business_Name': 'mastrolinks',
    #         'business_Email': 'mastrolinks@gmail.com',
    #         'business_Address': 'Chandigarh',
    #         'business_Phone': '987654321',
    #         'business_Number': '789456123',
    #         'client_Name': 'royal',
    #         'client_Email': ' royal@qwe.com',
    #         'client_Address': 'Zirakpur',
    #         'client_Phone': '9888548923',
    #         'invoiceno': ' inv00921',
    #         'date': '2020-09-14',
    #         'description': description,
    #         'amount': '$2840.00',
    #         'terms': 'Conditions apply'}
    data = {}
    html_string = render_to_string('fillform/Untitled-1.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def invoice_dummy(request):
    if request.method == "POST":
        invoice_title = request.POST.get('invoice_title')
        client_Name = request.POST.get('client_Name')
        client_Email = request.POST.get('client_Email')
        client_Address = request.POST.get('client_Address')
        client_Phone = request.POST.get('client_Phone')

    context = {}
    user = request.user
    current_user = account.objects.get(username=user)
    context['business_Name'] = current_user.business_Name
    context['business_Email'] = current_user.business_Email
    context['business_Address'] = current_user.business_Address
    context['business_Phone'] = current_user.business_Phone
    context['business_Number'] = current_user.business_Number
    context['invoice_no'] = current_user.invoice_no

    # print("request.user ", request.user)
    return render(request, 'fillform/generate.html', context)
