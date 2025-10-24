// Toggle file upload field pada admin (kelola soal & edit soal)
function toggleFileUpload(selectElement) {
    var fileDiv = document.getElementById('file-upload');
    if (fileDiv) {
        fileDiv.style.display = (selectElement.value === "gambar" || selectElement.value === "video") ? "block" : "none";
    }
}

window.addEventListener('DOMContentLoaded', function() {
    var tipeSelect = document.querySelector('select[name="tipe"]');
    if (tipeSelect) {
        toggleFileUpload(tipeSelect);
        tipeSelect.addEventListener('change', function() {
            toggleFileUpload(this);
        });
    }
});