function eo(i){
  return (i % 2 == 0 ? "even" : "odd");
};

// :-(
function styleEntry(entry, i) {
  return "<li class=\"" + eo(i) + "\">" +
    "<a href=\"" + entry.html + "\">" + entry.date + "</a>" +
    " <span class=\"issue-count\">(" + entry.issue_count + " issues created/updated/closed)</span>"
  "</li>"
};

function listReports() {
  $.getJSON( "index.json", function(data) {
      $.each( data, function(index, entry) {
          $(styleEntry(entry, index)).appendTo("#entries");
      });
  });
};
