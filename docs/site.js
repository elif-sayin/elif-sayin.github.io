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

  // 4) Mobil menü
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
