import TextDisplay from '@/components/text-display';
import { DisplayGraph } from '@/components/graph';


export default function ResponsePage() {

  return (
    <div className="my-10 mx-40 items-center">

      <div className="p-5 border-dashed border-2 rounded">
        <DisplayGraph />
      </div>

      <div className="p-10 text-center text-pretty">
        <TextDisplay />
      </div>

    </div>
  );
}

