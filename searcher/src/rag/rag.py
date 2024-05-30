from typing import List, Tuple, Any, Literal


class RAG:
    def __init__(
        self, Clients: Any,
        index_name: str,
        chat_model: Literal["gpt-4o", "gpt-3.5-turbo"],
        embedding_model: str,
        embedding_dimension: int, top_k: int
    ) -> None:

        self.index = index_name
        self.vector_store = Clients.elastic_search()
        self.openai = Clients.open_ai()
        self.embedding_model = embedding_model
        self.dims = embedding_dimension
        self.k = top_k
        self.llm = chat_model
        self.prompt = ""
        self.result_ids = []

    def __call__(
        self, query: str,
        system_message: str = "You are a helpful assistant!",
    ) -> Tuple[str, List[int]]:

        self.prompt = self.contextualized_query(query)
        answer = self.openai.chat.completions.create(
            model=self.llm,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": self.prompt},
            ],
        )
        return answer.choices[0].message, self.result_ids

    def query_embedding(self, query: str) -> List[float]:
        embedd = self.openai.embeddings.create(
            input=query,
            model=self.embedding_model,
            dimensions=self.dims
        )
        return embedd.data[0].embedding

    def retrieval(self, vector_query: List[float]) -> str:
        knn = self.vector_store.semantic_search(
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
