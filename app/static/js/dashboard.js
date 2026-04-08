document.addEventListener("DOMContentLoaded", () => {
    const statCards = document.querySelectorAll(".stat-card");
    statCards.forEach((card, index) => {
        card.style.animation = `dashboardPulse 5s ease-in-out ${index * 0.2}s infinite`;
    });
});
