class RAG:
    def __init__(self, Clients, index, embedding_model, dims, llm, k):
        self.index = index
        self.vector_store = Clients.elastic_search()
        self.openai = Clients.open_ai()
        self.embedding_model = embedding_model
        self.dims = dims
        self.k = k
        self.llm = llm
        self.prompt = ""
        self.result_ids = []

    def __call__(self, query, system_message="you are a helpful assistant."):
        self.prompt = self.contextualized_query(query)
        answer = self.openai.chat.completions.create(
            model=self.llm,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": self.prompt},
            ],
        )
        return answer.choices[0].message, self.result_ids

    def query_embedding(self, query):
        embedd = self.openai.embeddings.create(
            input=query,
            model=self.embedding_model,
            dimensions=self.dims
        )
        return embedd.data[0].embedding

    def retrieval(self, vector_query) -> str:
        knn = self.vector_store.semantic_search(self.index, vector_query, self.k)
        retrieved_context = ""
        for chunk in knn:
            self.result_ids.append(chunk.id)
            retrieved_context += chunk.text + "\n\n"
        return retrieved_context

    def contextualized_query(self, query):
        vector_query = self.query_embedding(query)
        retrieved_context = self.retrieval(vector_query)
        final_prompt = \
            f"""
            Answer the following Query based on the Context below:
            Query:
            '''
            {query}
            '''
            Context:
            '''
            {retrieved_context}
            '''
            """
        return final_prompt
