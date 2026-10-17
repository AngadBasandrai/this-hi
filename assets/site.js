(function () {
  var REPO = "AngadBasandrai/this-hi";
  var issues = null;

  // Open issues on the repo are the site's only data source (dreams, sightings, fan art, guestbook).
  function loadIssues() {
    if (!issues) {
      issues = fetch("https://api.github.com/repos/" + REPO + "/issues?state=open&per_page=100")
        .then(function (r) { if (!r.ok) throw r; return r.json(); })
        .then(function (all) { return all.filter(function (i) { return !i.pull_request; }); });
    }
    return issues;
  }

  function withPrefix(all, prefix) {
    prefix = prefix.toLowerCase();
    return all.filter(function (i) { return i.title.toLowerCase().indexOf(prefix) === 0; });
  }

  var count = document.getElementById("dream-count");
  if (count) {
    loadIssues()
      .then(function (all) { count.textContent = withPrefix(all, "Dream").length; })
      .catch(function () { count.textContent = "unavailable right now"; });
  }

  document.querySelectorAll("[data-issues]").forEach(function (box) {
    var prefix = box.getAttribute("data-issues");
    var status = box.querySelector(".live-status");
    loadIssues()
      .then(function (all) {
        var items = withPrefix(all, prefix);
        if (!items.length) { status.textContent = "Nothing submitted yet."; return; }
        status.remove();
        items.forEach(function (i) {
          var entry = document.createElement("div");
          entry.className = "entry";
          var p = document.createElement("p");
          var heading = i.title.slice(prefix.length).replace(/^[\s:\-]+/, "");
          var body = (i.body || "").trim();
          p.textContent = "\u201c" + (body ? (heading ? heading + "\n\n" : "") + body : heading) + "\u201d";
          var cite = document.createElement("cite");
          var link = document.createElement("a");
          link.href = i.html_url;
          link.textContent = "@" + i.user.login + ", " +
            new Date(i.created_at).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
          cite.appendChild(document.createTextNode("\u2014 "));
          cite.appendChild(link);
          entry.appendChild(p);
          entry.appendChild(cite);
          box.appendChild(entry);
        });
      })
      .catch(function () { status.textContent = "Couldn\u2019t load entries right now. Try again later."; });
  });
})();
