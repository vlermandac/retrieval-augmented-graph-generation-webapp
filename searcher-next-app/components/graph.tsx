'use client';
import React, { useEffect } from "react";
import Graph from "graphology";
// import { SigmaContainer } from "@react-sigma/core";
import "@react-sigma/core/lib/react-sigma.min.css";
import { SerializedGraph } from "graphology-types";
import jsonGraph from "@/public/graph-data.json";
import { useGraphCtx } from "@/lib/graph-context";
import dynamic from "next/dynamic";

const SigmaContainer = dynamic(
  import("@react-sigma/core").then((mod) => mod.SigmaContainer),
  { ssr: false },
);

const sigmaStyle = { height: "600px", width: "100%" };

const sigmaSettings = {
  allowInvalidContainer: true,
  labelDensity: 0.07,
  labelGridCellSize: 60,
  labelRenderedSizeThreshold: 15,
  renderEdgeLabels: true,
  defaultNodeColor: "#DFDBF9",
  zIndex: true,
};

const kgraph = Graph.from(jsonGraph as SerializedGraph);

export const DisplayGraph = () => {

  const { graph } = useGraphCtx();

  kgraph.forEachEdge(
    (edge, attributes, source, target, sourceAttributes, targetAttributes) => {
      if (graph.includes(attributes.chunk_id)) {
        kgraph.updateEdgeAttributes(edge, attr => {
          return { 
            label: attributes.label,
            size: 4,
            color: "#0E4D92",
            forceLabel: true,
          };
        });
      }
  });
  return (
    <SigmaContainer style={sigmaStyle} settings={sigmaSettings} graph={kgraph}>
    </SigmaContainer>
  );
};
