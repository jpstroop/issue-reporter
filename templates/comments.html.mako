<%! import misaka %>
<%page args="comments"/>
% for c in comments:
          <dd class="comment ${loop.cycle('even', 'odd')}">
            <dl>
              <dt>${c['user_name']} at <a href="${c['html_url']}">${c['updated_at']}</a>:</dt>
              <dd>${ misaka.html(c['body']) }</dd>
            </dl>
          </dd>
% endfor
