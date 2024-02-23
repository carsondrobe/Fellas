from django.contrib import admin
from .models import User, WeatherStation, StationData, UserProfile, Dashboard, Alert, Feedback, ResponseFromAdmin

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WeatherStation)
admin.site.register(StationData)
admin.site.register(Dashboard)
admin.site.register(Alert)
admin.site.register(Feedback)
admin.site.register(ResponseFromAdmin)


