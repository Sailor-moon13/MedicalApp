const imageInput = document.getElementById("image");
const preview = document.getElementById("preview");
const button = document.getElementById("predictButton");
const resultDiv = document.getElementById("result");


// Предпросмотр изображения
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if (!file) return;

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
});

// Отправка изображения
button.addEventListener("click", async () => {

    const file = imageInput.files[0];

    if (!file) {
        alert("Выберите изображение");
        return;
    }

    const model = document.getElementById("model").value;

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`/predict/${model}`, {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    resultDiv.innerHTML = `
        <h3>Результат</h3>
        <p>Класс: ${result.class}</p>
        <p>Уверенность: ${(result.confidence * 100).toFixed(2)}%</p>
    `;
});