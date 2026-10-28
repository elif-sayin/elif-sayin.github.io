// Elif Sayın — kişisel site. Dış kaynak yok; yalnızca küçük yardımcılar.

// 1) Tema: sayfa çizilmeden önce kayıtlı tercihi uygula (yanıp sönme olmasın).
//    Tercih yalnızca bu tarayıcıda tutulur; sunucuya hiçbir şey gitmez.
(function () {
  try {
    var t = localStorage.getItem("tema");
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
  } catch (e) { /* özel pencere vb. — sistem tercihi geçerli kalır */ }
})();

document.addEventListener("DOMContentLoaded", function () {
  var kok = document.documentElement;

  // 2) E-posta: adres HTML'de düz metin olarak durmaz (spam botları).
  var EPOSTA = ["elif.sayin3", "gmail.com"];
  var adres = EPOSTA.join("@");
  document.querySelectorAll("[data-eposta]").forEach(function (el) {
    el.setAttribute("href", "mailto:" + adres);
    var yazi = el.querySelector("[data-eposta-yazi]");
    if (yazi) yazi.textContent = adres;
  });

  // 3) Tema düğmesi
  var tema = document.querySelector("[data-tema-dugme]");
  if (tema) {
    tema.addEventListener("click", function () {
      var koyuMu = kok.getAttribute("data-theme") === "dark" ||
        (!kok.hasAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var yeni = koyuMu ? "light" : "dark";
      kok.setAttribute("data-theme", yeni);
      try { localStorage.setItem("tema", yeni); } catch (e) {}
    });
  }

  // 4) Sekmeler (Eğitim / Klinik / Diller). JS yoksa paneller alt alta görünür.
  var sekmeKap = document.querySelector("[data-sekmeler]");
  if (sekmeKap) {
    var sekmeler = Array.prototype.slice.call(sekmeKap.querySelectorAll("[data-sekme]"));
    var liste = sekmeKap.querySelector(".sekme-liste");
    sekmeKap.classList.add("js");
    liste.setAttribute("role", "tablist");
    sekmeler.forEach(function (s) {
      var panel = document.getElementById(s.getAttribute("data-sekme"));
      s.setAttribute("role", "tab");
      s.id = "sekme-" + panel.id;
      s.setAttribute("aria-controls", panel.id);
      panel.setAttribute("role", "tabpanel");
      panel.setAttribute("aria-labelledby", s.id);
    });

    var sec = function (id, odakla) {
      sekmeler.forEach(function (s) {
        var secili = s.getAttribute("data-sekme") === id;
        s.setAttribute("aria-selected", secili ? "true" : "false");
        s.setAttribute("tabindex", secili ? "0" : "-1");
        document.getElementById(s.getAttribute("data-sekme")).hidden = !secili;
        if (secili && odakla) s.focus();
      });
    };
    var hashPanel = function () {
      var id = location.hash.slice(1);
      return sekmeler.some(function (s) { return s.getAttribute("data-sekme") === id; }) ? id : null;
    };

    sec(hashPanel() || sekmeler[0].getAttribute("data-sekme"));

    sekmeler.forEach(function (s, i) {
      s.addEventListener("click", function (e) {
        e.preventDefault();
        sec(s.getAttribute("data-sekme"));
        if (history.replaceState) history.replaceState(null, "", "#" + s.getAttribute("data-sekme"));
      });
      s.addEventListener("keydown", function (e) {
        var yon = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (!yon) return;
        e.preventDefault();
        var hedef = sekmeler[(i + yon + sekmeler.length) % sekmeler.length];
        sec(hedef.getAttribute("data-sekme"), true);
      });
    });

    // Menüden #egitim / #klinik / #diller seçilince ilgili sekmeyi aç
    window.addEventListener("hashchange", function () {
      var id = hashPanel();
      if (id) { sec(id); (sekmeKap.closest("section") || sekmeKap).scrollIntoView(); }
    });
    if (hashPanel()) (sekmeKap.closest("section") || sekmeKap).scrollIntoView();
  }

  // 5) Mobil menü
  var dugme = document.querySelector("[data-menu-dugme]");
  var menu = document.getElementById("menu");
  if (dugme && menu) {
    dugme.addEventListener("click", function () {
      var acik = menu.classList.toggle("acik");
      dugme.setAttribute("aria-expanded", acik ? "true" : "false");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        menu.classList.remove("acik");
        dugme.setAttribute("aria-expanded", "false");
      }
    });
  }
});
