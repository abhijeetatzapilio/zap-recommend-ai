#data modeling

import json,random
from bson import json_util
from config.config import mongo
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from identitical.duplicacytool import get_similar

def get_questions(data):
    stop_words = set(stopwords.words("english"))
    if data["level"]=="Entry":
        level={"$or":[{"level":"Easy"},{"level":"Intermediate"}]}
    elif data["level"] in ("Experienced","Expert"):
        level = {"$or": [{"level": "Hard"}, {"level": "Intermediate"}]}
    else:
        level={}
    skill_vectorizer = TfidfVectorizer()
    db_data=json.loads(json_util.dumps(mongo.db.questions.find(level)))
    similar_idx=get_similar(db_data,index=True)
    db=[x for x in db_data if "skill" in x]
    db_skills={str(x["_id"]["$oid"]):" ".join(w for w in word_tokenize(x["skill"]) if w not in stop_words) for x in db if x["skill"]}
    db_skills_vectors = skill_vectorizer.fit_transform(list(db_skills.values()))
    ques={"data":[],"message":"Data not found","percent":{"easy":0.0,"intermediate":0.0,"hard":0.0}}
    for i in data["skills"]:
        data_skill=[" ".join(w for w in word_tokenize(i) if w not in stop_words)]
        data_skill_vector=skill_vectorizer.transform(data_skill)
        skill_cosine=list(map(lambda x:cosine_similarity(data_skill_vector,x),db_skills_vectors))
        idx=[y for x,y in zip(skill_cosine,db_skills.keys()) if x[0][0]>0.75]
        for k in similar_idx:
            if k in idx:
                idx=list(set(idx).difference(similar_idx[k]))
        ques_data=[x for x in db if str(x["_id"]["$oid"]) in idx]
        try:
            ques["data"].extend(random.sample(ques_data,data["skills"][i]*(2 if data["skills"][i]!=1 else 4)))
        except:
            ques["data"].extend(ques_data)
    try:
        ques["percent"]["easy"] = round((len([x for x in ques["data"] if x["level"] == "Easy"]) / len(ques["data"])) * 100,2)
        ques["percent"]["intermediate"] = round((len([x for x in ques["data"] if x["level"] == "Intermediate"]) / len(ques["data"])) * 100,2)
        ques["percent"]["hard"] = round((len([x for x in ques["data"] if x["level"] == "Hard"]) / len(ques["data"])) * 100,2)
        ques["message"]="Success"
    except ZeroDivisionError:
        pass
    return ques