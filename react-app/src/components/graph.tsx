import { FC, useState, useEffect } from "react";
import "@react-sigma/core/lib/react-sigma.min.css";
import Graph from "graphology";
import { SerializedGraph } from "graphology-types";
import { SigmaContainer } from "@react-sigma/core";

interface props {
  list: number[];
  onGraphRendered: (graphRendered: boolean) => void;
}

const sigmaSettings = {
  allowInvalidContainer: true,
  defaultNodeColor: "#DFDBF9",
  zIndex: true,
};

const sigmaStyle = { height: "800px", width: "100%" };

export const DisplayGraph:FC<props> = ({ list, onGraphRendered }) => {

  const [jsonGraph, setJsonGraph] = useState<SerializedGraph | null>(null);

  useEffect(() => {
    if (list.length === 0) return;
    const apiCall = async (list: number[]) => {
      const response = await fetch('http://localhost:8000/update-graph', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json '},
        body: JSON.stringify({ values: list })
      });
      const data = await response.json();
      setJsonGraph(data);
    };
    apiCall(list);
  }, [list]);

  useEffect(() => {
    if (jsonGraph) onGraphRendered(true);
  }, [jsonGraph, onGraphRendered]);

  const kgraph = jsonGraph ? Graph.from(jsonGraph) : new Graph();

  return (
      <SigmaContainer style={sigmaStyle} settings={sigmaSettings} graph={kgraph}>
      </SigmaContainer>
  );

};


