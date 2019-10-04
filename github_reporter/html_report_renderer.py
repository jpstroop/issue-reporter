from mako.lookup import TemplateLookup
from os.path import abspath, dirname, join

TITLE = 'PUL GitHub Issues'

class HTMLReportRenderer():

    def __init__(self):
        project_root = abspath(dirname(dirname(__file__)))
        templates_dir = join(project_root, 'templates')
        tmp_dir = join(project_root, 'tmp')
        self.lookup = TemplateLookup(directories=[templates_dir], module_directory=tmp_dir)

    def render(self, template, **kwargs):
        base_template = self.lookup.get_template(template)
        return base_template.render_unicode(title=TITLE, **kwargs)
