import React, { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { FaCog } from 'react-icons/fa';
import { FileUpload } from "@/components/submit";
import { Separator } from "@/components/ui/separator"

export function Settings() {
  const [settings, setSettings] = useState({
    index_name: "",
    chat_model: "",
    embedding_model: "",
    chunk_size: "",
    chunk_overlap: "",
    top_k: "",
  });

  const [indexList, setIndexList] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [configSaved, setConfigSaved] = useState<boolean>(false);

  useEffect(() => {
    setConfigSaved(false);
    const fetchIndexList = async () => {
      try {
        const response = await fetch('http://localhost:8000/list-files');
        const data = await response.json();
        setIndexList(data.files);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching index list:', error);
        setLoading(false);
      }
    };
    const fetchSettings = async () => {
      try {
        const response = await fetch('http://localhost:8000/config');
        const data = await response.json();
        setSettings({
          index_name: data.index_name,
          chat_model: data.chat_model,
          embedding_model: data.embedding_model,
          chunk_size: data.chunk_size.toString(),
          chunk_overlap: data.chunk_overlap.toString(),
          top_k: data.top_k.toString(),
        });
      } catch (error) {
        console.error('Error fetching settings:', error);
      }
    };
    fetchIndexList();
    fetchSettings();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setSettings((prevSettings) => ({
      ...prevSettings,
      [id]: value,
    }));
  };

  const handleSelectChange = (id: string, value: string) => {
    setSettings((prevSettings) => ({
      ...prevSettings,
      [id]: value,
    }));
  };

  const handleSubmit = async () => {
    const settingsJson = JSON.stringify(settings);
    console.log(settingsJson);
    const res = await fetch('http://localhost:8000/update-config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: settingsJson
    });
    const data = await res.json();
    console.log(data);
    setConfigSaved(true);
    // wait 2 seconds before hiding the success message
    setTimeout(() => {
      setConfigSaved(false);
    }, 2000);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Sheet>
      <SheetTrigger asChild>
        <div className="icon cursor-pointer transition-opacity duration-200 hover:opacity-20">
          <FaCog size={33} />
        </div>
      </SheetTrigger>

      <SheetContent className="px-12">
        <SheetHeader>
          <SheetTitle className="mb-5 text-center md:text-left">Settings</SheetTitle>
          <SheetDescription className="hidden xl:block py-4 text-center">
            Make changes to the app configuration here. Click save when you're done.
          </SheetDescription>
        </SheetHeader>

        <div className="grid gap-4 p-2">
          <div className="grid grid-cols-2 items-center">
            Index name
            <Select onValueChange={(value) => handleSelectChange("index_name", value)} 
              defaultValue={settings.index_name}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select an index" />
              </SelectTrigger>
              <SelectContent>
                {indexList.map((index) => (
                  <SelectItem key={index} value={index}>
                    {index}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 items-center">
            Chat model
            <Select onValueChange={(value) => handleSelectChange("chat_model", value)}
              defaultValue={settings.chat_model}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gpt-4o">gpt-4o</SelectItem>
                <SelectItem value="gpt-3.5-turbo">gpt-3.5-turbo</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 items-center">
            <p className="pr-2"> Embedding model </p>
            <Select onValueChange={(value) => handleSelectChange("embedding_model", value)}
              defaultValue={settings.embedding_model}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="text-embedding-3-small">text-embedding-3-small</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 items-center">
            Chunk size
            <Input id="chunk_size" value={settings.chunk_size} onChange={handleChange} />
          </div>

          <div className="grid grid-cols-2 items-center">
            <p className="pr-2"> Chunk overlap </p>
            <Input id="chunk_overlap" value={settings.chunk_overlap} onChange={handleChange} />
          </div>

          <div className="grid grid-cols-2 items-center">
            Top k
            <Input id="top_k" value={settings.top_k} onChange={handleChange} />
          </div>
        </div>

        <SheetFooter>
          <Button type="button" className="mt-6" onClick={handleSubmit}>
            Save changes
          </Button>
          {configSaved && <p className="text-center text-green-500">Config saved!</p>}
        </SheetFooter>
        <Separator className="my-5" />
        <FileUpload />
      </SheetContent>
    </Sheet>
  );
}
