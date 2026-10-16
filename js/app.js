(function () {
  "use strict";

  var app = document.getElementById("app");
  var SITE = window.SITE || {};
  var books = {};      // id -> book data (after load)
  var loading = {};    // id -> Promise

  // ---------- book loading ----------

  // Each book file calls window.registerBook({...})
  window.registerBook = function (book) {
    books[book.id] = book;
  };

  function entry(id) {
    return (window.LIBRARY || []).filter(function (b) { return b.id === id; })[0];
  }

  function loadBook(id) {
    if (books[id]) return Promise.resolve(books[id]);
    if (loading[id]) return loading[id];
    var e = entry(id);
    if (!e || !e.src) return Promise.reject(new Error("not found"));
    loading[id] = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = e.src;
      s.onload = function () {
        if (!books[id]) return reject(new Error("book did not register"));
        books[id].meta = e;
        resolve(books[id]);
      };
      s.onerror = function () { delete loading[id]; reject(new Error("load failed")); };
      document.head.appendChild(s);
    });
    return loading[id];
  }

  // ---------- small helpers ----------

  function esc(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  function donateButton(extraClass) {
    return '<a class="btn btn-donate ' + (extraClass || "") + '" href="' + esc(SITE.donateUrl) +
      '" target="_blank" rel="noopener">' + esc(SITE.donateLabel || "לתרום") + "</a>";
  }

  function setView(name, html) {
    document.body.setAttribute("data-view", name);
    app.innerHTML = html;
    window.scrollTo(0, 0);
  }

  function go(hash, replace) {
    if (replace) location.replace(hash); else location.hash = hash;
  }

  // ---------- views ----------

  function viewLibrary() {
    document.title = SITE.name;
    var list = window.LIBRARY || [];
    Promise.all(list.map(function (e) {
      return e.status === "available" ? loadBook(e.id).catch(function () { return null; }) : null;
    })).then(function (loaded) {
      var cards = list.map(function (e, i) {
        var b = loaded[i];
        if (!b) return "";
        var last = parseInt(store("progress:" + b.id), 10);
        var cont = last > 1 && last <= b.pages.length
          ? '<a class="card-continue" href="#/book/' + b.id + "/" + last + '">להמשיך מעמוד ' + last + "</a>" : "";
        return '<article class="card">' +
          '<a class="card-cover" href="#/book/' + b.id + '" aria-label="' + esc(b.title) + '">' + b.cover + "</a>" +
          '<div class="card-body">' +
            '<p class="card-series">' + esc(b.series) + " · פרק " + b.chapter + "</p>" +
            '<h2 class="card-title"><a href="#/book/' + b.id + '">' + esc(b.title) + "</a></h2>" +
            '<p class="card-blurb">' + esc(b.blurb) + "</p>" + cont +
          "</div></article>";
      }).join("");

      // upcoming chapters announced by the latest book of each series
      var soon = [];
      loaded.forEach(function (b) {
        if (b && b.nextChapters) b.nextChapters.forEach(function (c, i) {
          soon.push({ n: b.chapter + i + 1, title: c.title, series: b.series });
        });
      });
      var soonHtml = soon.length ? '<section class="soon"><h2 class="section-title">בפרקים הבאים</h2><ol class="soon-list">' +
        soon.map(function (c) {
          return '<li><span class="soon-n">' + c.n + '</span><span class="soon-t">' + esc(c.title) + "</span></li>";
        }).join("") + "</ol></section>" : "";

      setView("library",
        '<section class="hero">' +
          '<h1 class="hero-title">סיפורים קטנים<br>על דברים גדולים</h1>' +
          '<p class="hero-text">ספרי ילדים מאוירים בהשראת התורה, לקריאה יחד מהטלפון. כל ההכנסות הולכות לצדקה.</p>' +
          '<a class="hero-link" href="#/about">על המיזם</a>' +
        "</section>" +
        '<section class="shelf">' + cards + "</section>" + soonHtml + footer());
    });
  }

  function viewCover(id) {
    loadBook(id).then(function (b) {
      document.title = b.title + " · " + SITE.name;
      var last = parseInt(store("progress:" + b.id), 10);
      var cont = last > 1 && last <= b.pages.length
        ? '<a class="btn btn-ghost" href="#/book/' + b.id + "/" + last + '">להמשיך מעמוד ' + last + "</a>" : "";
      setView("cover",
        '<section class="cover">' +
          '<div class="cover-art">' + b.cover + "</div>" +
          '<div class="cover-text">' +
            '<p class="cover-series">' + esc(b.series) + " · פרק " + b.chapter + "</p>" +
            '<h1 class="cover-title">' + esc(b.title) + "</h1>" +
            '<p class="cover-sub">' + esc(b.subtitle) + "</p>" +
            '<div class="cover-actions">' +
              '<a class="btn btn-primary" href="#/book/' + b.id + '/1">להתחיל לקרוא</a>' + cont +
            "</div>" +
            '<p class="cover-note">' + b.pages.length + " עמודים · מחליקים הצידה כדי לדפדף</p>" +
          "</div>" +
        "</section>");
    }, notFound);
  }

  function viewReader(id, n) {
    loadBook(id).then(function (b) {
      var total = b.pages.length;
      if (n < 1) return go("#/book/" + id, true);
      if (n > total + 1) return go("#/book/" + id + "/" + (total + 1), true);
      document.title = b.title + " · " + SITE.name;

      var existing = app.querySelector(".reader[data-book='" + id + "']");
      if (!existing) {
        setView("reader",
          '<section class="reader" data-book="' + id + '">' +
            '<div class="reader-bar">' +
              '<a class="reader-close" href="#/book/' + id + '" aria-label="חזרה לכריכה">✕</a>' +
              '<div class="progress" role="progressbar" aria-valuemin="1" aria-valuemax="' + (total + 1) + '"><span></span></div>' +
              '<span class="reader-count" aria-live="polite"></span>' +
            "</div>" +
            '<div class="stage"></div>' +
            '<div class="reader-nav">' +
              '<button class="nav-btn nav-prev" type="button" aria-label="העמוד הקודם">→</button>' +
              '<button class="nav-btn nav-next" type="button" aria-label="העמוד הבא">←</button>' +
            "</div>" +
          "</section>");
        bindReader(id);
      }
      renderPage(b, n);
    }, notFound);
  }

  var current = { id: null, n: 0 };

  function pageHtml(b, n) {
    var total = b.pages.length;
    if (n <= total) {
      var p = b.pages[n - 1];
      return '<article class="page' + (isDark(p.bg) ? " page-dark" : "") + '">' +
        '<div class="page-art" aria-hidden="true">' + p.art + "</div>" +
        '<div class="page-text"><p>' + esc(p.text).replace(/\n/g, "<br>") + "</p></div>" +
        "</article>";
    }
    // end page
    var q = (b.questions || []).map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");
    var next = (b.nextChapters || []).slice(0, 1)[0];
    return '<article class="page page-end">' +
      '<div class="end-inner">' +
        '<p class="end-mark">סוֹף פֶּרֶק ' + b.chapter + "</p>" +
        '<p class="end-teaser">' + esc(b.teaser) + "</p>" +
        (next ? '<p class="end-next">פֶּרֶק ' + (b.chapter + 1) + ": <strong>" + esc(next.title) + "</strong> · בְּקָרוֹב</p>" : "") +
        (q ? '<div class="end-questions"><h2>לְשִׂיחָה אַחֲרֵי הַקְּרִיאָה</h2><ul>' + q + "</ul></div>" : "") +
        sourcesHtml(b.sourcesNotes) +
        '<div class="end-actions">' + donateButton() +
          '<a class="btn btn-ghost" href="#/about">לאן הולך הכסף?</a>' +
          '<a class="btn btn-link" href="#/book/' + b.id + '/1">לקרוא שוב מההתחלה</a>' +
        "</div>" +
      "</div></article>";
  }

  function isDark(hex) {
    var m = /^#?([0-9a-f]{6})$/i.exec(hex || "");
    if (!m) return false;
    var n = parseInt(m[1], 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    return (0.299 * r + 0.587 * g + 0.114 * b) < 128;
  }

  // "(1) ... (2) ..." -> list of sources for parents
  function sourcesHtml(notes) {
    if (!notes) return "";
    var parts = notes.split(/\s*\(\d+\)\s*/);
    var intro = parts.shift().replace(/[:：]\s*$/, "");
    return '<details class="end-sources"><summary>' + esc(intro || "מקורות להורים") + "</summary><ol>" +
      parts.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol></details>";
  }

  function renderPage(b, n) {
    var stage = app.querySelector(".stage");
    if (!stage) return;
    var total = b.pages.length;
    var dir = current.id === b.id && current.n ? (n > current.n ? "next" : n < current.n ? "prev" : "") : "";
    current = { id: b.id, n: n };
    if (n <= total) store("progress:" + b.id, String(n));

    var old = stage.querySelector(".page:not(.leaving)");
    var tmp = document.createElement("div");
    tmp.innerHTML = pageHtml(b, n);
    var page = tmp.firstChild;
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (old && dir && !reduce) {
      page.classList.add("enter-" + dir);
      stage.appendChild(page);
      old.classList.add("leaving", "leave-" + dir);
      old.style.transform = "";
      page.getBoundingClientRect();
      page.classList.remove("enter-" + dir);
      setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, 420);
    } else {
      stage.innerHTML = "";
      stage.appendChild(page);
    }

    app.querySelector(".progress span").style.width = (n / (total + 1) * 100) + "%";
    app.querySelector(".progress").setAttribute("aria-valuenow", n);
    app.querySelector(".reader-count").textContent = n <= total ? n + " / " + total : "סוף";
    app.querySelector(".nav-prev").disabled = false;
    app.querySelector(".nav-next").disabled = n > total;
    var bg = n <= total ? (b.pages[n - 1].bg || "") : "";
    document.body.style.setProperty("--reader-bg", bg || "var(--paper)");
    document.body.classList.toggle("reader-dark", isDark(bg));
  }

  function turn(id, delta) {
    var b = books[id];
    if (!b || current.id !== id) return;
    var n = current.n + delta;
    if (n < 1) return go("#/book/" + id);
    if (n > b.pages.length + 1) return;
    go("#/book/" + id + "/" + n, true);
  }

  function bindReader(id) {
    var stage = app.querySelector(".stage");
    app.querySelector(".nav-next").addEventListener("click", function () { turn(id, 1); });
    app.querySelector(".nav-prev").addEventListener("click", function () { turn(id, -1); });

    // Swipe. The book reads right-to-left, so the next page is on the left:
    // dragging the page to the right turns forward, to the left turns back.
    var startX = 0, startY = 0, dx = 0, dragging = false, locked = null, page = null;

    stage.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      if (e.target.closest("a, button")) return;
      startX = e.clientX; startY = e.clientY; dx = 0; dragging = true; locked = null;
      page = stage.querySelector(".page:not(.leaving)");
    });
    stage.addEventListener("pointermove", function (e) {
      if (!dragging || !page) return;
      var mx = e.clientX - startX, my = e.clientY - startY;
      if (locked === null && (Math.abs(mx) > 8 || Math.abs(my) > 8)) {
        locked = Math.abs(mx) > Math.abs(my) ? "x" : "y";
        if (locked === "x") { page.classList.add("dragging"); try { stage.setPointerCapture(e.pointerId); } catch (err) {} }
      }
      if (locked !== "x") return;
      dx = mx;
      page.style.transform = "translateX(" + dx * 0.9 + "px) rotate(" + dx * 0.012 + "deg)";
    });
    function end() {
      if (!dragging) return;
      dragging = false;
      if (page) { page.classList.remove("dragging"); }
      if (locked === "x" && Math.abs(dx) > Math.min(90, window.innerWidth * 0.18)) {
        turn(id, dx > 0 ? 1 : -1);
      } else if (page) {
        page.style.transform = "";
      }
      page = null;
    }
    stage.addEventListener("pointerup", end);
    stage.addEventListener("pointercancel", end);

    // Tap on the outer edges also turns pages (left edge = forward).
    stage.addEventListener("click", function (e) {
      if (e.target.closest("a, button") || Math.abs(dx) > 8) return;
      var r = stage.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width;
      if (x < 0.22) turn(id, 1); else if (x > 0.78) turn(id, -1);
    });
  }

  document.addEventListener("keydown", function (e) {
    if (document.body.getAttribute("data-view") !== "reader" || !current.id) return;
    if (e.key === "ArrowLeft" || e.key === " " || e.key === "PageDown") { e.preventDefault(); turn(current.id, 1); }
    else if (e.key === "ArrowRight" || e.key === "PageUp") { e.preventDefault(); turn(current.id, -1); }
    else if (e.key === "Escape") go("#/book/" + current.id);
  });

  function viewAbout() {
    document.title = "על המיזם · " + SITE.name;
    setView("about",
      '<section class="about">' +
        '<h1 class="about-title">על המיזם</h1>' +
        '<p class="about-lead">ספרייה קטנה היא מיזם של ספרי ילדים מאוירים בעברית, בהשראת סיפורי התורה והמדרש. הספרים נכתבים לקריאה משותפת של הורים וילדים, ישר מהטלפון.</p>' +
        '<div class="split">' +
          '<div class="split-visual" aria-hidden="true">' +
            '<svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="80" fill="#F3E3C3"/><path d="M100 20a80 80 0 0 1 0 160z" fill="#E9A23B"/><path d="M100 20a80 80 0 0 0 0 160z" fill="#24305E"/><circle cx="100" cy="100" r="34" fill="#FBF6EC"/></svg>' +
          "</div>" +
          '<div class="split-text">' +
            '<p class="split-head">כל ההכנסות הולכות לצדקה</p>' +
            '<div class="split-row"><span class="dot dot-ink"></span><div><strong>חצי ליצירת ספרים נוספים</strong><p>כתיבה, איור והפקה של הפרקים הבאים, כדי שיותר ילדים יקבלו עוד סיפורים.</p></div></div>' +
            '<div class="split-row"><span class="dot dot-sun"></span><div><strong>חצי לעמותות שנבחר</strong><p>עמותות שעוזרות לילדים ולמשפחות. רשימת העמותות ודיווח על הסכומים יפורסמו כאן.</p></div></div>' +
          "</div>" +
        "</div>" +
        '<h2 class="section-title">למה ככה?</h2>' +
        '<p>כמו יוּד, האות הכי קטנה באלף־בית: גם תרומה קטנה יכולה להיות חלק ממשהו גדול. כל רכישה מממנת ספר נוסף, וגם עוזרת למי שצריך עכשיו.</p>' +
        '<h2 class="section-title">שקיפות</h2>' +
        '<p>נפרסם כאן באופן קבוע כמה נאסף, כמה הועבר לכל עמותה, ומה נוצר מהחצי השני.</p>' +
        '<div class="about-actions">' + donateButton() + '<a class="btn btn-ghost" href="#/">לספרים</a></div>' +
        '<p class="about-note">הקישור לתרומה הוא זמני בשלב זה.</p>' +
      "</section>" + footer());
  }

  function footer() {
    return '<footer class="footer"><p>' + esc(SITE.name) + " · כל ההכנסות לצדקה</p>" + donateButton("btn-small") + "</footer>";
  }

  function notFound() {
    setView("notfound", '<section class="about"><h1 class="about-title">העמוד לא נמצא</h1><p><a href="#/">חזרה לספרייה</a></p></section>');
  }

  // ---------- router ----------

  function route() {
    var parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    if (parts[0] !== "book" || !parts[2]) {
      current = { id: null, n: 0 };
      document.body.classList.remove("reader-dark");
    }
    if (!parts.length) return viewLibrary();
    if (parts[0] === "about") return viewAbout();
    if (parts[0] === "book" && parts[1]) {
      if (parts[2]) return viewReader(parts[1], parseInt(parts[2], 10) || 1);
      return viewCover(parts[1]);
    }
    notFound();
  }

  window.addEventListener("hashchange", route);
  route();
})();
