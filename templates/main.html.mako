<%
    exclude = ('yesterday', 'today')
    repos = [(n,i) for n,i in r.items() if n not in exclude]
%>
% for name, issues in repos:
    <section class="repo">
      <header>
        <h2><a href="${issues[0]['repository_html_url']}">${name}</a></h2>
      </header>
      <%include file="issues.html.mako" args="issues=issues"/>
    </section>
% endfor
