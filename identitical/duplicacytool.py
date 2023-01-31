from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def get_similar(data,index=False):
    stop_words = set(stopwords.words("english"))
    question_types = {"pickOne", "pickMulti", "switch", "slider", "rank"} if not index else set()
    data = {str(x["_id"]["$oid"]):x["question"] for x in data if x["questionType"] in question_types or index}
    processed_data = [" ".join(w for w in word_tokenize(x) if w not in stop_words) for x in data.values()]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed_data)
    similarities = cosine_similarity(vectors)
    ques,similar_idx = {},{}
    for i in range(len(similarities)):
        idx = [k for j,k in zip(range(len(similarities[i])),data.keys()) if similarities[i][j] > 0.75]
        if len(idx) > 1:
            similar_idx[idx[0]] = idx[1:]
            ques[data[idx[0]]] = {"count": len(idx), "similar": [data[x] for x in idx[1:]]}
    if index:
        return similar_idx
    return ques