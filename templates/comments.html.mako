<%! import misaka %>
<%page args="comments"/>
          <dd class="comments">
            <dl>
      % for c in comments:
              <dt>${c['user_name']} at <a href="${c['html_url']}">${c['updated_at']}</a> <i class="fas fa-external-link-alt fa-xs"></i> :</dt>
              <dd class="${loop.cycle('even', 'odd')}">
                ${ misaka.html(c['body'], extensions=('autolink','fenced-code','tables')) }
                ## See https://misaka.61924.nl/#extensions for extensions
              </dd>
      % endfor
            </dl>
          </dd>
