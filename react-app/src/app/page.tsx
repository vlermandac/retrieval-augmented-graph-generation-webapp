import InputExtended from '@/components/input-extended';
import Header from '@/components/header';
                                                                              
export default function HomePage() {
  return (
    <div>
    <Header />
    <div className="my-52 flex flex-col items-center">
      <h1 className="text-4xl font-bold text-gray-800 w-full text-center tracking-tight m-5 md:text-6xl">🔍 Insert your query   </h1>
      <div className="w-11/12 md:w-8/12">
        <InputExtended />
      </div>
    </div>
    </div>
  );
}
