from django.contrib import admin
from .models import Module, Professor, ModuleInstance, Rating
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register custom User model
admin.site.register(User, UserAdmin)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_code', 'name')
    search_fields = ('module_code', 'name')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('professor_id', 'name')
    search_fields = ('professor_id', 'name')

@admin.register(ModuleInstance)
class ModuleInstanceAdmin(admin.ModelAdmin):
    list_display = ('module', 'year', 'semester', 'get_professors')
    list_filter = ('year', 'semester', 'module')
    filter_horizontal = ('professors',)

    def get_professors(self, obj):
        return ", ".join([p.professor_id for p in obj.professors.all()])
    get_professors.short_description = "Professors"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'professor', 'module_instance', 'rating')
    list_filter = ('rating', 'professor', 'module_instance__module')
    search_fields = ('user__username', 'professor__professor_id')