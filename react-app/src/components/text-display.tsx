import { useResponseCtx } from "@/lib/response-context";

export default function TextDisplay() {

  const { responseCtx } = useResponseCtx();

  return (
    <div>
      <div className="w-full h-full flex items-center text-pretty">
        {responseCtx}
      </div>
    </div>
  );
}
