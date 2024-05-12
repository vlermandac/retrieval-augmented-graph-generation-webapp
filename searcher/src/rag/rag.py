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
        return answer.choices[0].message

    def get_result_ids(self):
        if len(self.result_ids) == 0:
            print("No results to display.")
            return
        return self.result_ids

    def query_embedding(self, query):
        embedd = self.openai.embeddings.create(
            input=query,
            model=self.embedding_model,
            dimensions=self.dims
        )
        return embedd.data[0].embedding

    def retrieval_parser(self, response):
        output = []
        if len(response["hits"]["hits"]) == 0:
            print("Your search returned no results.")
        else:
            for hit in response["hits"]["hits"]:
                text = hit["_source"]["text"]
                id = hit["_id"]
                output.append(text)
                self.result_ids.append(id)
        return output

    def retrieval(self, vector_query):
        response = self.vector_store.search(
            index=self.index,
            knn={
                "field": "embedding",
                "query_vector": vector_query,
                "k": self.k,
                "num_candidates": self.k * 4,
            },
        )
        results = self.retrieval_parser(response)
        return "\n\n".join(results)

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
