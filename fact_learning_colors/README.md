# Fact Learning with Adaptive Color Palette: Effect of Stimuli-Independent Hints

See for more detail:
- [Experiment setup](meta/experiment_setup.md)
- [Data](meta/data.md)
- [User briefing](meta/briefing.md)

## Introduction & motivation

This user model application focuses on enhancing learning a foreign vocabulary. It has been shown that changing the repetition times of a certain word depending on its difficulty to the user, decreases the time it takes for the user to learn the foreign vocabulary (Sense et al., 2016 <sup>[3](#fn3)</sup>). On the other hand, many studies have been performed on the influence of colour on our everyday life. One major finding is the effect of colour on learning and making fast associations (many signs include colour, warning signs are usually red, etc.), Chang et al., 2018 <sup>[4](#fn4)</sup>. 

Based on these findings, this user model study aims to determine whether employing colour allows the user to learn a foreign vocabulary faster. More specifically, derived from the aforementioned methods to change the repetition time of words depending on the difficulty of the word to the user, this user model will change its background colour based on the difficulty to the user.

In detail, this means that prior to the study process a colour palette will be selected for every participant. This colour palette associates a different colour to different degrees of difficulty _(refer to the next sections for the method to select this colour palette)_. Each time a word is displayed, the background will changes to the colour from the colour palette that represents the difficulty the user model estimates the user is currently having with the word in question.

### Related Work

Van den Broek (2019) <sup>[1](#fn1)</sup> show that providing hints surprisingly does not have a long-lasting effect on later recall in fact-learning when the hints were not present.
A key difference is, however, that the hints used in their study were relevant to prompt (e.g. translating _vestis - clothes_: _Think of the word "vest"_).
Additionally, the hints were shown after the user response for a second chance.
In the case of our experiment, these "prompt context-independent" hints are shown before the prompt is answered.
In an extreme case, this may lead to even worse later recall results because the user could associate the answer with the specific colour (see [evaluation](#evaluation)) and not with the actual prompt.

## User-model & interface

Our model is based on the [spacing model used by SlimStampen](https://github.com/VanRijnLab/user-models-2122). To include the colour palette system in the model, we modify the background colour as the user is learning. The colours for each fact change according to how easy for the user to remember the fact. In the spacing model, the _rate of forgetting_ shows an estimated rate for a fact at a specified time, which could measure how difficult to remember the fact for the user. The colour palette from the easiest to the hardest scale should change in the proportion of the forgetting rate.


<!--All the figures are drawn with OpenSesame (Mathôt et al., 2012 <sup>[2](#fn2)</sup>) sketchpad item. -->

Examples of screens during the discovery phase (possibly also learning, once the user fills in the word).

group | easy | medium | hard   
:-:|:---:|:---:|:---:
C0 | ![easy](./meta/img/sketch_p0.png) | ![medium](./meta/img/sketch_p0.png) | ![hard](./meta/img/sketch_p0.png)
C1 | ![easy](./meta/img/sketch_p1_easy.png) | ![medium](./meta/img/sketch_p1_medium.png) | ![hard](./meta/img/sketch_p1_hard.png)
C2 | ![easy](./meta/img/sketch_p2.png) | ![medium](./meta/img/sketch_p2.png) | ![hard](./meta/img/sketch_p2.png)

## Experiments setup

Refer for a more detailed explanation to our [experiment setup](https://github.com/zouharvi/user-models/blob/main/meta/experiment_setup.md).

There is one factor which we test between-subject, palette presence (3 conditions).
We also measure testing in two modes: without and with color cues (same as in the learning phase).

### Pre-Experiment

In a pre-experiment, we will poll the participants on what colour palette they associate the most with the easy-difficulty scale.
If the results are heavily in favour of one specific palette (we expect green-red), we use this one.
In case of more balanced results, we will offer this selection to the users in C1.

Three palettes:

![palettes](./meta/img/palette.png)

### Palette Presence

The experiment will be based on learning words from English to a foreign language, most probably Swahili.
We need 3 contrastive groups:
- C0: no colour palette
- C1: colour based on a difficulty via ACT-R
- C2: word colours chosen randomly

<!--

Vilém thinks the last level is needed to contrast the following phenomenon: 
If a word is for a longer time in e.g. bright red colour, I can associate this with the answer (similar to my *star* example).
In order to rule out that this phenomenon is positively influencing the results (and not the palette), we would need the fourth group of people.

-->

### Evaluation

In order to determine the exact effect of the adaptive palette, the evaluation for users is yet another factor.
- PT0: evaluation without any colour cues
- PT1: evaluation with the same scheme as the original configuration (e.g. C1A2)

### Scale

17 participants were enlisted in total and each was assignment a condition (between-subject).

## Data analysis & hypothesis

Observations regarding the performance (number of words correctly translated or number of words learned) of the participants are noted.
These observations are statistically examined with respect to the experiment conditions.

### Expectations

With the assumption that our hypothesis holds, we expect to see a higher performance among participants in the adaptive colour palette condition with their own selection.
The random colour palette should show a significantly lower performance among subjects, similar to no palette (though higher in E1 because of additional hints).
This would indicate that the perception (user-defined) of a colour with a certain level of hardness allows the participant to scale their focus to match these and hence learn faster.
A similar performance in this group to the non-adaptive colour palette group indicates that the colours do not serve merely as context cues with one to one relationships among colours and words. 
A colour that we associate with hardness will tend to cue us on paying extra attention to the learning process.
These cues will further help the learner pace their focus in relation to the context.
We believe that E1 will have better performance than E0 because of similar reasons to those proposed by Van den Broek (2019).

### Research questions

- Does the perception of colours with a level of hardness serve as cues for distributing focus across tasks in learning better?
  - We compare groups in the first factor (C0, C1, C2)
- Can learning with non-contextual cues actually be hurtful?
  - I.e. C1E1 > C0 > C1E0 and C2E1 > C0 > C2E0 ?
- Is the performance gain because of the dynamic palette or because of random color associations?
  - I.e. C1 <> C2 ?
<!-- - 
- Is there a prominent global colour palette associated with the different levels of difficulty?
  - Which of the palettes is preferred (we expect imbalanced distribution)
  - Across the first two factors (P-A), does any lead to the best results as evaluated by either E0 or E1
-->

## References

<a name="fn1">1</a>: Van den Broek, G. S., Segers, E., Van Rijn, H., Takashima, A., & Verhoeven, L. (2019). Effects of elaborate feedback during practice tests: Costs and benefits of retrieval prompts. Journal of Experimental Psychology: Applied, 25(4), 588.  
<a name="fn2">2</a>: Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. Behavior Research Methods, 44(2), 314-324.  
<a name="fn3">3</a>: Sense, F., Behrens, F., Meijer, R. R., & van Rijn, H. (2016). An individual's rate of forgetting is stable over time but differs across materials. Topics in cognitive science, 8(1), 305-321.  
<a name="fn4">4</a>: Chang, B., Xu, R., & Watt, T. (2018). The impact of colors on learning.  

## Misc.
<!-- - ramp-up problem Konstan et al 1998 (prior 0.3) -->
- Do not use non-ASCII characters when running the OpenSesame experiment
