- Task: Predicting translation/post-editing time/difficulty
- User perspective: user wants to learn to translate from one language to another one (whole sentences).
- In professional setting this is usually done on the level of sentences which are however taken from whole documents.

- Our part would be to predict the future difficulty
- - Based on sentence properties in combination with the specific user history
- - For correct/incorrect answers we could use reference translations with automatic metrics or self-evaluation (both is doable)
- This is very applicable to MT industry where estimation of future cost is very vital (asked professional colleagues and they find it interesting)
- Presentation lists: _Improve the user model’s response time predictions_ which is directly this

The experiments could be done as follows:

- We collect translations of `N` documents from `M` users (can be various languages, the direction can mostly be English->Native language, as is common)
- We get `N*M` samples (in a time sequence). We take the first (N-k) documents from every person and then compare our predictions with that of the users.
- We can do predictions on whole document size and on sentence-level (i.e. How long will it take me to translate this document on this topic given my history?)
- This could also have a cross-linguistic aspect but lets not go into that right now.
- I asked a colleague for his opinion on this. :-)

Cons:
- Translation time has a lot of variance and great number of outliers
- Standard approaches can't be applied because no repetition (hence no activation), this can also be a good thing
- Not really learning of the users but of the system

Pros:
- Super interesting (for me at least)
- I know a journal where we could publish both positive and/ror negative results
- Highly applicatble
