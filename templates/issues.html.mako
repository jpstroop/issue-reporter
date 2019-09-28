<%page args="issues"/>
% for i in issues:
      <div class="issue ${loop.cycle('even', 'odd')}">
        <h3><a href="${i['html_url']}">#${i['number']}</a> ${i['title']}</h3>
        <dl>
          <dt>Creator:</dt>
          <dd>${i['user_name']}</dd>
          <dt>Created:</dt>
          <dd>${i['created_at'].split('T')[0]}</dd>
          <dt>State:</dt>
          <dd>${i['state']}</dd>
      % if i['comments']:
          <dt>Comments:</dt>
          <%include file="comments.html.mako" args="comments=i['comments']"/>
      % endif
      % if i['events']:
          <dt>Events:</dt>
          <%include file="events.html.mako" args="events=i['events']"/>
      % endif
        <dl>
      </div>
% endfor
