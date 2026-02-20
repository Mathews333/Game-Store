import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_embeddings_for_all_games(GameModel):

    games = list(GameModel.objects.all())

    if not games:
        print("No games found.")
        return

    corpus = []

    for game in games:
        text = f"{game.name} {game.get_category_display()} {game.description}"
        corpus.append(text)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

    for i, game in enumerate(games):
        game.embedding = tfidf_matrix[i].toarray()[0].tolist()
        game.save()

    print("Embeddings generated and saved successfully.")


def recommend_similar_games(target_game, GameModel, top_n=4):

    if not target_game.embedding:
        return []

    target_vector = np.array(target_game.embedding).reshape(1, -1)

    all_games = GameModel.objects.exclude(id=target_game.id)

    similarities = []

    for game in all_games:
        if not game.embedding:
            continue

        game_vector = np.array(game.embedding).reshape(1, -1)

        score = cosine_similarity(target_vector, game_vector)[0][0]
        similarities.append((game, score))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return [game for game, score in similarities[:top_n]]

def recommend_for_user(user, GameModel, LibraryModel, top_n=6):

    owned = LibraryModel.objects.filter(user=user)

    if not owned.exists():
        return []

    owned_vectors = []

    for item in owned:
        if item.game.embedding:
            owned_vectors.append(np.array(item.game.embedding))

    if not owned_vectors:
        return []

    user_vector = np.mean(owned_vectors, axis=0).reshape(1, -1)

    recommendations = []

    for game in GameModel.objects.all():

        if owned.filter(game=game).exists():
            continue

        if not game.embedding:
            continue

        game_vector = np.array(game.embedding).reshape(1, -1)

        score = cosine_similarity(user_vector, game_vector)[0][0]
        recommendations.append((game, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return [game for game, score in recommendations[:top_n]]

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

    if vectorizer is None:
        generate_embeddings_for_all_games(GameModel)

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, game_vectors)[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    top_ids = [game_ids[i] for i in top_indices]

    return GameModel.objects.filter(id__in=top_ids)