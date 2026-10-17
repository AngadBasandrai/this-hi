(function () {
  var REPO = "AngadBasandrai/this-hi";

  // Contact and guestbook forms post as a prefilled GitHub issue.
  document.querySelectorAll("form[data-issue-prefix]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var name = (data.get("name") || "").trim();
      var lines = [];
      data.forEach(function (value, key) {
        if (key !== "message" && String(value).trim()) lines.push(key.charAt(0).toUpperCase() + key.slice(1) + ": " + String(value).trim());
      });
      var body = (data.get("message") || "").trim() + (lines.length ? "\n\n" + lines.join("\n") : "");
      var url = "https://github.com/" + REPO + "/issues/new?title=" +
        encodeURIComponent(form.getAttribute("data-issue-prefix") + ": " + name) + "&body=" + encodeURIComponent(body);
      window.open(url, "_blank", "noopener");
    });
  });

  // Dreams, sightings, fan art and guestbook entries come from open issues with a matching title prefix.
  var boxes = document.querySelectorAll("[data-issues]");
  if (!boxes.length) return;
  fetch("https://api.github.com/repos/" + REPO + "/issues?state=open&per_page=100")
    .then(function (r) { if (!r.ok) throw r; return r.json(); })
    .then(function (all) {
      boxes.forEach(function (box) {
        var prefix = box.getAttribute("data-issues");
        all.filter(function (i) {
          return !i.pull_request && i.title.toLowerCase().indexOf(prefix.toLowerCase()) === 0;
        }).forEach(function (i) {
          var heading = i.title.slice(prefix.length).replace(/^[\s:\-]+/, "");
          var body = (i.body || "").trim();
          var p = document.createElement("p");
          var em = document.createElement("em");
          em.textContent = "\u201c" + (body || heading) + "\u201d";
          p.appendChild(em);
          box.appendChild(p);
        });
      });
    })
    .catch(function () {});
})();
