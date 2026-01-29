console.log("🚀 menu.js iniciado");

document.addEventListener("DOMContentLoaded", () => {

  const video = document.getElementById("previewVideo");
  const whatsapp = document.getElementById("whatsappBtn");
  const hotspots = document.querySelectorAll(".hotspot");

  console.log("🧩 Elementos:", {
    video: !!video,
    whatsapp: !!whatsapp,
    hotspots: hotspots.length
  });

  if (!video || !whatsapp || !hotspots.length) {
    console.error("❌ Estructura HTML incompleta");
    return;
  }

  hotspots.forEach((spot, i) => {

    const src = spot.dataset.video;
    const product = spot.dataset.product;

    console.log(`📍 Hotspot ${i}:`, product, src);

    const show = () => {
      console.log(`▶️ Reproduciendo: ${product}`);

      video.src = src;
      video.classList.add("active");

      video.play().catch(err =>
        console.warn("⚠️ Error al reproducir video:", err.message)
      );

      const msg = `Hola 👋, quiero pedir ${product}`;
      whatsapp.href =
        "https://wa.me/573028384875?text=" + encodeURIComponent(msg);
      whatsapp.classList.add("active");
    };

    const hide = () => {
      video.pause();
      video.removeAttribute("src");
      video.load();
      video.classList.remove("active");
      whatsapp.classList.remove("active");
    };

    // Desktop
    spot.addEventListener("mouseenter", show);
    spot.addEventListener("mouseleave", hide);

    // Mobile
    spot.addEventListener("click", e => {
      e.preventDefault();
      show();
    });
  });

  console.log("✅ Menú completamente funcional");
});
