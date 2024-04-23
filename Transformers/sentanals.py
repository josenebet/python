from transformers import pipeline
'''classifier = pipeline('sentiment-analysis')
res=classifier('We are very happy to introduce pipeline to the transformers repository.')
print(res)'''

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

res=distilled_student_sentiment_classifier ("Me encanto esta pelicula la volveria a ver otra vez")
print(res)