import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { loadFile } from "@/lib/fetch";

interface props {
  onFileUpload: (FileUpload: boolean) => void;
}

export const FileUpload: React.FC<props> = ({ onFileUpload }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [state, setState] = useState<string | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedFile) {
      setState("Please select a file first!");
      return;
    }
    if (selectedFile.name.includes(" ")) {
      setState("File name cannot contain spaces!");
      return;
    }
    setState("Loading...");
    const formData = new FormData();
    formData.append('file', selectedFile);
    console.log("formData: ", formData)
    await loadFile(formData);
    onFileUpload(true);
    setState("File uploaded successfully!");
    setTimeout(() => {
      setState(null);
    }, 2000);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="grid w-full gap-3">
      <Label htmlFor="pdf">Upload  file</Label>
      <Input className="transition-opacity duration-200 hover:opacity-40" id="pdf" type="file" accept="application/pdf" onChange={handleFileChange}/>
      <Button type="submit" className="mt-4">Upload PDF</Button>
      {state && <p>{state}</p>}
    </div>
    </form>
  );
};
