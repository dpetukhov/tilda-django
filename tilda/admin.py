from django.contrib import admin

from .models import TildaArticle

@admin.register(TildaArticle)
class TildaArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # распаковка архива при импорте
        archive_changed = 'archive' in form.changed_data

        # запишет файл на диск
        super(TildaArticleAdmin, self).save_model(request, obj, form, change)

        if archive_changed and obj.archive:
            obj.import_archive()
