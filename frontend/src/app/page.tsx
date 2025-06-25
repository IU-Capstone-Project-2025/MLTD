'use client'

async function uploadFile() {
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const results: HTMLElement | null = document.getElementById("results");
  const files: FileList | null = file_input.files;
  const file: File | null = files[0] ? files[0] : null;
  
  if (!file) {
    if (!results) {
      alert("Please upload a file!");
      return;
    }
    results.className = "bg-red-300 text-white";
    results.innerHTML = "<h2>Please upload a file.</h2>";
    return;
  }
  
  
  const formdata = new FormData();
  formdata.append("file", file);

  const response = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formdata
  }
  );
  
  if (response.ok) {
    if (!results) {
      alert("Successfully uploaded file(s).")
      return;
    }
    results.className = "bg-green-300 text-white";
    results.innerHTML = "<h2>Successfully uploaded file(s).</h2>";
    return;
  } else {
    if (!results) {
      return;
    }
    results.className = "bg-red-300 text-white";
    results.innerHTML = `<h2>Failed to upload file(s).</h2>`;
    return;
  }
}

async function analyzeFile() {
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const results: HTMLElement | null = document.getElementById("results");
  const files: FileList | null = file_input.files;

  if (!files) {
    alert("You must upload a file to detect threats.");
    return;
  }

  const file_name = files[0].name;

  const response = await fetch(`http://localhost:8000/detect/${file_name}`);
  const json_data = await response.json();
  const probability = json_data.probability;

  if (!probability) {
    if (!results) {
      alert("Results missing or malformed.");
      return;
    }
    results.className = "bg-red-300 text-white";
    results.innerHTML = "<h2>Results missing or malformed.</h2>";
    return;
  }

  if (probability <= .6) {
    if (!results) {
      alert(`No threats were found in "${file_name}"`);
      return;
    }
    results.className = "bg-yellow-300 text-white";
    results.innerHTML = `<h2>There is a ${probability}% chance of (a) threat(s) in "${file_name}".</h2>`;
  }
}

export default function Home() {
  return (

        <div className="bg-indigo-400 text-cyan-300 font-semibold font-mono justify-between text-center space-y-10">
          <div className="text-xl space-y-5">
              <h1 className="text-3xl font-bold">Welcome to MLTD!</h1>
              <p>Here you can upload log files (.txt, .log, and .csv) contating system or network activity, and have them sent to a threat detection API to find potential threats in your infrastructure.</p>
          </div>
          
          <div id="file-table" className="flex items-center justify-center space-x-10 space-y-10">
            <input type="file" id="file-input" className="flex bg-cyan-800 border-4 scale-125 text-3xl rounded-2xl" accept=".txt, .log, .csv"></input>
          </div>

          <div id="controls" className="flex bg-inherit items-center justify-center text-center space-x-25">
            <button onClick={uploadFile} className="text-2xl rounded-xl bg-cyan-600 hover:bg-cyan-800 text-cyan-500 hover:text-cyan-600">Upload</button>
            <button onClick={analyzeFile} className="text-2xl rounded-xl bg-cyan-600 hover:bg-cyan-800 text-cyan-500 hover:text-cyan-600">Analyze</button>
          </div>

          <div id="results" className="rounded-md flex justify-center"></div>
        </div>
  );
}
