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

  /* ---------- Tool filters ---------- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  var tools = document.querySelectorAll(".tool");
  var empty = document.querySelector(".tools-empty");

  if (chips.length && tools.length) {
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var key = chip.getAttribute("data-filter");
        chips.forEach(function (c) { c.classList.toggle("on", c === chip); });

        var shown = 0;
        tools.forEach(function (t) {
          var match =
            key === "all" ||
            t.getAttribute("data-cat") === key ||
            t.getAttribute("data-level") === key;
          t.hidden = !match;
          if (match) shown++;
        });
        if (empty) empty.hidden = shown !== 0;
      });
    });
  }
})();
