import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from 'react-router-dom';

export const FileUpload: React.FC = () => {

  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/load-file', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      console.log(data);
      setLoading(false);
      navigate(0);
    } catch (error) {
      console.error("There was an error uploading the file!", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="grid w-full gap-3">
      <Label htmlFor="pdf">Upload  file</Label>
      <Input className="transition-opacity duration-200 hover:opacity-40" id="pdf" type="file" accept="application/pdf" onChange={handleFileChange}/>
      <Button type="submit" className="mt-4">Upload PDF</Button>
      {loading && <p>Loading... the app will reload when file is uploaded</p>}
    </div>
    </form>
  );
};
