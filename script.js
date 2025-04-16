async function solve() {
    const clue = document.getElementById("clue").value;
    const pattern = document.getElementById("pattern").value;
    const resultDiv = document.getElementById("result");

    try {
        const response = await fetch("http://127.0.0.1:5000/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ clue, pattern })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();
        const { pattern_matches, synonyms, matches } = data;

        resultDiv.innerHTML = `
            <strong>Matches:</strong> ${[...matches].join(", ") || "None"}<br>
            <strong>Pattern Matches:</strong> ${[...pattern_matches].join(", ") || "None"}<br>
            <strong>Synonyms:</strong> ${[...synonyms].join(", ") || "None"}
        `;
    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = "Error connecting to server 😢";
    }
}
