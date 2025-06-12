from django.contrib import admin

# Personalización del admin
admin.site.site_header = 'Administración de Ferremas'
admin.site.site_title = 'Panel Admin Ferremas'
admin.site.index_title = 'Bienvenido al Panel Administrativo'
admin.site.site_url = '/admin-page/'  # El logo clickeable (opcional)
