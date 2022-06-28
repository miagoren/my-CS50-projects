from django.contrib import admin
from .models import *

# Models to show on admin view
admin.site.register(User)
admin.site.register(Opportunity)
admin.site.register(Conversation)
admin.site.register(Message)
