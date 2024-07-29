import InputExtended from '@/components/input-extended';
import Header from '@/components/header';
                                                                              
export default function HomePage() {
  return (
    <div>
    <Header />
    <div className="my-52 flex flex-col items-center">
      <h1 className="text-4xl font-bold text-gray-800 w-full text-center tracking-tight m-5">
        🔍 Buscador de Información sobre las Violaciones a los D.D.H.H. en Chile (1973 - 1990)
      </h1>
      <div className="w-11/12 md:w-8/12">
        <InputExtended />
      </div>
      <p className="text-gray-400 text-center mb-5 mt-36">Consideraciones:</p>
        <ul className="text-gray-400 text-left list-disc">
          <li className="m-2">El sistema de búsqueda responderá en base a la documentación que posee (actualmente Informes Rettig y Valech I).</li>
          <li className="m-2">Se entregan dos tipos de respuesta: una textual, y otra visual (grafo de conocimiento).</li>
          <li className="m-2">El grafo puede tardar de 1 a 2 minutos en cargar (en etapa de optimización).</li>
          <li className="m-2">Además se entregan las fuentes de la información y sus páginas correspondientes utilizadas para responder.</li>
          <li className="m-2">No es necesario configurar nada en caso de solo realizar consultas.</li>
        </ul>
    </div>
    </div>
  );
}
