'use client';
import React from "react";
import { useValue } from "@/lib/response-context";

export default function TextDisplay() {

  const { value } = useValue();

  return (
    <div>
      <div className="w-full h-full flex items-center text-pretty">
        {value}
      </div>
    </div>
  );
}
