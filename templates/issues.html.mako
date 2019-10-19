<%page args="issues,name"/>
% for i in issues:
      <div class="issue ${loop.cycle('even', 'odd')}" id="${name}-${i['number']}">
        <h3><a href="${i['html_url']}">#${i['number']}</a> ${i['title']}</h3>
        <dl>
          <dt>Creator:</dt>
          <dd>${i['user_name']}</dd>
          <dt>Created:</dt>
          <dd>${i['created_at']}</dd>
          <dt>Status:</dt>
          <dd>${str.capitalize(i['state']) }
      % if i['pr_html_url']:
          (<a href="${i['pr_html_url']}">pull request</a>)
      % endif
          </dd>
      % if i['comments']:
          <dt>Comments:</dt>
          <%include file="comments.html.mako" args="comments=i['comments']"/>
      % endif
      % if i['events']:
          <dt>Events:</dt>
          <dd>
            <ul class="events">
            <%include file="events.html.mako" args="events=i['events']"/>
            </ul>
          </dd>
      % endif
        </dl>
      </div>
% endfor
