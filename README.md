# Learning Foreign Language Vocabulary with Adaptive Color Palette (WIP)

## Introduction & motivation

This user model application focuses on enhancing learning a foreign vocabulary. It has been shown that changing the repetition times of a certain word depending on its difficulty to the user, decreases the time it takes for the user to learn the foreign vocabulary (TODO: cite -V.). On the other hand, many studies have been performed on the influence of colour on our everyday life. One major finding is the effect of colour on learning and making fast associations (many signs include colour, warning signs are usually red, etc.). 

Based on these findings, this user model study aims to determine whether employing colour allows the user to learn a foreign vocabulary faster. More specifically, derived from the aforementioned methods to change the repetition time of words depending on the difficulty of the word to the user, this user model will change its background colour based on the difficulty to the user.

In detail, this means that prior to the study process a colour palette will be selected for every participant. This colour palette associates a different colour to different degrees of difficulty _(refer to the next sections for the method to select this colour palette)_. Each time a word is displayed, the background wil changes to the colour from the colour palette that represents the difficulty the user model estimates the user is currently having with the word in question.


## User-model & interface

Our model is based on the [spacing model used by SlimStampen](https://github.com/VanRijnLab/user-models-2122). To include the colour palette system in the model, we modify the background colour as the user is learning. The colours for each fact change according to how easy for the user to remember the fact. In the spacing model, the _rate of forgetting_ shows an estimated rate for a fact at a specified time, which could measure how difficult to remember the fact for the user. The colour palette from the easiest to the hardest scale should change in the proportion of the forgetting rate.

TODO: would it be possible to add a sketch of what the interface will look like with the palettes? Like something simple in Inkscape (+ please push the source here) -V.

## Experiments setup

There are two factors: palette presence (4) and palette adaptivity (2) which is almost a 4x2 design though no adaptivity is needed for _no colour palette_ and _word colours chosen randomly_.
Overall this results in 6 conditions.

### Palette Presence

The experiment will be based on learning words from English to a foreign language, most probably Swahili.
We need 3 contrastive groups:
- P0: no colour palette
- P1: colour palette chosen by the user
- P2: colour palette chosen randomly
- P3: word colours chosen randomly

Vilém thinks the last group is needed to contrast the following phenomenon: 
If a word is for a longer time in e.g. bright red colour, I can associate this with the answer (similar to my *star* example).
In order to rule out that this phenomenon is positively influencing the results (and not the palette), we would need the fourth group of people.

### Adaptivity

Another factor would be the palette working scheme.
Is the palette with a fixed threshold or is it adapted to the current user progress?
- A0: 0 incorrect - white, 1-2 incorrect - pink, 3+ incorrect - red
- A1: 20% easiest - white, 20%-50% easiest - pink, 50%-100% easiest (harderst) - red

### Scale

The exact scale is yet to be determined (number words, sessions and people).
Since we have 6 groups, we may need e.g. 12 people to get 2 people per condition, and possibly more. 
Depending on whether we accept adaptivity as another factor, that increases the number of conditions.
Naturally, we will be using between-subject design because we can not change the configuration for someone mid-experiment.

## Data analysis & hypothesis
We hypothesize that colours have an impact on the learning process. For example, a colour that we associate with hardness will tend to cue us on paying extra attention to the learning process. These cues will further help the learner pace their focus in relation to the context. We further hope to investigate the experimental results in determining if certain palettes are globally identified with a certain level of hardness. These findings may enable us in building a UI that makes fact learning more efficient.

TODO: specific research questions, ideally a list -V.
