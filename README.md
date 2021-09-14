# Learning Foreign Language Vocabulary with Adaptive Color Palette (WIP)

## Introduction / motivation
_Leander_
This user model focuses on enhancing learning a foreign vocabulary. While other user models with similar purpose focus on differing the repetition time between words based on their difficulty for the user, this model uses color instead. 
During the learning process each word is accompanied by a certain color. This color changed based on the difficulty of the word for the user. 


## User model / interface

Our model will base on the [spacing model used in the SlimStampen](https://github.com/VanRijnLab/user-models-2122). To include the color palette system in the model, we have to modify the background color as the users learning. The colors for each fact change according to how easy for the user to remember the fact. In the spacing model, the `rate of forgetting` shows an estimated rate for a fact at a specified time, which could measure how difficult to remember the fact for the user. The color palette from the easiest to the hardest scale should change in the proportion of the forgetting rate. 

## Experiments setup

There are two factors: palette presence (4) and palette adaptavity (2) which is almost 4x2 design though no adaptavity is needed for _no color palette_ and _word colors chosen randomly_.
Overall this results in 6 conditions.

### Palette Presence

The experiment will be based on learning words from English to a foreign language, most probably Swahili.
We need 3 contrastive groups:
- G0: no color palette
- G1: color palette chosen by the user
- G2: color palette chosen randomly
- G3: word colors chosen randomly

Vilém thinks the last group is needed to contrast the following phenomenon: 
If a word is for a longer time in e.g. brigh red color, I can associate this with the answer (similar to my *star* example).
In order to rule out that this phenomenon is positively influencing the results (and not the palette), we would need the fourth group of people.

### Adaptivity

Another factor would be the palette working scheme.
Is the palette with a fixed threshold or is it adapted to the current user progress?
- Fixed: 0 incorrect - white, 1-2 incorrect - pink, 3+ incorrect - red
- Adaptive: 20% easiest - white, 20%-50% easiest - pink, 50%-100% easiest (harderst) - red

### Scale

The exact scale is yet to be determined (number words, sessions and people).
Since we have 6 groups, we may need e.g. 12 people to get 2 people per condition, and possibly more. 
Depending on whether we accept adaptivity as another factor, that increases the amount of conditions.
Naturally we will be using between-subject design because we can not change the configuration for someone mid-experiment.

## Data analysis / hypothesis
We hypothesize that colours have an impact on the learning process. For example, a colour that we associate with hardness will tend to cue us on paying extra attention to the learning process. These cues will further help the learner pace their focus in relation to the context. We further hope to investigate the experimental results in determining if certain palettes are globally identified with a certain level of hardness. These findings may enable us in building a UI that makes fact learning more efficient.

