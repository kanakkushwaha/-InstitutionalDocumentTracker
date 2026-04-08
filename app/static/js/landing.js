document.addEventListener("mousemove", (event) => {
    const stage = document.querySelector(".hero-stage");
    if (!stage) {
        return;
    }

    const rect = stage.getBoundingClientRect();
    const offsetX = ((event.clientX - rect.left) / rect.width - 0.5) * 16;
    const offsetY = ((event.clientY - rect.top) / rect.height - 0.5) * -16;
    stage.style.transform = `rotateX(${offsetY}deg) rotateY(${offsetX}deg)`;
});
