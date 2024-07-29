import React, { useEffect, useState } from 'react';
import { DisplayGraph } from '@/components/graph';
import { useContextValues } from "@/lib/response-context";
import Header from '@/components/header';

export default function ResponsePage() {

  const { responseCtx, responseCtxId } = useContextValues();
  const [idList, setIdList] = useState<number[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (responseCtxId) setIdList(responseCtxId);
  }, [responseCtxId]);

  console.log(responseCtx);

  return (
  <div>
    <Header />
  <div className="mx-5 items-center text-center">

    <div className=" shadow-md rounded-l">
      <DisplayGraph list={ idList } />
    </div>

    <div className="bottom-4 shadow-md text-lg bg-white/80 p-10 w-full h-1/6 text-pretty text-left">
      {
        responseCtx ?
        responseCtx.split('\n').map((line, index) => (
            <React.Fragment key={index}>
              {line}
              {index < responseCtx.split('\n').length - 1 && <br />}
            </React.Fragment>
          ))
        : "Cargando..."
      }
    </div>

  </div>
  </div>
  );

}

