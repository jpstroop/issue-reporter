<%page args="events"/>
% for e in events:
          <dd class="event ${loop.cycle('even', 'odd')}">${e['type']} by ${e['actor_name']} at ${e['created_at']}.</dd>
% endfor
