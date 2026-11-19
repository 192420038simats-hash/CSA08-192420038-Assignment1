"""A5 / B4 alternative: a trained model (multinomial Naive Bayes, scikit-learn) instead of a word list.
Accuracy is measured by leave-one-out cross-validation on the 52 + 12 hand-labelled complaints (tiny data!);
time and memory are measured on the real sizes and on a large synthetic training set."""
import random, sys, time
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from complaints import COMPLAINTS
from holdout import HOLDOUT
from sentiment import label

data = COMPLAINTS + HOLDOUT
X, y = [t for t, _, _ in data], [g for _, g, _ in data]
model = make_pipeline(CountVectorizer(), MultinomialNB())
pred = cross_val_predict(model, X, y, cv=LeaveOneOut())
acc_nb = np.mean([p == g for p, g in zip(pred, y)])
acc_lex = np.mean([label(t) == g for t, g in zip(X, y)])
print(f"{len(data)} labelled complaints")
print(f"  Naive Bayes, leave-one-out accuracy : {acc_nb:.1%}   (trained on 63 complaints at a time)")
print(f"  word list (window 1) accuracy       : {acc_lex:.1%}   (no training; list written while reading 52 of them)")
for g in ("positive", "negative", "neutral"):
    idx = [i for i, v in enumerate(y) if v == g]
    print(f"    {g:<9} recall: Naive Bayes {np.mean([pred[i] == g for i in idx]):.0%}   word list {np.mean([label(X[i]) == g for i in idx]):.0%}")

model.fit(X, y)
texts = X * 800                                              # 51,200 complaints
t0 = time.perf_counter(); model.predict(texts); t_nb = (time.perf_counter() - t0) / len(texts) * 1e6
t0 = time.perf_counter(); [label(t) for t in texts]; t_lex = (time.perf_counter() - t0) / len(texts) * 1e6
t0 = time.perf_counter()
for t in X[:200]: model.predict([t])
t_one = (time.perf_counter() - t0) / 200 * 1e6
print(f"\nTime per complaint: word list {t_lex:.1f} us | Naive Bayes in a batch of 51,200 {t_nb:.1f} us | Naive Bayes one at a time {t_one:.0f} us")

cv, nb = model.steps[0][1], model.steps[1][1]
print(f"\nMemory of the trained model (vocabulary {len(cv.vocabulary_)} words): "
      f"{(nb.feature_log_prob_.nbytes + nb.class_log_prior_.nbytes) / 1024:.1f} KiB of numbers + the vocabulary dictionary {sys.getsizeof(cv.vocabulary_) / 1024:.0f} KiB")
rnd = random.Random(1)
for vocab in (5_000, 50_000, 200_000):
    words = [f"w{i}" for i in range(vocab)]
    docs = [" ".join(rnd.choices(words, k=30)) for _ in range(3000)]
    labels = [rnd.choice(["positive", "negative", "neutral"]) for _ in docs]
    m = make_pipeline(CountVectorizer(), MultinomialNB()).fit(docs, labels)
    c, n = m.steps[0][1], m.steps[1][1]
    print(f"  vocabulary of {len(c.vocabulary_):>7,} words (synthetic): model arrays {n.feature_log_prob_.nbytes / 1e6:>6.2f} MB, vocabulary dict {sys.getsizeof(c.vocabulary_) / 1e6:>6.2f} MB")
print(f"word list in memory: {len(__import__('sentiment').POSITIVE) + len(__import__('sentiment').NEGATIVE) + len(__import__('sentiment').NEGATORS)} words, "
      f"{(sys.getsizeof(__import__('sentiment').POSITIVE) + sys.getsizeof(__import__('sentiment').NEGATIVE)) / 1024:.1f} KiB")
