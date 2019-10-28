from datetime import date, timedelta
from github_reporter.html_report_renderer import HTMLReportRenderer
from json import load
from os import sep, walk
from os.path import abspath, dirname, join

# A helper script for regenerating the HTML from our JSON reports when
# the template has changed.


def html_file_path_from_json_path(json_path):
    return json_path.replace(".json", f"{sep}index.html")


def html_dir_path_from_json_path(json_path):
    return json_path.replace(".json", "")


def html_from_json(renderer, json_path):
    with open(json_path, "r") as f:
        report = load(f)
    html_path = html_file_path_from_json_path(json_path)
    template = "issue_report_page.html.mako"
    with open(html_path, "w") as f:
        print(renderer.render(template, r=report), file=f)
    return 0


def accumulate_json(root_path):
    def filt(tup):
        return all([i.endswith(".json") for i in tup[2]]) and len(tup[2]) > 0

    dir_files = [(dp, fn) for dp, _, fn in filter(filt, walk(root_path))]
    return [join(dir, file) for dir, files in dir_files for file in files]


def date_from_json_path(json_path):
    y, m, d = map(int, json_path.split(".")[0].split(sep)[-3:])
    return date(y, m, d)


def docs_dir():
    return join(abspath(dirname(__file__)), "docs", "reports")


def json_is_older_than_n_days(json_path, n):
    today = date.today()
    file_date = date_from_json_path(json_path)
    return (today - file_date).days > n


# "public" functions you might want to call in __main__
def rerender_html():
    renderer = HTMLReportRenderer()
    [html_from_json(renderer, jp) for jp in accumulate_json(docs_dir())]


# TODO: pick this up when we have more data and actually want it
# TODO: don't forget to update index.json
# TODO: don't forget empty month and year dirs-
#   Maybe just run something like this:
#   https://www.jacobtomlinson.co.uk/posts/2014/
#     python-script-recursively-remove-empty-folders/directories/
def remove_old_reports(days):
    json_paths = accumulate_json(docs_dir())
    to_rm = []
    for jp in json_paths:
        if json_is_older_than_n_days(jp, days):
            html_path = html_file_path_from_json_path(jp)
            html_dir = html_dir_path_from_json_path(jp)
            to_rm.append((jp, html_path, html_dir))
    print(to_rm)


# TODO: sigh...JSONReport class:
#                 .date, .html, .html_dir, .rerender_html(), .older_than(days)
#                 .remove()

if __name__ == "__main__":
    rerender_html()
