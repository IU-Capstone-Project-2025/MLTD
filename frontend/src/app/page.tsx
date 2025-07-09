"use client";

import * as React from "react";
import {toast} from "sonner";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { AlertTriangleIcon, CheckCircle2Icon, FileInputIcon, FileTextIcon, ScrollTextIcon, Trash2Icon, UploadCloudIcon } from "lucide-react";

import { renderToString } from "react-dom/server";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

function ControlButton({...props}) {
  return (<Button className=" bg-indigo-600 hover:bg-indigo-800 text-violet-400 hover:text-violet-500 text-center text-l rounded-md border-inherit hover:border-inherit border-8 scale-125" {...props}/>);
}

function FormatSelection() {

  return (
  <div className="bg-indigo-600 hover:bg-indigo-800 text-violet-400 hover:text-violet-500 text-center text-l rounded-md border-inherit hover:border-inherit border-8 scale-125">

    <select id="format-selector">
      <option value="" disabled>Log Format</option>
      <option value="BGL">BGL</option>
      <option value="HDFS">HDFS</option>
      <option value="MAC">MAC</option>
    </select>
  </div>);
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
    <div className="cursor-pointer items-center text-center w-screen bg-indigo-700 hover:bg-indigo-800 text-violet-400 hover:text-violet-500 border-inherit border-8 rounded-md" onChange={showFileName}>
      <Label htmlFor="file-input" onChange={showFileName}>
        <Card className="cursor-pointer items-center text-center w-screen text-inherit bg-inherit border-none rounded-md">
          <CardContent>
            <div className="flex items-center justify-center" id="file-icon">
              <FileInputIcon className="w-16 h-16" />
            </div>
            <p id="file-label" className="text-xl font-semibold">No file chosen.</p>
          </CardContent>
        </Card>
      </Label>
      <Input id="file-input" type="file" className="hidden" onChange={showFileName} accept=".txt, .log, .csv" />
    </div>);
}



function PostiveResultAlert({...props}) {
  return (
    <Alert className="bg-green-600 text-xl w-fit">
      <CheckCircle2Icon className="scale-150"/>
      <AlertTitle>Finished</AlertTitle>
      <AlertDescription className="text-white" {...props} />
    </Alert>
  );
}

function NegativeResultAlert({...props}) {
  return (
    <Alert className="bg-red-700 text-xl w-fit">
      <AlertTriangleIcon className="scale-150" />
      <AlertTitle>Finished</AlertTitle>
      <AlertDescription className="text-white" {...props} />
    </Alert>
  );
}

function clearFile() {
  const results: HTMLDivElement | null = document.getElementById("results")as HTMLDivElement;
  const file_icon: HTMLDivElement | null = document.getElementById("file-icon") as HTMLDivElement;
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const file_label: HTMLParagraphElement | null = document.getElementById("file-label") as HTMLParagraphElement;
  const files: FileList | null = (file_input ? file_input.files : null);

  if (!files || files.length == 0) {
    toast.warning("No files to remove.");
    return;
  }

  file_icon.innerHTML = renderToString(<FileInputIcon className="w-16 h-16" />);
  file_label.innerText = "No file chosen.";
  file_input.value = "";
  results.innerHTML = "";

  toast.info("Removed file(s)");
}

async function uploadFile() {
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const files: FileList | null = (file_input ? file_input.files : null);

  if (!files || files.length == 0) {
    toast.warning("Please upload a log file!");
    return;
  }

  const file: File = files[0];
  if (!file || file.size == 0) {
    toast.error("Malformed or empty file!");
    return;
  }

  const file_name = files[0].name;
  if (!file_name.endsWith(".txt") && !file_name.endsWith(".log") && !file_name.endsWith(".csv")) {
    toast.warning("File name must end with .txt, .log, or .csv!");
    return;
  }
  
  const formdata = new FormData();
  formdata.append("file", file);

  const response = await fetch("http://localhost:8000/upload", {method: "POST", body: formdata});
  
  if (response.ok) {
    toast.success(`Successfully uploaded "${file_name}".`);
    return;
  }

  toast.error(`Failed to upload "${file_name}".`);
}

async function analyzeFile() {
  const file_input: HTMLInputElement | null = document.getElementById("file-input") as HTMLInputElement;
  const files: FileList | null = (file_input ? file_input.files : null);
  const format_selector: HTMLSelectElement | null = document.getElementById("format-selector") as HTMLSelectElement;
  const results: HTMLDivElement | null = document.getElementById("results") as HTMLDivElement;

  if (!files || files.length == 0) {
    toast.warning("Please upload a file to analyze threats!")
    return;
  }

  const file_name = files[0].name;
  const log_format = format_selector.value;
  const response = await fetch(`http://localhost:8000/analyze/${file_name}?format=${log_format}`);
  if (!response.ok) {
    toast.error("Failed");
    return;
  }

  const json_data = await response.json();
  const probability = json_data.probability;

  if (!probability || probability < 0) {
    toast.error("Missing or malformed result data.");
    return;

  }

  if (probability < 0.4) {
    results.innerHTML = renderToString(<PostiveResultAlert>No threats were found in "{file_name}"</PostiveResultAlert>)
    toast.success(`No threats were found in "${file_name}"`);
    return;
  }
  results.innerHTML = renderToString(<NegativeResultAlert>{probability}% chance of (a) threat(s) in "{file_name}"</NegativeResultAlert>);
  toast.warning(`${probability} percent chance of (a) threat(s) in "${file_name}"!`);
}

export default function Home() {
  return (
        <div className="text-center items-center font-semibold font-mono space-y-15">
          <div className="text-violet-400 text-xl space-y-10">
              <h1 className="text-3xl font-bold">Welcome to MLTD!</h1>
              <p>Here you can upload log files (.txt, .log, and .csv) contating system or network activity, and have them sent to a threat detection API to find potential threats in your infrastructure.</p>
          </div>
          

          <div id="controls" className="text-violet-400 items-center space-x-20 space-y-5">
            <FileBrowser />
            <div className="flex space-x-10 h-10 items-center justify-center">
              <ControlButton onClick={uploadFile}><UploadCloudIcon className="scale-150" />Upload</ControlButton>
              <ControlButton onClick={analyzeFile}><ScrollTextIcon className="scale-150" />Analyze</ControlButton>
              <ControlButton onClick={clearFile}><Trash2Icon className="scale-150" />Clear</ControlButton>
              <FormatSelection />
            </div>
          </div>
          <br />
          <div id="results" className="flex text-white text-center items-center justify-center scale-200">  
          </div>
      </div>);
}