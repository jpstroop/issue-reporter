function eo(i) {
  return (i % 2 == 0 ? "even" : "odd");
};

// :-(
function styleLegacyEntry1(entry, i) {
  return "<li class=\"" + eo(i) + "\">" +
    "<a href=\"" + entry.html + "\">" + entry.date + "</a>" +
    " <span class=\"issue-count\">(" + entry.issue_count + " issues created/updated/closed)</span>"
  "</li>"
};

function styleLegacyEntry2(entry, i) {
  return "<li class=\"" + eo(i) + "\">" +
    "<a href=\"" + entry.html + "\">" + entry.date + "</a>" +
    " <span class=\"issue-count\">(" +
    entry.meta.issue_count + " issues: " +
    entry.meta.created_count + " created, " +
    entry.meta.updated_count + " updated, " +
    entry.meta.closed_count + " closed, " +
    entry.meta.pull_request_count + " pull requests)</span>" +
    "</li>"
};

function styleEntry(entry, i) {
  return "<li class=\"" + eo(i) + "\">" +
    "<a href=\"" + entry.html + "\">" + entry.date + "</a>" +
    " <span class=\"issue-count\">(" +
    entry.meta.issue_count + " issues: " +
    entry.meta.created_count + " created, " +
    entry.meta.updated_count + " updated, " +
    entry.meta.closed_count + " closed, " +
    entry.meta.pull_request_open_count + " pull requests; open, " +
    entry.meta.pull_request_closed_count + " pull requests; closed)</span>" +
    "</li>"
};

function listReports() {
  $.getJSON("index.json", function(data) {
    $.each(data, function(i, entry) {
      if ("meta" in entry) {
        if ("pull_request_count" in entry.meta) {
          $(styleLegacyEntry2(entry, i)).appendTo("#entries");
        } else {
          $(styleEntry(entry, i)).appendTo("#entries");
        }
      } else {
        $(styleLegacyEntry1(entry, i)).appendTo("#entries");
      }
    });
  });
};
