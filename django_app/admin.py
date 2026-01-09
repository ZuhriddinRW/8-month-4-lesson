from django.contrib import admin
from .models import User, CodeVerification

admin.site.register ( [User, CodeVerification] )