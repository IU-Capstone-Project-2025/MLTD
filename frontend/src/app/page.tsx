"use client";

import * as React from "react";
import { useRef } from "react";
import { renderToString } from "react-dom/server";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardTitle } from "@/components/ui/card";
import { AlertTriangleIcon, CheckCircle2Icon, FileInputIcon, FileTextIcon, ListRestartIcon, ScrollTextIcon, Trash2Icon, UploadCloudIcon } from "lucide-react";

const show_controls = () => {
    const controls: HTMLDivElement | null = document.getElementById("controls") as HTMLDivElement;
    const upload_control: HTMLDivElement | null = document.getElementById("upload-control") as HTMLDivElement;
    const results: HTMLDivElement | null = document.getElementById("results") as HTMLDivElement;
    const reset_button: HTMLDivElement | null = document.getElementById("reset-button") as HTMLDivElement;

    reset_button.className = "invisible";
    controls.className = "visible";
    upload_control.className = "visible";
    results.innerHTML = "";
  };

function ControlButton({...props}) {
  return (<Button type="button" className=" bg-indigo-600 hover:bg-indigo-800 text-violet-400 hover:text-violet-500 text-center text-l rounded-md border-inherit hover:border-inherit border-8 scale-150" {...props}/>);
}

function FormatSelection() {
  return (
    <select id="format-selector" defaultValue="" className="bg-indigo-600 hover:bg-indigo-800 text-violet-400 hover:text-violet-500 text-center text-l rounded-md border-inherit hover:border-inherit border-8 scale-150">
        <option value="" disabled>Log Format</option>
        <option value="BGL">BGL</option>
        <option value="HDFS">HDFS</option>
        <option value="MAC">MAC</option>
        <option value="SSH">SSH</option>
    </select>);
}

function FileBrowser() {

  const showFileName = () => {
    const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
    const file_icon: HTMLDivElement | null = document.getElementById("file-icon") as HTMLDivElement;
    const file_label: HTMLParagraphElement | null = document.getElementById("file-label") as HTMLParagraphElement;
    const files: FileList | null = (file_input ? file_input.files : null);

    if (!files || files.length == 0) {
      return;
    }
    const file: File | null = files[0] ? files[0] : null;
    
    if (!file) {
      file_icon.innerHTML = renderToString(<FileInputIcon className="w-16 h-16" />);
      file_label.innerText = "No file chosen.";
      return;
    }

    file_icon.innerHTML = renderToString(<FileTextIcon className="w-16 h-16" />);
    file_label.innerText = `${file.name}`;

  };

  return ( 
    <div className="flex-row items-center justify-center w-175 cursor-pointer bg-indigo-700 hover:bg-indigo-800 text-violet-400 hover:text-violet-500 border-inherit border-8 rounded-md" onChange={showFileName}>
      <Input id="file-input" type="file" className="hidden" onChange={showFileName} accept=".txt, .log, .csv" />
      <Label htmlFor="file-input" onChange={showFileName}>
        <Card className="flex items-center justify-center min-w-full cursor-pointer text-inherit bg-inherit border-none">
          <CardContent className="flex-row items-center justify-center text-center">
            <div className="flex items-center justify-center" id="file-icon">
              <FileInputIcon className="w-16 h-16" />
            </div>
            <p id="file-label" className="text-2xl font-semibold">No file chosen.</p>
          </CardContent>
        </Card>
      </Label>
    </div>);
}

function SuccessNotification({...props}) {
  return (
    <Alert className="bg-green-700 text-xl w-fit scale-150">
      <CheckCircle2Icon className="scale-150"/>
      <AlertTitle>Success</AlertTitle>
      <AlertDescription className="text-white" {...props} />
    </Alert>
  );
}

function FailureNotifcation({...props}) {
  return (
    <Alert className="bg-red-700 text-xl w-fit scale-150">
      <AlertTriangleIcon className="scale-150" />
      <AlertTitle>Failure</AlertTitle>
      <AlertDescription className="text-white" {...props} />
    </Alert>
  );
}

function WarningNotifcation({...props}) {
  return (
  <Alert className="bg-yellow-700 text-xl w-fit scale-150">
      <AlertTriangleIcon className="scale-150" />
      <AlertDescription className="text-white" {...props} />
  </Alert>);
}

function DotSpinner({ size = 48, dotCount = 8, dotSize = 10, color = "bg-indigo-400" }) {
  const dots = Array.from({ length: dotCount });

  return (
    <div
      className="relative animate-spin"
      style={{
        width: size,
        height: size,
      }}
    >
      {dots.map((_, i) => {
        const angle = (i / dotCount) * 2 * Math.PI;
        const radius = size / 2 - dotSize;
        const x = radius * Math.cos(angle);
        const y = radius * Math.sin(angle);
        return (
          <span
            key={i}
            className={`absolute ${color} rounded-full`}
            style={{
              width: dotSize,
              height: dotSize,
              top: size / 2 - dotSize / 2 + y,
              left: size / 2 - dotSize / 2 + x,
            }}
          />
        );
      })}
    </div>
  );
}

function ProgressNotifcation({...props}) {
  return (<Alert className="flex bg-indigo-700 text-violet-500 text-xl w-fit items-center justify-center space-x-5 scale-150">
    <DotSpinner />
    <AlertTitle {...props} />
  </Alert>);
}

function ResultNotifcation({file_name, log_format, probability, anomalies, lines}: {file_name: string, log_format: string, probability: number, anomalies: string | number, lines: string | number}) {
  
  let background_color = "bg-red-700";
  if (probability < .5) {
    background_color = "bg-green-700";
  } else if (probability < .8) {
    background_color = "bg-yellow-700";
  }

  return (<Card className={`items-center text-center w-screen ${background_color} text-white border-inherit border-8 rounded-md`}>
    <CardTitle className="text-4xl font-bold">Results</CardTitle>
    <CardDescription className="text-3xl font-semibold text-inherit">
      <p>Filename: {file_name}</p>
      <p>Log format: {log_format}</p>
      <p>Number of lines: {lines}</p>
      <p>Anomalies found: {anomalies}</p>
      <p>Probability of threat(s): {probability * 100}%</p>
    </CardDescription>
  </Card>);
}

async function uploadFile() {
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const results: HTMLDivElement | null = document.getElementById("results") as HTMLDivElement;
  const files: FileList | null = (file_input ? file_input.files : null);
  const upload_control: HTMLDivElement | null = document.getElementById("upload-control") as HTMLDivElement;
  const analyze_control: HTMLDivElement | null = document.getElementById("analyze-control") as HTMLDivElement;

  if (!files || files.length == 0) {
    results.innerHTML = renderToString(<WarningNotifcation>Please select a log file from your system!</WarningNotifcation>);
    return;
  }

  const file: File = files[0];
  if (!file || file.size == 0) {
    results.innerHTML = renderToString(<WarningNotifcation>File is empty or corrupt!</WarningNotifcation>);
    return;
  }

  const file_name = files[0].name;
  if (!file_name.endsWith(".txt") && !file_name.endsWith(".log") && !file_name.endsWith(".csv")) {
    results.innerHTML = renderToString(<WarningNotifcation>File name must end in .txt, .log, or .csv!</WarningNotifcation>)
    return;
  }
  
  const formdata = new FormData();
  formdata.append("file", file);

  results.innerHTML = renderToString(<ProgressNotifcation>Uploading {file_name}</ProgressNotifcation>);
  const response = await fetch("http://localhost:8000/upload", {method: "POST", body: formdata});

  if (response.ok) {
    results.innerHTML = renderToString(<SuccessNotification>Successfully uploaded &quot;{file_name}&quot;</SuccessNotification>)
    upload_control.className = "hidden";
    analyze_control.className = "flex-row visible space-x-20";
    return;
  }

  results.innerHTML = renderToString(<FailureNotifcation>Failed to upload &quot;{file_name}&quot;</FailureNotifcation>);
}

async function analyzeFile() {
  const controls: HTMLDivElement | null = document.getElementById("controls") as HTMLDivElement;
  const upload_control: HTMLDivElement | null = document.getElementById("upload-control") as HTMLDivElement;
  const format_selector: HTMLSelectElement | null = document.getElementById("format-selector") as HTMLSelectElement;
  const analyze_control: HTMLDivElement | null = document.getElementById("analyze-control") as HTMLDivElement;
  const reset_button: HTMLDivElement | null = document.getElementById("reset-button") as HTMLDivElement;
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const files: FileList | null = (file_input ? file_input.files : null);
  const results: HTMLDivElement | null = document.getElementById("results") as HTMLDivElement;

  if (!files || files.length == 0) {
    results.innerHTML = renderToString(<WarningNotifcation>Please upload a file to analyze threats!</WarningNotifcation>);
    return;
  }
  
  const file_name = files[0].name;
  const log_format = format_selector.value;
  if (!log_format || log_format == "") {
    results.innerHTML = renderToString(<WarningNotifcation>Please select the format of your log file!</WarningNotifcation>);
    return;
  }

  controls.className = "invisible";
  analyze_control.className = "invisible";
  results.innerHTML = renderToString(<ProgressNotifcation>Analyzing &quot;{file_name}&quot;</ProgressNotifcation>);
  
  const response = await fetch(`http://localhost:8000/analyze/${file_name}?format=${log_format}`, {method: "GET"})
  if (!response.ok) {
    switch (response.status) {
      case 400:
        controls.className = "visible";
        upload_control.className = "visible";
        analyze_control.className = "hidden";
        results.innerHTML = renderToString(<WarningNotifcation>{await response.text()}</WarningNotifcation>);
        break;

      case 404:
        controls.className = "visible";
        upload_control.className = "visible";
        analyze_control.className = "hidden";
        results.innerHTML = renderToString(<WarningNotifcation>Please upload &quot;{file_name}&quot; before analyzing it!</WarningNotifcation>);
        break;

      default:
        controls.className = "visible";
        upload_control.className = "visible";
        analyze_control.className = "hidden";
        results.innerHTML = renderToString(<FailureNotifcation>Failed to analyze &quot;{file_name}&quot;!</FailureNotifcation>);
    }
    return;
  }

  const json_data = await response.json();
  const probability = json_data.probability;
  const total_anomalies = json_data.total_anomalies;
  const total_lines = json_data.total_lines;
  if (!json_data 
    || !probability || probability < 0 
    || !total_anomalies || total_anomalies < 0
    || !total_lines || total_lines < 0) {
    controls.className = "visible";
    results.innerHTML = renderToString(<FailureNotifcation>Missing or malformed result data.</FailureNotifcation>)
    return;
  }
  reset_button.className = "visible";
  results.innerHTML = renderToString(<SuccessNotification>Finished analyzing &quot;{file_name}&quot;</SuccessNotification>);
  results.innerHTML += renderToString(<ResultNotifcation file_name={file_name} log_format={log_format} probability={probability} anomalies={total_anomalies} lines={total_lines} />);
}

export default function Home() {
  return (
        <div className="flex-col text-center items-center font-semibold font-mono space-y-10">
          <div className="text-violet-400 text-xl space-y-10">
              <h1 className="text-3xl font-bold">Welcome to MLTD!</h1>
              <p>Upload log files (.txt, .log, and .csv) that contain system or network activity, and have them sent to a threat detection API to find potential threats in your infrastructure.</p>
          </div>

          <div id="controls" className="flex-row items-center justify-center text-violet-400">
            <div className="flex items-center justify-center">
              <FileBrowser />
            </div>

            <br />
            <div className="flex-col items-center justify-center">
              <div id="upload-control" className="flex-row items-center justify-center">
                <ControlButton onClick={uploadFile}><UploadCloudIcon className="scale-150" />Upload</ControlButton>
              </div>
              
              <div id="analyze-control" className="flex-row hidden items-center justify-center space-x-20">
                <FormatSelection />
                <ControlButton onClick={analyzeFile}><ScrollTextIcon className="scale-150" />Analyze</ControlButton>
              </div>
            </div>
          </div>

          <div id="results" className="flex flex-col text-center items-center justify-center space-y-20">
          </div>

          <div id="reset-button" className="flex items-center justify-center space-y-20 invisible">
            <ControlButton onClick={show_controls}><ListRestartIcon /> Start a new scan</ControlButton>
          </div>
      </div>);
}