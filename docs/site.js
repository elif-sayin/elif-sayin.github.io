// Elif Sayın — kişisel site. Dış kaynak yok; yalnızca küçük yardımcılar.

// 1) Tema: varsayılan KOYU. Ziyaretçi açık temayı seçtiyse sayfa çizilmeden uygula.
//    Tercih yalnızca bu tarayıcıda tutulur; sunucuya hiçbir şey gitmez.
(function () {
  var kok = document.documentElement;
  kok.classList.add("js-hazir");
  try {
    if (localStorage.getItem("tema") === "light") kok.setAttribute("data-theme", "light");
  } catch (e) { /* özel pencere vb. — koyu tema geçerli kalır */ }
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

  // 3) Tema düğmesi (koyu ↔ açık)
  var tema = document.querySelector("[data-tema-dugme]");
  if (tema) {
    tema.addEventListener("click", function () {
      var acik = kok.getAttribute("data-theme") === "light";
      if (acik) kok.removeAttribute("data-theme"); else kok.setAttribute("data-theme", "light");
      try { localStorage.setItem("tema", acik ? "dark" : "light"); } catch (e) {}
    });
  }

  // 4) Kaydırınca beliren öğeler
  var belirenler = document.querySelectorAll(".belir");
  if ("IntersectionObserver" in window) {
    var gozcu = new IntersectionObserver(function (girdiler) {
      girdiler.forEach(function (g) {
        if (g.isIntersecting) { g.target.classList.add("gorundu"); gozcu.unobserve(g.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px" });
    belirenler.forEach(function (el) { gozcu.observe(el); });
  } else {
    belirenler.forEach(function (el) { el.classList.add("gorundu"); });
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
