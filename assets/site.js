/* KeyDrive — shared site script. Global search (reads assets/concepts-index.json, the single
   JSON "content pointer" file every concept and sub-section is registered in) + anchor deep-link
   scroll/highlight, so a search hit — or any shared link — can point at one exact box on a page,
   not just the page itself. */

(function () {
  var root = document.body.getAttribute("data-root") || "";
  var input = document.querySelector(".kdsearch input");
  var resultsBox = document.querySelector(".kdsearch-results");
  var wrap = document.querySelector(".kdsearch");
  if (!input || !resultsBox || !wrap) return;

  var INDEX = [];
  var activeIndex = -1;
  var currentItems = [];

  fetch(root + "assets/concepts-index.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { INDEX = data; })
    .catch(function () { INDEX = []; });

  function scoreItem(item, q) {
    var title = item.title.toLowerCase();
    var kw = (item.keywords || "").toLowerCase();
    if (title.indexOf(q) === 0) return 5;
    if (title.indexOf(q) > -1) return 4;
    if (kw.split(" ").some(function (w) { return w.indexOf(q) === 0; })) return 2;
    if (kw.indexOf(q) > -1) return 1;
    return 0;
  }

  function highlight(title, q) {
    var i = title.toLowerCase().indexOf(q);
    if (i === -1) return title;
    return title.slice(0, i) + "<mark>" + title.slice(i, i + q.length) + "</mark>" + title.slice(i + q.length);
  }

  function render(items, q) {
    resultsBox.innerHTML = "";
    activeIndex = -1;
    currentItems = items;
    if (!q) return;
    if (items.length === 0) {
      var empty = document.createElement("div");
      empty.className = "kd-empty";
      empty.textContent = "No concept found for “" + q + "” yet.";
      resultsBox.appendChild(empty);
      return;
    }
    items.forEach(function (item) {
      var row = document.createElement("div");
      row.className = "kd-item";
      row.setAttribute("role", "option");
      row.innerHTML =
        '<span class="ki-icon">' + (item.anchor ? "🔖" : "🧩") + "</span>" +
        '<span class="ki-text">' +
          '<span class="ki-title">' + highlight(item.title, q) + "</span>" +
          '<span class="ki-path">' + (item.category || "KeyDrive") + "</span>" +
        "</span>";
      row.addEventListener("mousedown", function (e) { e.preventDefault(); goTo(item); });
      resultsBox.appendChild(row);
    });
  }

  function goTo(item) {
    window.location.href = root + item.page + (item.anchor ? "#" + item.anchor : "");
  }

  function setActive(i) {
    var rows = resultsBox.querySelectorAll(".kd-item");
    rows.forEach(function (r) { r.classList.remove("active"); });
    if (rows[i]) { rows[i].classList.add("active"); rows[i].scrollIntoView({ block: "nearest" }); }
    activeIndex = i;
  }

  input.addEventListener("input", function () {
    var q = input.value.trim().toLowerCase();
    if (!q) { render([], ""); return; }
    var scored = INDEX
      .map(function (item) { return { item: item, score: scoreItem(item, q) }; })
      .filter(function (s) { return s.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 8)
      .map(function (s) { return s.item; });
    render(scored, q);
  });

  input.addEventListener("keydown", function (e) {
    var rows = resultsBox.querySelectorAll(".kd-item");
    if (e.key === "ArrowDown") { e.preventDefault(); if (rows.length) setActive((activeIndex + 1) % rows.length); }
    else if (e.key === "ArrowUp") { e.preventDefault(); if (rows.length) setActive((activeIndex - 1 + rows.length) % rows.length); }
    else if (e.key === "Enter") {
      if (activeIndex > -1 && currentItems[activeIndex]) goTo(currentItems[activeIndex]);
      else if (currentItems[0]) goTo(currentItems[0]);
    } else if (e.key === "Escape") { render([], ""); input.blur(); }
  });

  input.addEventListener("focus", function () { wrap.classList.add("has-focus"); });
  input.addEventListener("blur", function () {
    wrap.classList.remove("has-focus");
    setTimeout(function () { resultsBox.innerHTML = ""; }, 150);
  });
})();

/* Anchor deep-link: scroll to and briefly glow the exact section a link/search-hit pointed at
   (e.g. concepts/rag.html#recall) — a plain #id jump is instant and easy to miss on a long page. */
(function () {
  if (!location.hash) return;
  var target = document.getElementById(location.hash.slice(1));
  if (!target) return;
  setTimeout(function () {
    target.scrollIntoView({ behavior: "smooth", block: "center" });
    target.classList.add("kd-pointed");
    setTimeout(function () { target.classList.remove("kd-pointed"); }, 2600);
  }, 60);
})();
