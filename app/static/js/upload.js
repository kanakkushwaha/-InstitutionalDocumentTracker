document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-upload");
    const preview = document.getElementById("upload-preview");

    if (!fileInput || !preview) {
        return;
    }

    fileInput.addEventListener("change", () => {
        if (!fileInput.files.length) {
            preview.textContent = "No file selected yet.";
            return;
        }

        const file = fileInput.files[0];
        preview.textContent = `${file.name} selected (${Math.round(file.size / 1024)} KB)`;
    });
});
