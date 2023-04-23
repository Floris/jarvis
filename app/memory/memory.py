import logging

import numpy as np
import openai
import weaviate
from weaviate.util import generate_uuid5

from settings import settings

logger = logging.getLogger()
WEAVIATE_URL = "http://localhost:8080"
OPENAI_MODEL_NAME = "text-embedding-ada-002"


def convert_text_to_vector(text: str) -> np.ndarray:
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


def get_default_schema(weaviate_index: str) -> dict:
    """
    Returns the default schema for a given Weaviate index.

    Args:
        weaviate_index (str): The name of the Weaviate index.

    Returns:
        dict: The default schema for the given index.
    """
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


class WeaviateMemoryStorage:
    def __init__(self, ai_name: str) -> None:
        """
        Initializes a new WeaviateMemoryStorage instance.

        Args:
            ai_name (str): The name of the AI.
        """
        self.client = weaviate.Client(
            WEAVIATE_URL,
            additional_headers={"X-OpenAI-Api-Key": settings.api_key},
        )

        self.index = ai_name
        self._initialize_schema()

    def __enter__(self) -> "WeaviateMemoryStorage":
        """
        Enters the WeaviateMemoryStorage instance.

        Returns:
            WeaviateMemoryStorage: The WeaviateMemoryStorage instance.
        """
        return self

    def __exit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        """
        Exits the WeaviateMemoryStorage instance.

        Args:
            exc_type (str): The type of the exception.
            exc_value (str): The value of the exception.
            traceback (str): The traceback of the exception.
        """
        logger.info("Closing Weaviate Memory Storage")
        self.clear_storage()
        self.client._connection.close()

    def _initialize_schema(self) -> None:
        """
        Creates the schema for the index.
        """
        schema = get_default_schema(self.index)
        if not self.client.schema.contains(schema):
            self.client.schema.create_class(schema)

    def add_data(self, data: str) -> str:
        """
        Adds the given data to the index.

        Args:
            data (str): The data to add to the index.

        Returns:
            str: A message indicating that the data has been inserted into memory.
        """
        vector = convert_text_to_vector(data)

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

    def clear_storage(self) -> None:
        """
        Clears the index.
        """
        self.client.schema.delete_all()
        self._initialize_schema()

        logger.info("Cleared Weaviate Memory")

    def get_most_relevant(self, data: str, num_relevant: int = 5) -> list[str]:
        """
        Returns the top N most relevant data items from the index based on the given data.

        Args:
            data (str): The data to find relevant data for.
            num_relevant (int, optional): The number of relevant data items to return. Defaults to 5.

        Returns:
            list[str]: The list of top N most relevant data items from the index.
        """
        query_embedding = convert_text_to_vector(data)
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

    def get_storage_stats(self) -> dict:
        """
        Returns the statistics for the index.

        Returns:
            dict: The statistics for the index.
        """
        result = self.client.query.aggregate(self.index).with_meta_count().do()
        class_data = result["data"]["Aggregate"][self.index]

        return class_data[0]["meta"] if class_data else {}
