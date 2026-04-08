document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".reveal-on-scroll");
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";
                }
            });
        },
        { threshold: 0.16 },
    );

    items.forEach((item, index) => {
        item.style.opacity = "0";
        item.style.transform = `translateY(${18 + index * 4}px)`;
        item.style.transition = "opacity 700ms ease, transform 700ms ease";
        observer.observe(item);
    });

    const filterButtons = document.querySelectorAll("[data-admin-filter]");
    const reviewGroups = document.querySelectorAll("[data-admin-role-group]");

    if (filterButtons.length && reviewGroups.length) {
        filterButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const filter = button.dataset.adminFilter;

                filterButtons.forEach((item) => item.classList.remove("is-active"));
                button.classList.add("is-active");

                reviewGroups.forEach((group) => {
                    const matches = filter === "all" || group.dataset.adminRoleGroup === filter;
                    group.hidden = !matches;
                });
            });
        });
    }
});
