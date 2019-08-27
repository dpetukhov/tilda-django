import datetime
import os

from django.conf import settings
from django.db import models

from .utils import IrkruTildaArchive


class TildaArticle(models.Model):
    tilda_content = models.TextField(u'HTML-код', blank=True)
    styles = models.TextField(u'Стили', blank=True)
    scripts = models.TextField(u'Скрипты', blank=True)
    archive = models.FileField(u'Импорт из файла', blank=True, null=True, upload_to='tilda/zip/')

    class Meta:
        verbose_name = u'статья (Тильда)'
        verbose_name_plural = u'статьи (Тильда)'

    def _extract_path(self):
        return u'tilda/{year}/{folder}/'.format(
            year=datetime.date.today().year,
            folder=os.path.basename(os.path.splitext(self.archive.path)[0])
        )

    @property
    def tilda_extract_root(self):
        """Путь к папке, в которую разархивированы файлы после импорта"""
        if self.archive:
            return settings.MEDIA_ROOT + self._extract_path()

    @property
    def tilda_extract_url(self):
        """URL папки с распакованными файлами"""
        if self.archive:
            return settings.MEDIA_URL + self._extract_path()

    def prepare_content(self):
        """Возвращает готовый к выводу хтмл"""
        result = self.tilda_content.replace('="images/', '="{}images/'.format(self.tilda_extract_url))
        result = result.replace("url('images/", "url('{}images/".format(self.tilda_extract_url))
        return result

    def prepare_scripts(self):
        return self.scripts.replace('src="js/', 'src="{}js/'.format(self.tilda_extract_url))

    def prepare_styles(self):
        return self.styles.replace('href="css/', 'href="{}css/'.format(self.tilda_extract_url))

    def import_archive(self):
        """Распаковать и импортировать загруженный в `archive` файл из Тильды"""
        if self.archive:
            archive = IrkruTildaArchive(self.archive, material=self)
            archive.process()
