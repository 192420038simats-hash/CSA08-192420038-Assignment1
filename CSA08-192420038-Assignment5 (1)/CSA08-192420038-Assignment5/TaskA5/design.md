# Task A5 – Design an AI Application for Citizen Complaints (K3)

**Files:** `TaskA5/design.md`, `chatbot.py`; the scorer and summariser are in `TaskB4/sentiment.py`.

## A5.1 Sentiment scorer and summariser
**Lexicon sentiment with negation – pseudocode**
```
ALGORITHM Score(text, window)
  CONSTANTS POSITIVE (words such as good, clean, fast, helpful), NEGATIVE (bad, dirty, smoke, broken, ...), NEGATORS (not, never, no, cannot, ...)
1  words <- lower-case words of text;  total <- 0
2  FOR i <- 0 TO LENGTH(words) - 1 DO
3      IF words[i] IN POSITIVE THEN value <- +1  ELSE IF words[i] IN NEGATIVE THEN value <- -1  ELSE value <- 0
4      IF value <> 0 AND any of the previous `window` words IS IN NEGATORS THEN value <- -value
5      total <- total + value
6  IF total > 0 THEN RETURN "positive"  ELSE IF total < 0 THEN RETURN "negative"  ELSE RETURN "neutral"
```
`window = 1` flips a word only when the negator is directly before it ("not good"); `window = 2` also handles "not very good". The word lists are sets, so each look-up is O(1) and the whole text is O(words).

**Extractive summariser – pseudocode**
```
ALGORITHM Summarise(text, k)
1  sentences <- split text at . ! ?;   IF LENGTH(sentences) <= k THEN RETURN text
2  freq <- empty dictionary
3  FOR EACH word IN text DO  IF word is not a stop word AND LENGTH(word) > 2 THEN freq[word] <- freq[word] + 1
4  FOR EACH sentence DO  score <- sum of freq[word] for the words of the sentence
5  best <- the k sentences with the highest score (ties: the earlier sentence)
6  RETURN best in their original order
```
Important words are the non-stop words; a word that the citizen repeats is probably the topic, so the sentence that holds the most frequent words is the one that says what the complaint is about.

## A5.2 Rule-based chatbot
```
ALGORITHM Reply(question)
1  stations <- stations named in the question (exact name, otherwise closest spelling)
2  IF question contains "help" THEN RETURN the list of things the bot can do
3  IF question contains "worst" / "most polluted" THEN QUERY the station with the highest mean on the latest day;  RETURN it
4  IF question contains "best" / "cleanest" THEN (the same with the lowest)
5  IF question contains "compare" AND two stations THEN QUERY both;  RETURN them
6  IF question contains "pm2.5" / "air" / "pollution" THEN
7      IF no station THEN RETURN "Which station do you mean?"
8      IF question contains "average" / "month" THEN QUERY the station's mean ELSE QUERY the latest day's mean
9      RETURN the number with the quality band (good ... severe)
10 RETURN "I did not understand"
```
All database access uses `?` placeholders. "Today" means the latest day stored. Conversation of `chatbot.py`:
```text
(database: latest day = 2026-10-31)

user : What is the PM2.5 in Adyar today?
bot  : The mean PM2.5 at Adyar on 2026-10-31 is 48.0 ug/m3 - satisfactory.

user : pm25 in guindy
bot  : The mean PM2.5 at Guindy on 2026-10-31 is 71.6 ug/m3 - moderate.

user : What is the average PM2.5 at Manali this month?
bot  : The average PM2.5 at Manali over the stored month is 118.3 ug/m3 (poor).

user : How is the air in Adyr?
bot  : The mean PM2.5 at Adyar on 2026-10-31 is 48.0 ug/m3 - satisfactory.

user : Which is the most polluted station today?
bot  : The most polluted station on 2026-10-31 is Manali with a mean PM2.5 of 120.6 ug/m3 (very poor).

user : compare Adyar and Manali pm2.5
bot  : Mean PM2.5 on 2026-10-31 (ug/m3) - Adyar: 48.0, Manali: 120.6.

user : What is the PM2.5 in Mumbai today?
bot  : Which station do you mean? Try: 'What is the PM2.5 in Adyar today?'

user : Is the air clean in Adyar or not?
bot  : The mean PM2.5 at Adyar on 2026-10-31 is 48.0 ug/m3 - satisfactory.

user : Will it rain tomorrow?
bot  : Sorry, I did not understand. Type 'help' to see what I can answer.

user : PM2.5 in Adyar DROP TABLE readings; --
bot  : The mean PM2.5 at Adyar on 2026-10-31 is 48.0 ug/m3 - satisfactory.

user : help
bot  : I can tell you the PM2.5 of a station today, its monthly average, the most or least polluted station, or list the stations.

readings table still has 8912 rows
```

**Limitations:** (1) only keywords – "Is the air clean in Adyar *or not*?" is answered with a number and not understood; (2) no memory of the conversation ("and in Guindy?" fails); (3) only fixed intents, a question outside them gets a refusal; (4) spelling help is limited (`Adyr` works, a different name or Tamil text does not); (5) it cannot say *why* the air is bad or forecast; (6) a station that is not in the network ("Mumbai") is confused with a missing station name; (7) several keywords in one question are resolved by a fixed order of rules; (8) the answer is only as correct as the data and the day it reports; (9) English only.

## Alternative – a trained machine-learning model instead of a word list
```
Training (offline):   FOR EACH labelled complaint: count the words per class  ->  log-probabilities of every word given the class
Prediction:           score(class) <- log prior(class) + sum of log P(word | class);  RETURN the class with the highest score
```
It needs **labelled data** (hundreds to thousands of complaints with positive/negative/neutral marked by a person), a vectoriser and a library (scikit-learn); a pre-trained language model would need much more memory and a GPU or an API. Compared on the 64 complaints that I labelled by hand (52 + 12 new ones, `naive_bayes_compare.py` in Task B4; leave-one-out test, so the model never sees the complaint it is asked about):

| | Word list | Naive Bayes (trained) |
|---|---|---|
| Accuracy on 64 complaints | 92.2 % (but 52 were read while choosing the words) | 70.3 % (only 63 training examples) |
| Time per complaint | 6.2 µs | 9.2 µs in a batch; 69 µs one at a time |
| Memory | 60 words = 2.4 KiB | vocabulary 410 words: 9.6 KiB of numbers + 13 KiB dictionary; for 41,827 words 1.0 MB + 1.0 MB; 72,425 words 1.7 MB + 1.9 MB |

Time and memory of both are small (O(words) per complaint; the model needs O(vocabulary × classes) memory, which grows with the data). The real difference is **accuracy and effort**: with 63 examples the trained model is clearly worse; it would improve with thousands of labelled complaints and would then learn words and phrases I did not list (and would handle spelling and Tamil-English mixing if trained on such data), but it needs labelling work, retraining and monitoring. The word list needs no training and every decision can be explained.
