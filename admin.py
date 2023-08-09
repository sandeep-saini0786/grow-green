from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Post)
class NowKnowHowThisGonnaWork(admin.ModelAdmin):
    filter_horizontal  = ('tags',)
    class Media: # This should be remain same 
        js = ('js/tinyinjector.js',) 
admin.site.register(Tags)
admin.site.register(FeaturedPost)
admin.site.register(RecentWork)
# admin.site.register(Post)
admin.site.register(Comment)