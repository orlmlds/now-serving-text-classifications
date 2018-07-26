from embeddings import GloveEmbedding

embeddings_name = 'common_crawl_840'
embeddings_dimension = 300
glove_embeddings = GloveEmbedding(name=embeddings_name, d_emb=embeddings_dimension, show_progress=True)

