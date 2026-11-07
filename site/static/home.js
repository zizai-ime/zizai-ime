/* 字在官網首頁的視差與進場淡入。漸進增強：沒有這支程式頁面也完整可讀。
   「減少動態效果」開著時什麼都不做；手機（600px 以下）位移幅度減半。 */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var root = document.documentElement;
  var layers = Array.prototype.slice.call(document.querySelectorAll(".px[data-speed]"));
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  var ticking = false;
  var io = null;
  var on = false;

  function update() {
    ticking = false;
    if (!on) return;
    var vh = window.innerHeight;
    var scale = window.innerWidth <= 600 ? 0.5 : 1;
    for (var i = 0; i < layers.length; i++) {
      var el = layers[i];
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) continue;
      var offset = (r.top + r.height / 2) - vh / 2;
      var y = -offset * parseFloat(el.getAttribute("data-speed")) * scale;
      el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
    }
  }

  function request() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  function start() {
    on = true;
    root.classList.add("js-motion");
    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request);
    if ("IntersectionObserver" in window) {
      io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            io.unobserve(e.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px" });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add("is-in"); });
    }
    update();
  }

  function stop() {
    on = false;
    root.classList.remove("js-motion");
    window.removeEventListener("scroll", request);
    window.removeEventListener("resize", request);
    if (io) { io.disconnect(); io = null; }
    layers.forEach(function (el) { el.style.transform = ""; });
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  if (!reduce.matches) start();
  var onChange = function () { if (reduce.matches) stop(); else if (!on) start(); };
  if (reduce.addEventListener) reduce.addEventListener("change", onChange);
  else if (reduce.addListener) reduce.addListener(onChange);
})();
