import { useEffect, useState } from 'react';
import { DisplayGraph } from '@/components/graph';
import { useContextValues } from "@/lib/response-context";

export default function ResponsePage() {

  const { responseCtx, responseCtxId } = useContextValues();
  const [graphRendered, setGraphRendered] = useState<boolean>(false);
  const [idList, setIdList] = useState<number[]>([]);

  const handleGraphRendered = (isRendered: boolean) => {
    setGraphRendered(isRendered);
  };

  useEffect(() => {
    if (responseCtxId) setIdList(responseCtxId);
  }, [responseCtxId]);

  console.log(graphRendered);

  return (
  <div className="my-10 mx-10 items-center text-center">

    <div className="p-5 border-dashed border-2 rounded">
      <DisplayGraph list={ idList } onGraphRendered={handleGraphRendered} />
    </div>

    <div className="p-10 w-full h-full text-pretty">
        {responseCtx ? responseCtx : "Loading..."}
    </div>

  </div>
  );

}

