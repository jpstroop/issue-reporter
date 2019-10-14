from json import load
from github_reporter.html_report_renderer import HTMLReportRenderer

def re_render(json_path):
    renderer = HTMLReportRenderer()
    with open(json_path, 'r') as f:
        report = load(f)
    template = 'issue_report_page.html.mako'
    html = renderer.render(template, r=report)
    print(html)

if __name__ == '__main__':
    json_path = '/Users/jstroop/workspace/github_reporter/docs/reports/2019/10/09.json'
    re_render(json_path)
