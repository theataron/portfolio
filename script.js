/* Connect panel, tool filters. No dependencies. */
(function () {
  "use strict";

  /* ---------- Connect panel ---------- */
  var panel = document.getElementById("connect-panel");

  if (panel) {
    document.querySelectorAll("[data-connect]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (typeof panel.showModal === "function") {
          panel.showModal();
        } else {
          panel.setAttribute("open", "");
        }
      });
    });

    panel.querySelectorAll("[data-connect-close]").forEach(function (btn) {
      btn.addEventListener("click", function () { panel.close(); });
    });

    // click on the backdrop closes it
    panel.addEventListener("click", function (e) {
      if (e.target === panel) panel.close();
    });

    // copy the email address
    panel.querySelectorAll("[data-copy]").forEach(function (btn) {
      var original = btn.textContent;
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-copy");
        var done = function () {
          btn.textContent = "Copied";
          btn.classList.add("copied");
          setTimeout(function () {
            btn.textContent = original;
            btn.classList.remove("copied");
          }, 1800);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, fallback);
        } else {
          fallback();
        }
        function fallback() {
          var ta = document.createElement("textarea");
          ta.value = text;
          ta.setAttribute("readonly", "");
          ta.style.position = "fixed";
          ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand("copy"); done(); } catch (err) { /* ignore */ }
          document.body.removeChild(ta);
        }
      });
    });
  }

  /* ---------- Tool search and filters ---------- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  var tools = document.querySelectorAll(".tool");
  var empty = document.querySelector(".tools-empty");
  var q = document.getElementById("tool-q");
  var qClear = document.querySelector("[data-tool-clear]");
  var activeKey = "all";

  if (tools.length) {
    var apply = function () {
      var term = q ? q.value.trim().toLowerCase() : "";
      var shown = 0;
      tools.forEach(function (t) {
        var byGroup =
          activeKey === "all" ||
          t.getAttribute("data-cat") === activeKey ||
          t.getAttribute("data-level") === activeKey;
        var hay = t.getAttribute("data-search") || t.textContent.toLowerCase();
        var byTerm = !term || hay.indexOf(term) !== -1;
        var match = byGroup && byTerm;
        t.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
      if (qClear) qClear.hidden = !term;
    };

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        activeKey = chip.getAttribute("data-filter");
        chips.forEach(function (c) { c.classList.toggle("on", c === chip); });
        apply();
      });
    });

    if (q) {
      q.addEventListener("input", apply);
      q.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { q.value = ""; apply(); }
      });
    }
    if (qClear) {
      qClear.addEventListener("click", function () {
        if (q) { q.value = ""; q.focus(); }
        apply();
      });
    }
  }

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var next = function () {
    return root.getAttribute("data-theme") === "light" ? "dark" : "light";
  };
  document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
    var span = btn.querySelector(".theme-label");
    var paint = function () {
      var to = next();
      var text = to === "light" ? "Light" : "Dark";
      if (span) span.textContent = text;
      btn.setAttribute("title", "Switch to " + to + " mode");
      btn.setAttribute("aria-label", "Switch to " + to + " mode");
    };
    paint();
    btn.addEventListener("click", function () {
      var to = next();
      root.setAttribute("data-theme", to);
      try { localStorage.setItem("theme", to); } catch (e) { /* ignore */ }
      paint();
    });
  });
})();
