<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${title}</title>
    <link rel = "stylesheet" type="text/css" href="css/main.css" />
  </head>
  <body>
    <header>
      <h1>${title}</h1>
    </header>
    <ol>
    % for i in index_files:
    ## TODO: make pretty; add JSON too?
      <li><a href="${i}">${i}</a></li>
    % endfor
    </ol>
  </body>
</html>
