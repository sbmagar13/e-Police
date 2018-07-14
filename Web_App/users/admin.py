from django.contrib import admin

# Register your models here.
from users.models import PasModel,LcnModel,VoterModel,CtzModel

admin.site.register(PasModel)
admin.site.register(LcnModel)
admin.site.register(VoterModel)
admin.site.register(CtzModel)

