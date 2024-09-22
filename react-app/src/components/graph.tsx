import { FC, useState, useEffect } from "react";
import "@react-sigma/core/lib/react-sigma.min.css";
import Graph from "graphology";
import circular from 'graphology-layout/circular';
import { useWorkerLayoutForceAtlas2 } from "@react-sigma/layout-forceatlas2";
import { SerializedGraph } from "graphology-types";
import { SigmaContainer } from "@react-sigma/core";
import { fetchGraph } from "@/lib/fetch";
import { useCurrentIndex } from "@/lib/current-index-context";

const sigmaStyle = { height: "800px", width: "100%" };
const sigmaSettings = {
  allowInvalidContainer: true,
  renderEdgeLabels: true,
  defaultNodeColor: "#DFDBF9",
  zIndex: true,
};

interface props {
  list: number[];
}

const Fa2: FC = () => {
  const { start, kill } = useWorkerLayoutForceAtlas2(
    {
      settings: { 
        gravity: 15,
        adjustSizes: true,
        scalingRatio: 50,
      } 
    }
  );

  useEffect(() => {
    // start FA2
    start();

    // wait 5 seconds and kill FA2
    setTimeout(() => {
      kill();
    }, 3000);

  }, [start, kill]);

  return null;
};

export const DisplayGraph: FC<props> = ({ list }) => {
  const [jsonGraph, setJsonGraph] = useState<SerializedGraph | null>(null);
  const [graph, setGraph] = useState<Graph | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const { currentIndex } = useCurrentIndex();

  useEffect(() => {
    const apiCall = async () => {
      if (!currentIndex || list.length < 1) return;
      const data = await fetchGraph(currentIndex, list);
      console.log("fetch graph response: ", data);
      setJsonGraph(data);
      console.log("jsonGraph: ", jsonGraph);
    };
    apiCall();
  }, [currentIndex, list]);

  useEffect(() => {
    if (jsonGraph){
      const tmp = Graph.from(jsonGraph);
      const position = circular(tmp, { scale: 100 });
      circular.assign(tmp, position);
      setGraph(tmp);
      setLoading(false);
    }
  }, [jsonGraph]);

  if (loading) {
    return <div>Cargando Grafo...</div>;
  }

  return (
    <div>
    {graph ? 
    <SigmaContainer style={sigmaStyle} settings={sigmaSettings} graph={graph}>
        <Fa2 />
    </SigmaContainer>
    : <div>Cargando Grafo...</div>}
    </div>
  );

};
