import os
from openai import OpenAI


def generate_embedding_for_game(game):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables")

    client = OpenAI(api_key=api_key)

    text = f"""
    Game Name: {game.name}
    Category: {game.get_category_display()}
    Description: {game.description}
    Price: {game.game_price}
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding
