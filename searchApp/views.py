from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .cron.emailSender import sendEmail
from .handlers import emag


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def dashboard(request):
    products = []
    if request.method == "POST":
        searchInput = request.POST.get('search')
        emagUrl = "https://www.emag.ro/search/" + searchInput
        products = emag.getProducts(emagUrl)

    context = {
        'products': products
    }
    return render(request, 'searchApp/dashboard.html', context)



@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        fromField = request.POST.get("email")
        subject = 'New FeedBack from {}'.format(fromField)
        body = request.POST.get("feedback")
        sendEmail(fromField, subject, body,
                  replyTo=['adrian.balcan@feedcheck.co', 'catalin.briscan@feedcheck.co', 'maria.antal@feedcheck.co'])

    return HttpResponse('Success')