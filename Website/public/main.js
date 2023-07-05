const inputText = document.getElementById("inputText");
const output_div = document.getElementById("output");
const output_text = document.getElementById("output-text");
const spinner = document.getElementById('spinner');
let form = document.getElementById('form');
let inputValue = "";

inputText.addEventListener("input", () => {
  inputValue = inputText.value;
  console.log(inputValue);
});

form.addEventListener("submit", (e) => {
    e.preventDefault();

    const data = { query: inputValue };
  
    output_div.style.display = 'none';
    spinner.style.display = 'block';

    fetch("http://127.0.0.1:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(data => {
        try {
          let score = data["answers"][0]["score"]
          
          if (score < 0.5) {
            output_text.innerHTML = "I'm sorry, I could not find a suitable answer.";
          }
          else {
            output_text.innerHTML = data["answers"][0]["answer"]
          }
          
          spinner.style.display = 'none';
          output_div.style.display = 'block';
        } catch (error) {
        output_text.innerHTML = "ERROR: Could not parse JSON response. Please try again later.";
        console.error(error);
        output_div.style.display = 'block';
        }
      })
      .catch(error => {
        output_text.innerHTML = "ERROR: Could not fetch data. Please try again later.";
        console.error(error);
        spinner.style.display = 'none';
        output_div.style.display = 'block';
    });
});