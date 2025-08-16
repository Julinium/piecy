from django.conf import settings

def main_data(request=None):
    """
    Provides main data to all templates' context 
    """
    context = {}
    languages = settings.LANGUAGES
    messages_display = settings.MESSAGES_DISPLAY

    if request:
        if request.user:
            if request.user.is_authenticated:
                tenant = request.user.tenant
                context['tenant'] = tenant

    context['LANGUAGES'] = languages
    context['MESSAGES_DISPLAY'] = messages_display

    return context
