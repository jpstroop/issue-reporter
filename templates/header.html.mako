<%
    exclude = ('yesterday', 'today')
    repos = [k for k in r.keys() if k not in exclude]
%>
<h1 class="bg-dark text-light">PUL GitHub Issues<br /><small class="text-white-70">${r['today'].split('T')[0]}</small></h1>
<nav class="navbar sticky-top navbar-dark bg-dark">
  <a class="navbar-brand" href="#">Repositories</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar-toggler" aria-controls="navbar-toggler" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbar-toggler">
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item not-mono">
        <a class="nav-link" href="../../../../index.html"><i class="fas fa-arrow-left"></i> Back to Report List Page</a>
      </li>
      % for repo in repos:
      <li class="nav-item">
        <a class="nav-link" href="#${repo}">pulibrary/${repo}</a>
      </li>
      % endfor
      </li>
    </ul>
  </div>
</nav>
