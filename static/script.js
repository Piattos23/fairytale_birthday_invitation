(() => {
  const sparkleLayer = document.querySelector(".sparkle-layer");

  // Gentle floating sparkle trail. Limited to desktop pointer movement.
  let lastSparkle = 0;
  if (sparkleLayer && window.matchMedia("(pointer:fine)").matches) {
    document.addEventListener("pointermove", (event) => {
      const now = Date.now();
      if (now - lastSparkle < 75) return;
      lastSparkle = now;
      const sparkle = document.createElement("span");
      sparkle.className = "mouse-sparkle";
      sparkle.textContent = Math.random() > .5 ? "✧" : "·";
      sparkle.style.left = `${event.clientX + (Math.random() * 12 - 6)}px`;
      sparkle.style.top = `${event.clientY + (Math.random() * 12 - 6)}px`;
      document.body.appendChild(sparkle);
      window.setTimeout(() => sparkle.remove(), 800);
    });
  }

  // Occasional ambient sparkles across the background.
  if (sparkleLayer) {
    window.setInterval(() => {
      if (document.hidden) return;
      const sparkle = document.createElement("span");
      sparkle.className = "sparkle";
      sparkle.textContent = Math.random() > .5 ? "✧" : "✦";
      sparkle.style.left = `${Math.random() * 100}%`;
      sparkle.style.top = `${Math.random() * 100}%`;
      sparkleLayer.appendChild(sparkle);
      window.setTimeout(() => sparkle.remove(), 900);
    }, 650);
  }

  // Envelope opening and invitation reveal.
  const openButton = document.getElementById("openEnvelope");
  const envelope = document.getElementById("envelope");
  const invitation = document.getElementById("invitationCard");
  if (openButton && envelope && invitation) {
    openButton.addEventListener("click", () => {
      if (envelope.classList.contains("open")) return;
      envelope.classList.add("open");
      openButton.disabled = true;
      window.setTimeout(() => {
        invitation.classList.add("revealed");
        invitation.setAttribute("aria-hidden", "false");
        invitation.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 850);
    });
  }

  // Subtle 3D tilt on cards for mouse/trackpad users.
  if (window.matchMedia("(pointer:fine)").matches &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll(".tilt-card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width;
        const y = (event.clientY - rect.top) / rect.height;
        const rotateY = (x - .5) * 4;
        const rotateX = (.5 - y) * 4;
        card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
      });
      card.addEventListener("pointerleave", () => {
        card.style.transform = "";
      });
    });
  }

  // Confetti burst on affirmative RSVP. The form still submits normally to Flask.
  const form = document.getElementById("rsvpForm");
  if (form) {
    form.addEventListener("submit", (event) => {
      const submitter = event.submitter;
      if (!submitter || submitter.value !== "Yes") return;
      burstConfetti();
    });
  }

  function burstConfetti() {
    const colors = ["#e8abc6", "#c8b8e8", "#f4d5a6", "#ffffff", "#d99fbc"];
    const pieces = 75;
    for (let i = 0; i < pieces; i++) {
      const piece = document.createElement("i");
      piece.style.position = "fixed";
      piece.style.zIndex = "100";
      piece.style.left = `${45 + Math.random() * 10}%`;
      piece.style.top = `${42 + Math.random() * 8}%`;
      piece.style.width = `${5 + Math.random() * 6}px`;
      piece.style.height = `${8 + Math.random() * 8}px`;
      piece.style.borderRadius = Math.random() > .5 ? "50%" : "2px";
      piece.style.background = colors[Math.floor(Math.random() * colors.length)];
      piece.style.pointerEvents = "none";
      document.body.appendChild(piece);

      const dx = (Math.random() - .5) * window.innerWidth * .9;
      const dy = 150 + Math.random() * window.innerHeight * .65;
      const rotation = Math.random() * 900 - 450;
      const animation = piece.animate([
        { transform: "translate(0,0) rotate(0deg)", opacity: 1 },
        { transform: `translate(${dx}px,${dy}px) rotate(${rotation}deg)`, opacity: 0 }
      ], { duration: 900 + Math.random() * 900, easing: "cubic-bezier(.12,.65,.3,1)" });
      animation.onfinish = () => piece.remove();
    }
  }
})();
