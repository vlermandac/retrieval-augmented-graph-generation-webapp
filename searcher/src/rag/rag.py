from typing import List, Tuple
from core_classes import Database, LLM, EmbeddingModel


class RAG:
    def __init__(
        self, db: Database,
        embedding: EmbeddingModel,
        llm: LLM,
        index_name: str,
        top_k: int
    ) -> None:

        self.db = db
        self.llm = llm
        self.embedding = embedding
        self.index = index_name
        self.k = top_k
        self.prompt = ""
        self.result_ids = []
        self.sources = []

    def __call__(
        self, query: str,
        system_message: str = "Eres un experto en historia y política de Chile",
    ) -> Tuple[str, List[int]]:

        self.prompt = self.contextualized_query(query)
        completion = self.llm.inference(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": self.prompt},
            ],
        )
        completion += "\n\nFuentes:\n\n"
        for source in self.sources:
            completion += f"{source}\n"
        return completion, self.result_ids

    def query_embedding(self, query: str) -> List[float]:
        return self.embedding.create(input=query)

    def retrieval(self, vector_query: List[float]) -> str:
        knn = self.db.semantic_search(
            self.index,
            vector_query,
            self.k
        )
        retrieved_context = ""
        for chunk in knn:
            self.result_ids.append(chunk.id)
            print(f'"id": {chunk.id}, "text": "{chunk.text}"')
            doc_name = chunk.metadata["doc_name"]
            chunk_pages = f"(p. {chunk.metadata['start_page']} - {chunk.metadata['end_page']})"
            source = f"{doc_name} {chunk_pages}"
            self.sources.append(source)
            retrieved_context += chunk.text + "\n\n"
        return retrieved_context

    def contextualized_query(self, query: str) -> str:
        vector_query = self.query_embedding(query)
        retrieved_context = self.retrieval(vector_query)
        final_prompt = f"""
            Responde la siguiente Query en base al Contexto de abajo:
            Query:
            '''
            {query}
            '''
            Contexto:
            '''
            {retrieved_context}
            ''' """
        return final_prompt
