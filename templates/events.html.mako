<%page args="events"/>
% for e in events:
          <li class="event ${loop.cycle('even', 'odd')}"><code>${e['type']}</code> by ${e['actor_name']} at ${e['created_at']}.</li>
% endfor
