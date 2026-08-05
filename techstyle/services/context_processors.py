from .models import BusinessInfo


def business_info(request):
    info = BusinessInfo.objects.first()
    if not info:
        info = BusinessInfo.objects.create()
    return {
        'business_info': info
    }
