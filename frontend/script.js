async function analyze() {
    const text = document.getElementById("inputText").value;

    const res = await fetch("https://YOUR_RENDER_BACKEND_URL/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    const data = await res.json();
    const resultDiv = document.getElementById("result");

    if (!data.emotions || Object.keys(data.emotions).length === 0) {
        resultDiv.innerHTML = "No strong emotions detected.";
    } else {
        resultDiv.innerHTML = JSON.stringify(data.emotions, null, 2);
    }
}
