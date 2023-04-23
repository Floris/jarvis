import logging

import numpy as np
import openai
import weaviate
from weaviate.util import generate_uuid5

from settings import settings

logger = logging.getLogger()
WEAVIATE_URL = "http://localhost:8080"
OPENAI_MODEL_NAME = "text-embedding-ada-002"


def text_to_vector(text: str) -> np.ndarray:
    """
    Convert the given text to a vector using OpenAI's text-embedding-ada-002 model.

    Args:
        text (str): The text to convert.

    Returns:
        np.ndarray: The vector representation of the given text.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
    )
    embeddings = response.data[0].embedding

    return np.array(embeddings, dtype=np.float32)


def default_schema(weaviate_index: str) -> dict:
    return {
        "class": weaviate_index,
        "properties": [
            {
                "name": "raw_text",
                "dataType": ["text"],
                "description": "original text for the embedding",
            }
        ],
    }


class WeaviateMemory:
    def __init__(self, ai_name: str) -> None:
        self.client = weaviate.Client(
            WEAVIATE_URL,
            additional_headers={"X-OpenAI-Api-Key": settings.api_key},
        )

        self.index = ai_name
        self._create_schema()

    def __enter__(self) -> "WeaviateMemory":
        return self

    def __exit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        logger.info("Closing Weaviate Memory")
        self.clear()
        self.client._connection.close()

    def _create_schema(self) -> None:
        schema = default_schema(self.index)
        if not self.client.schema.contains(schema):
            self.client.schema.create_class(schema)

    def add(self, data: str) -> str:
        vector = text_to_vector(data)

        doc_uuid = generate_uuid5(data, self.index)
        data_object = {"raw_text": data}

        with self.client.batch as batch:
            batch.add_data_object(
                uuid=doc_uuid,
                data_object=data_object,
                class_name=self.index,
                vector=vector,
            )

        return f"Inserting data into memory at uuid: {doc_uuid}:\n data: {data}"

    def get(self, data: str) -> list[str]:
        return self.get_relevant(data, 1)

    def clear(self) -> None:
        self.client.schema.delete_all()

        # weaviate does not yet have a neat way to just remove the items in an index
        # without removing the entire schema, therefore we need to re-create it
        # after a call to delete_all
        self._create_schema()

        logger.info("Cleared Weaviate Memory")

    def get_relevant(self, data: str, num_relevant: int = 5) -> list[str]:
        query_embedding = text_to_vector(data)
        results = (
            self.client.query.get(self.index, ["raw_text"])
            .with_near_vector({"vector": query_embedding, "certainty": 0.7})
            .with_limit(num_relevant)
            .do()
        )

        if len(results["data"]["Get"][self.index]) > 0:
            return [
                str(item["raw_text"]) for item in results["data"]["Get"][self.index]
            ]
        else:
            return []

    def get_stats(self) -> dict:
        result = self.client.query.aggregate(self.index).with_meta_count().do()
        class_data = result["data"]["Aggregate"][self.index]

        return class_data[0]["meta"] if class_data else {}
