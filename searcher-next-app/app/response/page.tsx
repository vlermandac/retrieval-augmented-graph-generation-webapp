'use client'
import TextDisplay from '@/components/text-display';
import { DisplayGraph } from '@/components/graph';
import dynamic from 'next/dynamic';


export default function ResponsePage() {

  const SigmaContainer = dynamic(
    import("@react-sigma/core").then((mod) => mod.SigmaContainer),
    { ssr: false },
  );

  return (
    <div className="my-10 mx-40 items-center">

      <div className="p-5 border-dashed border-2 rounded">
      <SigmaContainer>
        <DisplayGraph />
      </SigmaContainer>
      </div>

      <div className="p-10 text-center text-pretty">
        <TextDisplay />
      </div>

    </div>
  );
}
