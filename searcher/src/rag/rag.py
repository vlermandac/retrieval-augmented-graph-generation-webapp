from typing import List, Tuple, Literal
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

    def __call__(
        self, query: str,
        system_message: str = "You are a helpful assistant!",
    ) -> Tuple[str, List[int]]:

        self.prompt = self.contextualized_query(query)
        completion = self.llm.inference(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": self.prompt},
            ],
        )
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
            retrieved_context += chunk.text + "\n\n"
        return retrieved_context

    def contextualized_query(self, query: str) -> str:
        vector_query = self.query_embedding(query)
        retrieved_context = self.retrieval(vector_query)
        final_prompt = f"""
            Answer the following Query based on the Context below:
            Query:
            '''
            {query}
            '''
            Context:
            '''
            {retrieved_context}
            ''' """
        return final_prompt
