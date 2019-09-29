<%
    exclude = ('yesterday', 'today')
    repos = [(n,i) for n,i in r.items() if n not in exclude]
%>
% for name, issues in repos:
    <section class="repo" id="${name}">
      <h2><a href="${issues[0]['repository_html_url']}">${name}</a></h2>
      <div class="issues" id="${name}_issues">
        <%include file="issues.html.mako" args="issues=issues"/>
      </div>
    </section>
% endfor
