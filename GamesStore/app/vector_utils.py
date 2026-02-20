import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = None
game_vectors = None
game_ids = None

# def generate_embeddings_for_all_games(GameModel):

#     games = list(GameModel.objects.all())

#     if not games:
#         print("No games found.")
#         return

#     corpus = []

#     for game in games:
#         text = f"{game.name} {game.get_category_display()} {game.description}"
#         corpus.append(text)

#     vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = vectorizer.fit_transform(corpus)

#     for i, game in enumerate(games):
#         game.embedding = tfidf_matrix[i].toarray()[0].tolist()
#         game.save()

#     print("Embeddings generated and saved successfully.")


def recommend_similar_games(target_game, GameModel, top_n=4):
    global vectorizer, game_vectors, game_ids

    if vectorizer is None:
        generate_embeddings_for_all_games(GameModel)

    target_text = f"{target_game.name} {target_game.description} {target_game.category}"
    target_vector = vectorizer.transform([target_text])

    similarities = cosine_similarity(target_vector, game_vectors)[0]

    top_indices = np.argsort(similarities)[::-1][1:top_n+1]

    top_ids = [game_ids[i] for i in top_indices]

    return GameModel.objects.filter(id__in=top_ids)

def recommend_for_user(user, GameModel, LibraryModel, top_n=6):
    global vectorizer, game_vectors, game_ids

    owned = LibraryModel.objects.filter(user=user)

    if not owned.exists():
        return []

    if vectorizer is None:
        generate_embeddings_for_all_games(GameModel)

    owned_texts = [
        f"{item.game.name} {item.game.description} {item.game.category}"
        for item in owned
    ]

    owned_vector = np.asarray(
    vectorizer.transform(owned_texts).mean(axis=0)
)

    similarities = cosine_similarity(owned_vector, game_vectors)[0]

    top_indices = np.argsort(similarities)[::-1]

    owned_ids = owned.values_list("game_id", flat=True)

    recommendations = []

    for i in top_indices:
        if game_ids[i] not in owned_ids:
            recommendations.append(game_ids[i])
        if len(recommendations) >= top_n:
            break

    return GameModel.objects.filter(id__in=recommendations)

vectorizer = None
game_vectors = None
game_ids = None


def generate_embeddings_for_all_games(GameModel):
    global vectorizer, game_vectors, game_ids

    games = GameModel.objects.all()

    texts = [
        f"{game.name} {game.description} {game.category}"
        for game in games
    ]

    game_ids = [game.id for game in games]

    vectorizer = TfidfVectorizer(stop_words="english")
    game_vectors = vectorizer.fit_transform(texts)


def semantic_search(query, GameModel, top_k=12):
    global vectorizer, game_vectors, game_ids
    
    print("Semantic search triggered with query:", query)

    # Generate embeddings once
    if vectorizer is None:
        generate_embeddings_for_all_games(GameModel)

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, game_vectors)[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    top_ids = [game_ids[i] for i in top_indices]

    # Preserve similarity order
    preserved_order = sorted(
        GameModel.objects.filter(id__in=top_ids),
        key=lambda x: top_ids.index(x.id)
    )

    return preserved_order