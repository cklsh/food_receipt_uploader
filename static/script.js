const uploadForm = document.getElementById("upload-form");
const resultEl = document.getElementById("result");
const answerEl = document.getElementById("answer");

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("file");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("/upload", { method: "POST", body: formData });
        const data = await response.json();
        resultEl.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resultEl.textContent = "Error uploading: " + err;
    }
});

document.getElementById("ask-btn").addEventListener("click", async () => {
    const question = document.getElementById("question").value;
    try {
        const response = await fetch(`/query?question=${encodeURIComponent(question)}`, {
            method: "GET"
        });
        const data = await response.json();
        answerEl.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        answerEl.textContent = "Error querying: " + err;
    }
});