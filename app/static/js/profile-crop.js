document.addEventListener("DOMContentLoaded", () => {
    const cropCards = document.querySelectorAll("[data-profile-cropper]");
    cropCards.forEach(initializeCropper);
});

function initializeCropper(card) {
    const form = card.closest("form");
    const fileInput = form?.querySelector('input[type="file"][name="profile_image"]');
    const hiddenInput = form?.querySelector('input[type="hidden"][name="profile_image_cropped"]');
    const previewImage = card.querySelector("[data-crop-preview]");
    const emptyState = card.querySelector("[data-crop-empty]");
    const controls = card.querySelector("[data-crop-controls]");
    const zoomSlider = card.querySelector('input[name="crop_zoom"]');
    const xSlider = card.querySelector('input[name="crop_x"]');
    const ySlider = card.querySelector('input[name="crop_y"]');
    const resetButton = card.querySelector("[data-crop-reset]");
    const sourceCanvas = document.createElement("canvas");
    const outputCanvas = document.createElement("canvas");
    const image = new Image();
    let sourceUrl = "";
    let state = null;

    if (!fileInput || !hiddenInput) {
        return;
    }

    image.onload = () => {
        state = {
            width: image.naturalWidth,
            height: image.naturalHeight,
            zoom: 1,
            x: 50,
            y: 50,
        };

        const minDimension = Math.min(state.width, state.height);
        const maxDimension = Math.max(state.width, state.height);
        const minZoom = 1;
        const suggestedZoom = maxDimension / minDimension;
        const maxZoom = Math.max(3, Math.ceil(suggestedZoom * 10) / 10);

        zoomSlider.min = String(minZoom);
        zoomSlider.max = String(maxZoom);
        zoomSlider.step = "0.01";
        zoomSlider.value = String(Math.min(Math.max(suggestedZoom, minZoom), maxZoom));
        state.zoom = Number(zoomSlider.value);
        xSlider.value = "50";
        ySlider.value = "50";
        controls.hidden = false;
        renderCrop();
    };

    fileInput?.addEventListener("change", () => {
        const [file] = fileInput.files || [];
        hiddenInput.value = "";
        if (!file) {
            clearPreview();
            return;
        }
        if (!file.type.startsWith("image/")) {
            clearPreview();
            return;
        }
        if (sourceUrl) {
            URL.revokeObjectURL(sourceUrl);
        }
        sourceUrl = URL.createObjectURL(file);
        image.src = sourceUrl;
    });

    [zoomSlider, xSlider, ySlider].forEach((control) => {
        control?.addEventListener("input", () => {
            if (!state) {
                return;
            }
            state.zoom = Number(zoomSlider.value || 1);
            state.x = Number(xSlider.value || 50);
            state.y = Number(ySlider.value || 50);
            renderCrop();
        });
    });

    resetButton?.addEventListener("click", () => {
        if (!state) {
            return;
        }
        xSlider.value = "50";
        ySlider.value = "50";
        zoomSlider.value = zoomSlider.min || "1";
        state.zoom = Number(zoomSlider.value);
        state.x = 50;
        state.y = 50;
        renderCrop();
    });

    function clearPreview() {
        controls.hidden = true;
        hiddenInput.value = "";
        previewImage.removeAttribute("src");
        previewImage.hidden = true;
        emptyState.hidden = false;
        state = null;
    }

    function renderCrop() {
        if (!state) {
            return;
        }

        const cropSize = Math.min(state.width, state.height) / state.zoom;
        const maxX = Math.max(0, state.width - cropSize);
        const maxY = Math.max(0, state.height - cropSize);
        const cropX = maxX * (state.x / 100);
        const cropY = maxY * (state.y / 100);

        sourceCanvas.width = state.width;
        sourceCanvas.height = state.height;
        sourceCanvas.getContext("2d").drawImage(image, 0, 0);

        outputCanvas.width = 320;
        outputCanvas.height = 320;
        const outputContext = outputCanvas.getContext("2d");
        outputContext.clearRect(0, 0, 320, 320);
        outputContext.drawImage(
            sourceCanvas,
            cropX,
            cropY,
            cropSize,
            cropSize,
            0,
            0,
            320,
            320,
        );

        const dataUrl = outputCanvas.toDataURL("image/png");
        hiddenInput.value = dataUrl;
        previewImage.src = dataUrl;
        previewImage.hidden = false;
        emptyState.hidden = true;
    }
}
