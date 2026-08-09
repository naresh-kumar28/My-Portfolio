from django.conf import settings

def portfolio_context(request):
    return {
        'WHATSAPP_NUMBER': getattr(settings, 'CONTACT_PHONE_NUMBER'),
    }
