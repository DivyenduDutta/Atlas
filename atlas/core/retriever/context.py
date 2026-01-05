import os

from atlas.utils.embedder_utils import generate_embedding
from atlas.core.indexer.faiss_vector_store import FaissVectorStore

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


def retrieve_context(results_load_path: str, user_query: str, k: int = 5) -> str | None:
    """
    Retrieve the context for the user query. The context is the concatenated text of the most
    relevant chunks associated with the user query.

    Args:
        results_load_path (str): Directory to load the above mentioned two result files from.
        user_query (str): User query to retrieve context for.
        k (int): Number of most similar embeddings (aka neighbors) to the query vector.
                 Default is 5.

    Returns:
        str | None: The context associated with the user query.
    """

    # 1. load the vector store
    store = FaissVectorStore(
        dim=384
    )  # the encoder model we used generated embeddings of size 384
    try:
        store.load(results_load_path)
    except Exception as e:
        LOGGER.error(f"Error while retrieving context : {repr(e)}")
        return None

    # 2. embded user query
    encoder_config_path = os.path.join(
        os.getcwd(), "atlas", "core", "configs", "sentence_transformer_config.yaml"
    )
    query_vector = generate_embedding(user_query, encoder_config_path)

    # 3. search for k top neighbors
    try:
        results = store.search(query_vector, k)
    except Exception as e:
        LOGGER.error(f"Error while retrieving context : {repr(e)}")
        return None

    # 4. build and return context
    context_parts = []
    if results == []:
        return ""

    for rank, result in enumerate(results):
        context_parts.append(f"[Context {rank + 1}]\n{result['text'].strip()}")

    return "\n\n".join(context_parts)


if __name__ == "__main__":
    LOGGER.info("-" * 20)
    LOGGER.info("Retrieve context for user prompt")

    # this is the root folder which loads the following 2 files:
    # 1. index file
    # 2. metadata json
    results_load_path = r"D:\\Deep learning\\Atlas\\Resources"
    user_query = (
        "Journey is more important that the final result in life"  # paraphrasing
    )
    k = 3  # retrieve 3 most relevant chunks as the context for the user query

    context = retrieve_context(results_load_path, user_query, k)

    if context:
        LOGGER.info("context found: \n\n")
        LOGGER.info(context)
    elif context == "":
        LOGGER.warning("No context found!!!")
    else:
        LOGGER.error("Error while trying to find context!!!")
