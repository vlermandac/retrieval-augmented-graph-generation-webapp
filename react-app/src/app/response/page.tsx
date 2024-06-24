import { useEffect, useState } from 'react';
import { DisplayGraph } from '@/components/graph';
import { useContextValues } from "@/lib/response-context";
import Header from '@/components/header';

export default function ResponsePage() {

  const { responseCtx, responseCtxId } = useContextValues();
  const [idList, setIdList] = useState<number[]>([]);

  useEffect(() => {
    if (responseCtxId) setIdList(responseCtxId);
  }, [responseCtxId]);

  return (
  <div>
    <Header />
  <div className="mx-5 items-center text-center">

    <div className=" shadow-md rounded-l">
      <DisplayGraph list={ idList } />
    </div>

    <div className="sticky bottom-4 shadow-md text-lg bg-white/80 p-10 w-full h-full text-pretty">
      {responseCtx ? responseCtx : "Loading..."}
    </div>

  </div>
  </div>
  );

}

