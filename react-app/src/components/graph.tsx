import "@react-sigma/core/lib/react-sigma.min.css";
import Graph from "graphology";
import { SerializedGraph } from "graphology-types";
import { SigmaContainer } from "@react-sigma/core";
import jsonGraph from "@/data/graph-data.json";
import { useGraphCtx } from "@/lib/graph-context";

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

  const { graphCtx } = useGraphCtx();

  kgraph.forEachEdge(
    (edge, attributes, source, target, sourceAttributes, targetAttributes) => {
      if (graphCtx.includes(attributes.chunk_id)) {
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
