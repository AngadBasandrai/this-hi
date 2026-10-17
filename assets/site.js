(function () {
  var REPO = "AngadBasandrai/this-hi";

  // The cat says hi when you touch the portrait.
  var portrait = document.querySelector(".portrait");
  if (portrait) {
    portrait.addEventListener("click", function () {
      portrait.classList.remove("said");
      void portrait.offsetWidth;
      portrait.classList.add("said");
      clearTimeout(portrait._t);
      portrait._t = setTimeout(function () { portrait.classList.remove("said"); }, 1600);
    });
  }

  // Reported sightings: grows steadily from launch day.
  var counter = document.getElementById("sightings");
  if (counter) {
    var launch = Date.UTC(2026, 9, 17);
    var hours = Math.max(0, (Date.now() - launch) / 36e5);
    counter.textContent = (2000 + Math.floor(hours * 3.7)).toLocaleString("en-US");
  }

  // Leave a tab and it greets you from the title bar.
  var title = document.title;
  document.addEventListener("visibilitychange", function () {
    document.title = document.hidden ? "Hi." : title;
  });

  // Live entries from GitHub issues whose title starts with a given prefix.
  document.querySelectorAll("[data-issues]").forEach(function (box) {
    var prefix = box.getAttribute("data-issues").toLowerCase();
    var status = box.querySelector(".live-status");
    fetch("https://api.github.com/repos/" + REPO + "/issues?state=open&per_page=100")
      .then(function (r) { if (!r.ok) throw r; return r.json(); })
      .then(function (issues) {
        var items = issues.filter(function (i) {
          return !i.pull_request && i.title.toLowerCase().indexOf(prefix) === 0;
        });
        if (!items.length) { status.textContent = "No new entries yet. Be the first."; return; }
        status.remove();
        items.forEach(function (i) {
          var card = document.createElement("div");
          card.className = "report";
          var p = document.createElement("p");
          var heading = i.title.slice(prefix.length).replace(/^[\s:\-]+/, "");
          var body = (i.body || "").trim();
          p.textContent = body ? (heading ? heading + "\n\n" : "") + body : heading;
          var cite = document.createElement("cite");
          cite.textContent = "\u2014 @" + i.user.login + ", " +
            new Date(i.created_at).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
          card.appendChild(p);
          card.appendChild(cite);
          box.appendChild(card);
        });
      })
      .catch(function () { status.textContent = "Couldn\u2019t reach the archive right now. Try again later."; });
  });
})();
