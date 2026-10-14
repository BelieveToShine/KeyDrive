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

/* One-level "Back" button in the crumb bar — see docs/rules/navigation.md. A plain left-click on
   any internal link tags its href with where it came from (bfrom = this page's clean URL +
   scroll position, bt = label); the destination reads the tag once, shows ← Back, then strips it
   from the URL. So Back is exactly one hop, a page reached BY Back never shows its own Back, and
   a fresh visit / reload / search-box jump never shows one. Returning restores scroll position. */
(function () {
  var P = ["bfrom", "bt", "bs"];

  function cleanUrl(url) {
    var hi = url.indexOf("#");
    var hash = hi > -1 ? url.slice(hi) : "";
    var rest = hi > -1 ? url.slice(0, hi) : url;
    var qi = rest.indexOf("?");
    var base = qi > -1 ? rest.slice(0, qi) : rest;
    var params = new URLSearchParams(qi > -1 ? rest.slice(qi + 1) : "");
    P.forEach(function (k) { params.delete(k); });
    var qs = params.toString();
    return base + (qs ? "?" + qs : "") + hash;
  }

  // add a query param BEFORE any #hash (a param after the hash never reaches the page)
  function addParam(url, key, val) {
    var hi = url.indexOf("#");
    var base = hi > -1 ? url.slice(0, hi) : url;
    var hash = hi > -1 ? url.slice(hi) : "";
    return base + (base.indexOf("?") > -1 ? "&" : "?") + key + "=" + encodeURIComponent(val) + hash;
  }

  var incoming = new URLSearchParams(location.search);
  var backHref = incoming.get("bfrom");
  var backLabel = incoming.get("bt");
  var scrollTo = parseInt(incoming.get("bs"), 10);
  var crumbs = document.querySelector("nav.kd-crumbs");

  if (crumbs && backHref) {
    var btn = document.createElement("a");
    btn.className = "crumb-back";
    btn.href = backHref;
    var label = backLabel ? "Back to " + backLabel : "Back";
    btn.setAttribute("aria-label", label);
    btn.title = label;
    btn.innerHTML = '<span class="cb-arrow">←</span><span class="cb-text">Back</span>';
    crumbs.appendChild(btn);
  }

  // this page is a Back target: put the reader exactly where they left it
  if (!isNaN(scrollTo) && scrollTo > 0) {
    setTimeout(function () { window.scrollTo(0, scrollTo); }, 120);
  }

  if (backHref !== null || incoming.has("bs")) {
    history.replaceState(null, "", cleanUrl(location.pathname + location.search + location.hash));
  }

  document.addEventListener("click", function (e) {
    if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a");
    if (!a || a.classList.contains("crumb-back") || a.closest(".kdsearch-results")) return;
    // SVG anchors (journey-map nodes) use xlink:href; HTML anchors use href
    var XL = "http://www.w3.org/1999/xlink";
    var attr = a.hasAttribute("href") ? "href" : (a.hasAttributeNS(XL, "href") ? "xlink:href" : null);
    if (!attr) return;
    var href = a.getAttribute(attr);
    if (!href || href.charAt(0) === "#" || /^[a-z][a-z0-9+.-]*:/i.test(href) || a.target === "_blank") return;

    var from = cleanUrl(location.pathname + location.search + location.hash);
    var y = Math.round(window.scrollY || 0);
    if (y > 0) from = addParam(from, "bs", y);
    var label = (document.title || "").split(" — ")[0].trim();
    var tagged = addParam(addParam(href, "bfrom", from), "bt", label);
    a.setAttribute(attr, tagged);
    setTimeout(function () { a.setAttribute(attr, href); }, 0);
  }, true);
})();

/* Fixed bottom journey bar — Prev / ↑ category hub / Next on every concept page, built from
   assets/journeys.json (ordered concept list per category) + concepts-index.json (titles).
   Zero per-page markup. See docs/rules/navigation.md.
   - journeys.json "written" (optional): slugs that exist. A neighbour that isn't written yet is
     shown as a locked "coming soon" cell instead of a dead link. Omit it when all are written.
   - journeys.json "sub": { subSlug: parentSlug } — deep-dive pages hanging off a concept. They are
     not part of "order"; their bar goes parent → sub 1 → sub 2 → … → parent's next concept. */
(function () {
  var m = location.pathname.match(/\/([^\/]+)\/concepts\/([^\/]+)\.html$/);
  if (!m) return;
  var cat = m[1], slug = m[2];
  var root = document.body.getAttribute("data-root") || "";

  Promise.all([
    fetch(root + "assets/journeys.json").then(function (r) { return r.json(); }),
    fetch(root + "assets/concepts-index.json").then(function (r) { return r.json(); })
  ]).then(function (res) {
    var journey = res[0][cat];
    if (!journey) return;
    var sub = journey.sub || {};
    var written = journey.written || journey.order;
    var titles = {};
    res[1].forEach(function (it) { if (!it.anchor && it.page.indexOf(cat + "/") === 0) titles[it.id] = it.title; });
    Object.keys(journey.titles || {}).forEach(function (k) { titles[k] = journey.titles[k]; });
    Object.keys(journey.subTitles || {}).forEach(function (k) { titles[k] = journey.subTitles[k]; });

    function target(s, tag) {
      if (!s) return null;
      return { title: titles[s] || s, href: s + ".html", locked: written.indexOf(s) < 0 && !sub[s], tag: tag };
    }

    var total = journey.order.length, prev, next, i;
    if (sub[slug]) {
      var parent = sub[slug];
      var sibs = Object.keys(sub).filter(function (k) { return sub[k] === parent; });
      var si = sibs.indexOf(slug);
      i = journey.order.indexOf(parent);
      prev = target(si > 0 ? sibs[si - 1] : parent, si > 0 ? "Previous deep dive" : "Main concept");
      next = si < sibs.length - 1
        ? target(sibs[si + 1], "Next deep dive")
        : target(journey.order[i + 1], i + 1 < total ? "Next concept · " + (i + 2) + " of " + total : "");
    } else {
      i = journey.order.indexOf(slug);
      if (i < 0) return;
      prev = target(journey.order[i - 1], "Previous · " + i + " of " + total);
      next = target(journey.order[i + 1], "Next · " + (i + 2) + " of " + total);
    }
    if (!next) next = { title: "Back to " + journey.title + " hub", href: "../index.html", tag: "Finished" };

    function side(t, cls, arrowFirst) {
      if (!t) return '<span class="fp-side ' + cls + ' fp-empty"></span>';
      var arrow = '<span class="fp-arrow">' + (t.locked ? "🔒" : (arrowFirst ? "←" : "→")) + "</span>";
      var text = '<span class="fp-text"><span class="fp-tag">' + (t.locked ? "Coming soon" : t.tag) + '</span><span class="fp-title">' +
        t.title + "</span></span>";
      var inner = arrowFirst ? arrow + text : text + arrow;
      return t.locked
        ? '<span class="fp-side fp-locked ' + cls + '" aria-disabled="true">' + inner + "</span>"
        : '<a class="fp-side ' + cls + '" href="' + t.href + '">' + inner + "</a>";
    }

    var bar = document.createElement("nav");
    bar.className = "fixed-pager";
    bar.setAttribute("aria-label", "Journey navigation");
    bar.innerHTML = side(prev, "fp-prev", true) +
      '<a class="fp-mid" href="../index.html">↑ ' + journey.title + " hub</a>" + side(next, "fp-next", false);
    document.body.appendChild(bar);
    document.body.classList.add("has-fixed-pager");
  }).catch(function () {});
})();

/* Phone view of the hub journey map: the SVG is a 640px-wide picture, so on narrow screens we also
   build a vertical stepper from the same SVG (nodes, "why the next step" pills, group boxes). */
(function () {
  var wrap = document.querySelector(".journey-wrap");
  var svg = wrap && wrap.querySelector("svg");
  if (!svg) return;
  var num = function (el, a) { return parseFloat(el.getAttribute(a)) || 0; };
  var groups = [].slice.call(svg.querySelectorAll("rect[stroke-dasharray]")).map(function (r) {
    var t = r.nextElementSibling;
    return { y: num(r, "y"), h: num(r, "height"), label: t ? t.textContent.trim() : "" };
  });
  var pills = [].slice.call(svg.querySelectorAll(".arrow-pill")).map(function (g) {
    return { y: num(g.querySelector("rect"), "y"), text: g.querySelector("text").textContent.trim() };
  });
  var rows = {};
  [].slice.call(svg.querySelectorAll(".jm-node")).forEach(function (n) {
    var y = num(n.querySelector("rect"), "y"), a = n.parentNode;
    (rows[y] = rows[y] || []).push({
      text: n.querySelector("text").textContent.trim(),
      href: a.tagName.toLowerCase() === "a" ? (a.getAttribute("href") || a.getAttribute("xlink:href")) : null
    });
  });
  var ys = Object.keys(rows).map(Number).sort(function (a, b) { return a - b; });
  var out = '<ol class="jm-steps" aria-label="Journey steps in order">', prevY = -1, lastGroup = null;
  ys.forEach(function (y, i) {
    var why = pills.filter(function (p) { return p.y < y && p.y > prevY; }).pop();
    if (i && why) out += '<li class="jm-why">↓ ' + why.text + "</li>";
    var g = groups.filter(function (g) { return y >= g.y && y <= g.y + g.h; })[0];
    if (g && g !== lastGroup) out += '<li class="jm-group">' + g.label + "</li>";
    lastGroup = g || null;
    out += '<li class="jm-row' + (g ? " in-group" : "") + '">' + rows[y].map(function (n) {
      return n.href ? '<a class="jm-step" href="' + n.href + '">' + n.text + "</a>"
                    : '<span class="jm-step locked">' + n.text + " · soon</span>";
    }).join("") + "</li>";
    prevY = y;
  });
  var box = document.createElement("div");
  box.className = "jm-steps-wrap";
  box.innerHTML = out + "</ol>";
  wrap.insertBefore(box, svg.nextSibling);
})();

/* ---------- Animated explanations (docs/rules/diagram-style.md "Diagram animation") ----------
   1. Story figures  (figure.kd-story): step-by-step animated diagrams with captions + play/pause/step.
      Elements carry data-s="a-b" (visible from step a to b), data-hl="n" (highlighted at step n);
      .tok groups travel along the <path id=data-path> when their step starts.
   2. Flow pulses: every other svg.concept-diagram gets a small dot travelling along each arrow
      (direction of the relationship). Both are off for prefers-reduced-motion and pause off-screen. */
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NS = "http://www.w3.org/2000/svg";
  function range(el, n) {
    var m = /^(\d*)-(\d*)$/.exec(el.getAttribute("data-s") || "-");
    return [m && m[1] ? +m[1] : 1, m && m[2] ? +m[2] : n + 999];
  }
  var registry = [];

  function Story(fig) {
    var self = this;
    this.fig = fig; this.svg = fig.querySelector("svg"); this.n = +fig.getAttribute("data-steps");
    this.k = 0; this.timer = null; this.playing = false; this.visible = false; this.raf = [];
    this.caps = [].map.call(fig.querySelectorAll(".st-caps li"), function (li) { return li.innerHTML; });
    this.els = [].map.call(this.svg.querySelectorAll(".st"), function (g) {
      var r = range(g, self.n), hl = (g.getAttribute("data-hl") || "").split(",").filter(Boolean).map(Number);
      return { g: g, lo: r[0], hi: r[1], hl: hl, tok: g.querySelector(".tok") };
    });
    this.bar = fig.querySelector(".st-bar"); this.cap = fig.querySelector(".st-cap");
    this.playBtn = fig.querySelector(".st-play"); this.dots = fig.querySelector(".st-dots");
    fig.classList.add("st-live"); this.bar.hidden = false; this.cap.hidden = false;
    for (var i = 1; i <= this.n; i++) {
      var d = document.createElement("button"); d.type = "button"; d.className = "st-dot"; d.setAttribute("aria-label", "Step " + i);
      d.addEventListener("click", (function (j) { return function () { self.pause(); self.set(j); }; })(i));
      this.dots.appendChild(d);
    }
    fig.querySelector('[data-act="prev"]').addEventListener("click", function () { self.pause(); self.set(self.k > 1 ? self.k - 1 : self.n); });
    fig.querySelector('[data-act="next"]').addEventListener("click", function () { self.pause(); self.set(self.k < self.n ? self.k + 1 : 1); });
    this.playBtn.addEventListener("click", function () { self.playing ? self.pause() : self.play(true); });
    this.set(reduce ? this.n : 1, true);
    registry.push(this);
  }
  Story.prototype.set = function (k, instant) {
    var self = this; this.k = k;
    this.raf.forEach(cancelAnimationFrame); this.raf = [];
    this.els.forEach(function (e) {
      e.g.classList.toggle("st-off", !(k >= e.lo && k <= e.hi));
      e.g.classList.toggle("st-hl", e.hl.indexOf(k) > -1);
      if (e.tok) self.place(e, k, instant);
    });
    this.cap.innerHTML = '<span class="st-n">' + k + "/" + this.n + "</span> " + (this.caps[k - 1] || "");
    [].forEach.call(this.dots.children, function (d, i) { d.classList.toggle("on", i + 1 === k); d.classList.toggle("done", i + 1 < k); });
  };
  Story.prototype.place = function (e, k, instant) {
    var path = this.svg.getElementById ? this.svg.getElementById(e.tok.getAttribute("data-path")) : null;
    if (!path) return;
    var L = path.getTotalLength(), self = this;
    function at(t) { var p = path.getPointAtLength(L * t); e.tok.setAttribute("transform", "translate(" + p.x + "," + p.y + ")"); }
    if (k > e.lo || instant || reduce) { at(k >= e.lo ? 1 : 0); return; }
    at(0);
    if (k < e.lo) return;
    var t0 = null, dur = Math.max(900, Math.min(1800, L * 5));
    var step = function (ts) {
      if (t0 === null) t0 = ts + 350;                       // short pause before it sets off
      var t = Math.max(0, Math.min(1, (ts - t0) / dur)), ease = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      at(ease);
      if (t < 1) self.raf.push(requestAnimationFrame(step));
    };
    this.raf.push(requestAnimationFrame(step));
  };
  Story.prototype.play = function (restart) {
    this.playing = true; this.playBtn.textContent = "⏸"; this.fig.classList.add("st-playing");
    if (restart && this.k >= this.n) this.set(1);
    this.schedule();
  };
  Story.prototype.pause = function () { this.playing = false; this.playBtn.textContent = "▶"; this.fig.classList.remove("st-playing"); clearTimeout(this.timer); };
  Story.prototype.schedule = function () {
    var self = this; clearTimeout(this.timer);
    if (!this.playing || !this.visible) return;
    var dwell = this.k >= this.n ? 4200 : 3400;
    this.timer = setTimeout(function () { self.set(self.k >= self.n ? 1 : self.k + 1); self.schedule(); }, dwell);
  };

  function initStories() {
    var figs = [].slice.call(document.querySelectorAll("figure.kd-story"));
    if (!figs.length) return;
    var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var s = en.target.__story; if (!s) return;
        s.visible = en.isIntersecting;
        if (en.isIntersecting && !s.started && !reduce) { s.started = true; s.play(); }
        else if (s.playing) s.schedule(); else clearTimeout(s.timer);
        if (!en.isIntersecting) clearTimeout(s.timer);
      });
    }, { threshold: 0.45 }) : null;
    figs.forEach(function (f) {
      var s = new Story(f); f.__story = s;
      if (io) io.observe(f); else if (!reduce) { s.visible = true; s.play(); }
      if (reduce) s.pause();
    });
  }
  window.kdStory = { set: function (fig, k, instant) { var s = fig.__story; if (s) { s.pause(); s.set(k, instant !== false); } }, all: registry };

  /* flow pulses on ordinary diagrams */
  function initPulses() {
    if (reduce || !document.createElementNS) return;
    var svgs = [].slice.call(document.querySelectorAll("svg.concept-diagram")).filter(function (s) { return !s.closest(".kd-story") && !s.closest(".journey-wrap"); });
    svgs.forEach(function (svg) {
      var paths = [].slice.call(svg.querySelectorAll("path[marker-end]")).filter(function (p) { return !p.classList.contains("flow-arrow") && p.getTotalLength() > 40; });
      paths.forEach(function (p, i) {
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("r", "3.2"); c.setAttribute("fill", p.getAttribute("stroke") || "#22d3ee"); c.setAttribute("class", "pulse"); c.setAttribute("aria-hidden", "true");
        var len = p.getTotalLength(), dur = Math.max(1.6, len / 70) + 1.6;
        var m = document.createElementNS(NS, "animateMotion");
        m.setAttribute("dur", dur + "s"); m.setAttribute("repeatCount", "indefinite"); m.setAttribute("begin", (i * 0.45) + "s");
        m.setAttribute("keyPoints", "0;1;1"); m.setAttribute("keyTimes", "0;" + (1 - 1.6 / dur).toFixed(3) + ";1"); m.setAttribute("calcMode", "linear");
        var mp = document.createElementNS(NS, "mpath"); mp.setAttributeNS("http://www.w3.org/1999/xlink", "href", "#" + (p.id || (p.id = "pp" + Math.random().toString(36).slice(2, 8))));
        m.appendChild(mp);
        var o = document.createElementNS(NS, "animate");
        o.setAttribute("attributeName", "opacity"); o.setAttribute("dur", dur + "s"); o.setAttribute("repeatCount", "indefinite"); o.setAttribute("begin", (i * 0.45) + "s");
        o.setAttribute("values", "0;.95;.95;0;0"); o.setAttribute("keyTimes", "0;.06;" + (1 - 1.8 / dur).toFixed(3) + ";" + (1 - 1.6 / dur).toFixed(3) + ";1");
        c.appendChild(m); c.appendChild(o); svg.appendChild(c);
      });
    });
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { try { en.isIntersecting ? en.target.unpauseAnimations() : en.target.pauseAnimations(); } catch (e) {} });
      }, { threshold: 0.1 });
      svgs.forEach(function (s) { io.observe(s); });
    }
  }
  function boot() { initStories(); initPulses(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();


/* Journey-map node labels: shrink the font until the label fits inside its box with a clear margin, so long titles never
   spill over the border or collide with the emoji / neighbouring pills. Re-runs a few times because emoji fonts and web
   fonts can finish loading late (and differ per OS). Runs on every hub page that has an SVG journey map. */
(function () {
  function fit() {
    document.querySelectorAll(".jm-node").forEach(function (g) {
      var r = g.querySelector("rect"), t = g.querySelector("text");
      if (!r || !t || !t.getBBox) return;
      var max = parseFloat(r.getAttribute("width")) - 44, fs = 14;
      t.setAttribute("font-size", fs);
      var guard = 0;
      while (t.getBBox().width > max && fs > 8 && guard++ < 40) { fs -= 0.5; t.setAttribute("font-size", fs); }
    });
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener("load", fit);
  [300, 900, 2000].forEach(function (ms) { setTimeout(fit, ms); });
})();


/* Keep the breadcrumb bar (with the ← Back pill) pinned directly under the top bar while scrolling. */
(function () {
  function sync() {
    var tb = document.querySelector(".topbar");
    if (!tb) return;
    var h = window.innerWidth <= 700 ? 0 : tb.getBoundingClientRect().height;
    document.documentElement.style.setProperty("--topbar-h", h + "px");
    var c = document.querySelector("nav.kd-crumbs");
    document.documentElement.style.scrollPaddingTop = (h + (c ? c.getBoundingClientRect().height : 0) + 12) + "px";
  }
  sync();
  window.addEventListener("resize", sync);
  window.addEventListener("load", sync);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
})();
