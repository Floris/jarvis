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


class WeaviateMemory:
    def __init__(self, ai_name: str) -> None:
        """
        Initializes a new WeaviateMemory instance.

        Args:
            ai_name (str): The name of the AI.
        """
        self.client = weaviate.Client(
            WEAVIATE_URL,
            additional_headers={"X-OpenAI-Api-Key": settings.api_key},
        )

        self.index = ai_name
        self._create_schema()

    def __enter__(self) -> "WeaviateMemory":
        """
        Enters the WeaviateMemory instance.

        Returns:
            WeaviateMemory: The WeaviateMemory instance.
        """
        return self

    def __exit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        """
        Exits the WeaviateMemory instance.

        Args:
            exc_type (str): The type of the exception.
            exc_value (str): The value of the exception.
            traceback (str): The traceback of the exception.
        """
        logger.info("Closing Weaviate Memory")
        self.clear()
        self.client._connection.close()

    def _create_schema(self) -> None:
        """
        Creates the schema for the index.
        """
        schema = default_schema(self.index)
        if not self.client.schema.contains(schema):
            self.client.schema.create_class(schema)

    def add(self, data: str) -> str:
        """
        Adds the given data to the index.

        Args:
            data (str): The data to add to the index.

        Returns:
            str: A message indicating that the data has been inserted into memory.
        """
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
        """
        Returns the most relevant
            Args:
            data (str): The data to find relevant data for.

        Returns:
            list[str]: The list of most relevant data from the index.
        """
        return self.get_relevant(data, 1)

    def clear(self) -> None:
        """
        Clears the index.
        """
        self.client.schema.delete_all()

        # weaviate does not yet have a neat way to just remove the items in an index
        # without removing the entire schema, therefore we need to re-create it
        # after a call to delete_all
        self._create_schema()

        logger.info("Cleared Weaviate Memory")

    def get_relevant(self, data: str, num_relevant: int = 5) -> list[str]:
        """
        Returns the most relevant data from the index based on the given data.

        Args:
            data (str): The data to find relevant data for.
            num_relevant (int, optional): The number of relevant data to return. Defaults to 5.

        Returns:
            list[str]: The list of most relevant data from the index.
        """
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
        """
        Returns the statistics for the index.

        Returns:
            dict: The statistics for the index.
        """
        result = self.client.query.aggregate(self.index).with_meta_count().do()
        class_data = result["data"]["Aggregate"][self.index]

        return class_data[0]["meta"] if class_data else {}
