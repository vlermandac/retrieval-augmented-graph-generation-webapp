import { FC, useState, useEffect } from "react";
import "@react-sigma/core/lib/react-sigma.min.css";
import Graph from "graphology";
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
      setGraph(Graph.from(jsonGraph));
      setLoading(false);
    }
  }, [jsonGraph]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
    {graph ? 
    <SigmaContainer style={sigmaStyle} settings={sigmaSettings} graph={graph}>
    </SigmaContainer>
    : <div>Loading...</div>}
    </div>
  );

};
