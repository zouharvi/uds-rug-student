# A simplified version for the [translation](https://github.com/zouharvi/user-models/blob/main/drafts/translation.md) (?)

+ Reasons: Sentences translations are normally N to N mapping. In our case when it's English -> other languages, there might be many possible correct answers(some of them could even be equally good). Although it is possible to use metrics and get the distance with baseline translation, there might be a lot of other parameters hard to control/model (e.g. the mean reaction time for different participants/different types of sentences may not be in the same difficulty level/ etc.).

+ To reduce the prediction from sentences -> paragraph to words -> sentence level might be easier to manipulate and connect to the parameters we want to get from the users.

+ Also it would be possible to include eye-tracking and pupil size besides reaction time as [attention](https://github.com/zouharvi/user-models/blob/main/drafts/attention.md) indicates, since the eye-movement will not have that much diversity when it's in words level.

+ To stay in the scope of fact-learning(though it's not that strict?), the translation idea seems to assume the participants are familiar with translation English -> other languages. But if it is in the word level, it is possible to get word pairs(which could be one-to-one mapping) and give them to naive participants to learn, then we could get the whole learning process to predict the sentence level. In this way, the diversity won't be so variance since they all learn from the very beginning without related knowledge.
 
