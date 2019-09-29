<?xml version="1.0" encoding="utf-8"?>
<%
    exclude = ('yesterday', 'today')
    repos = [(n,i) for n,i in r.items() if n not in exclude]
    ## See: https://iiif.io/news/atom.xml
%>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>${title}</title>
    <link href="http://demo.dotcms.com/home/atom-feed.html" rel="self" />
    <id>https://jpstroop.github.io/issue-reporter/</id>
    <updated>${i['today']}<!-- TODO: TIME ZONE? --></updated>
    % for name, issues in repos:
    ## WAIT...do we want an entry per day (loop over file system) or an entry
    ## per issue, or an entry per repo?
        <entry>
          <title>${title} for ${r['yesterday'].split('T')[0]}</title>
          <link href="http://demo.dotcms.com/news/${con.urlTitle}" />
          <id>https://jpstroop.github.io/issue-reporter/reports/${r['yesterday'].split('T')[0]}.html</id>
          <updated>${i['today']}<!-- TODO: TIME ZONE? --></updated>
          <author><name>$con.byline</name></author>
          <summary></summary>
          <content type="xhtml">
            <div xmlns="http://www.w3.org/1999/xhtml">
              <p>This is the entry content.</p>
            </div>
          </content>
        </entry>
    % endfor
</feed>
