<%! import misaka %>
<%page args="comments"/>
          <dd class="comments">
            <dl>
      % for c in comments:
              <dt>${c['user_name']} at <a href="${c['html_url']}">${c['updated_at']}</a>:</dt>
              <dd class="${loop.cycle('even', 'odd')} ${'last' if loop.last else 'not_last'}">
                ${ misaka.html(c['body'], extensions=('autolink','fenced-code')) }
                ## See https://misaka.61924.nl/#extensions for extensions
              </dd>
      % endfor
            </dl>
          </dd>
