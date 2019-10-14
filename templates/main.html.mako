<%
    exclude = ('yesterday', 'today')
    repos = [(n,i) for n,i in r.items() if n not in exclude]
%>
% for name, issues in repos:
    <section class="repo" id="${name}">
      <h2><a href="${issues[0]['repository_html_url']}">pulibrary/${name}</a> <i class="fas fa-external-link-alt fa-xs"></i></h2>
      <div class="issues">
        <%include file="issues.html.mako" args="issues=issues,name=name"/>
      </div>
    </section>
% endfor
