from github_reporter.html_report_renderer import HTMLReportRenderer
from json import load
from os import sep, walk
from os.path import abspath, dirname, join

# A helper script for regenerating the HTML from our JSON reports when
# the template has changed.

def html_path_from_json_path(json_path):
    return json_path.replace('.json', f'{sep}index.html')

def re_render(render, json_path):
    with open(json_path, 'r') as f:
        report = load(f)
    html_path = html_path_from_json_path(json_path)
    template = 'issue_report_page.html.mako'
    with open(html_path, 'w') as f:
        print(renderer.render(template, r=report), file=f)
    return 0

def accumulate_json(root_path):
    def filt(tup):
        return all([i.endswith('.json') for i in tup[2]]) and len(tup[2]) > 0
    dir_files = [(dp, fn) for dp, _, fn in filter(filt, walk(root_path))]
    return [join(dir, file) for dir, files in dir_files for file in files]

if __name__ == '__main__':
    docs_dir = join(abspath(dirname(__file__)), 'docs', 'reports')
    renderer = HTMLReportRenderer()
    [re_render(renderer, jp) for jp in accumulate_json(docs_dir)]
