import os
import re
import shutil
import zipfile


class TildaArchive(object):
    def __init__(self, path):
        self.path = path

    def content(self, zipinfo, f):
        pass

    def extract_path(self, zipinfo):
        return False

    def done(self):
        pass

    def process(self):
        with zipfile.ZipFile(self.path) as zf:
            for zipinfo in zf.infolist():
                # парсинг контента
                with zf.open(zipinfo) as f:
                    self.content(zipinfo, f)

                # распаковка
                with zf.open(zipinfo) as f:
                    save_as = self.extract_path(zipinfo)
                    if save_as:
                        self.save(f, save_as)

            self.done()

    def save(self, source, targetpath):
        # Create all upper directories if necessary
        upperdirs = os.path.dirname(targetpath)
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs)

        with open(targetpath, "wb") as target:
            shutil.copyfileobj(source, target)

        return targetpath


class IrkruTildaArchive(TildaArchive):
    def __init__(self, path, material):
        super(IrkruTildaArchive, self).__init__(path)

        self.material = material
        self.styles = None
        self.scripts = None
        self.body = None

        self.extract_root = material.tilda_extract_root
        self.extract_url = material.tilda_extract_url

    def content(self, zipinfo, f):
        """
        Из html-файла парсит ссылки на стили и скрипты
        """
        filename = self.strip_project(zipinfo.filename)

        if re.match(r'page\d+.html', filename):
            html = f.read().decode('utf-8')
            self.styles, self.scripts = self.assets(html)
        elif re.match(r'files/page\d+body.html', filename):
            self.body = f.read().decode('utf-8')

    def done(self):
        """
        Вызывается после обработки всех файлов
        """
        if self.styles:
            self.material.styles = '\n'.join(self.styles)

        if self.scripts:
            self.material.scripts = '\n'.join(self.scripts)

        if self.body:
            self.material.tilda_content = self.body

        self.material.save()

    def extract_path(self, zipinfo):
        filename = self.strip_project(zipinfo.filename)
        path = False

        if self.is_css(filename) or self.is_js(filename) or self.is_image(filename):
            path = os.path.join(self.extract_root, filename)

        return path

    @staticmethod
    def assets(html):
        styles, scripts = None, None

        link_pattern = re.compile(r'''<link[^>]+rel=["']stylesheet["'].+?>''')
        styles = link_pattern.findall(html)

        link_pattern = re.compile(r'''<script\s+src=["'].+?></script>''')
        scripts = link_pattern.findall(html)

        return styles, scripts

    @staticmethod
    def strip_project(filename):
        return re.sub(r'project\d+/', '', filename).lstrip('/')

    @staticmethod
    def is_css(filename):
        return filename.startswith('css/') and filename.endswith('.css')

    @staticmethod
    def is_js(filename):
        return filename.startswith('js/') and filename.endswith('.js')

    @staticmethod
    def is_image(filename):
        return re.match(r'(project\d+/)?images/[-a-z0-9_]+\.(png|jpg|jpeg)', filename, re.I)
