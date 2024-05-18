import InputExtended from '@/components/input-extended';
                                                                              
export default function HomePage() {
  return (
    <div className="m-52 items-center">
      <h1 className="text-5xl font-bold text-gray-800 w-full text-center tracking-tight m-5">🔍 Insert your query   </h1>
      <div className="w-full m-5">
        <InputExtended />
      </div>
    </div>
  );
}
