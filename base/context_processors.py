from django.conf import settings

def main_data(request=None):
    context = {}
    LANGUAGES = settings.LANGUAGES
    MESSAGES_DISPLAY = settings.MESSAGES_DISPLAY
    
    context['LANGUAGES'] = LANGUAGES
    context['MESSAGES_DISPLAY'] = MESSAGES_DISPLAY

    return context
