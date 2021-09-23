# Experiment setup
> This document outlines the experimental procedure of this project.

## Materials
* Computer + experiment software
* Display
* Keyboard

## Participants
We are looking for participants, possibly students, that are open to learn a new language: Swahili.
To this end, the participants may not be familiar with the Swahili language as to have a similar common knowledge of the language prior to the experiment.

## Method
Each participant will be selected to a group. We define three groups:
1. The control group; No colour palette
2. Condition 1 group; Colour palette based on difficulty of the word
3. Condition 2 group; Different colour per word

Each participant will receive a briefing prior to the experiment. All briefings will start with the standard briefing.

In this briefing the participants are informed that in this experiment the participant will be learning the Swahili language, from the English language.
I.e. each participant will be presented with an English word and is tasked to provide the Swahili translation of this word _???_.

Based on their group, each participant may then follow a different procedure.

### Discovery phase
In the discovery phase each participant will get to know the words in the vocabulary. Concretely, each Swahili word will in turn be presented together with it's English counterpart.
The participant is then tasked to retype the _Swahili???_ word to confirm he or she has read the word.

Then based on the group the participant is placed in, the participant will be presented with the words in different ways:
1. Both words are presented in the center of the screen in black text on a white background, with an input field located below.  
2. The same layout is used as for group 1, however the fields of interested are now placed in a white square, while all remaining background is coloured by the colour chosen to be the medium difficulty colour based on the difficulty colour palette.
3. Group 3 on its turn uses the same layout as group 2, however now the background will change to the colour assigned to each word respectively.

### Learning phase
Once the participant has seen each word once, the learning phase starts.
The learning phase will stop whenever 15 minutes have passed and the participant has completed the last word he or she is dealing with. 
The participants will not be actively presented with the time they have left, as to avoid stress thereof _(maybe we even want to go further to remove all notices of time from the room and participant)_.

During the learning phase the participant will learn the new vocabulary. All English words from the vocabulary are in turn presented to the participant, their occurence and repetition determined by the model by Sense et al. (2016).
During each turn the participant is tasked to produce the Swahili translation, for which he or she has **60???** seconds.

There are two situations:
1. The participant produces the correct translation _(obvious spelling errors are also considered as correct translation)???_. 
In this case a text with 'Correct!' is displayed for _1 second???_, before the next English word is displayed.
2. The participant failes to produce the correct translation. This can be either due to giving the wrong input, or through timeout.
In this case the word 'Incorrect' is displayed for _1 second???_, before the correct translation is displayed. 
>??? now we need to decide wether the correct translation is displayed for _n_ seconds before displaying the next word, or whether we want to show the correct translation untill the user has typed in the correct translation (will take more time probably, but speed up learning?).

How the words are displayed once again depends on the group the participant is played in:
1. Same layout as during the discovery phase, however obviously now the Swahili word is hidden.
2. Same layout as during the discovery phase, with the Swahili word hidden. However, whenever a new word is displayed, the background changes to a new colour from the difficulty colour palette corresponding to the difficulty of the word to the participant as estimated by the system.
3. Same layout as during the discovery phase, with the Swahili word hidden.

### Evaluation phase
>??? Here we have to determine whether we want to do the same as in Van den Broek et al. (2019) and do evaluation like one week after discovery and learning.
The evaluation phase is held some time after the learning phase, as to assure that the participants actually learned the words, rather than remembering it in their short-term memory.

The start of the evaluation phase will be equal for each participant, regardless of the group they were in during the discovery and learning phase:

All English words from the vocabulary are presented one time on turn to the participant. Once again the participant has _60 seconds???_ to give the correct answer.
This means that the participant may encounter words that have only been seen during the discovery phase. The system will keep track of this variable, for correction during later data analysis.
Whenever input is submitted, the next word is displayed without feedback to the user whether the past input was correct or not, though whether the input was correct is being logged by the system.

>??? Here we have to determine whether we want to keep the ordering of the words equal for each participant, or whether we want to shuffle the words, this especially will be important when we do the double evaluation phases.

Whenever the participant has answered two-thirds of the vocabulary, _(maybe with a short break in between???)_ the layout used during the learning phase will be employed again.
Group 1 will see no change, group 2 and 3 will have each word presented with a coloured background respective to their group. 
For group 2 this means that the background colour for each word will be equal to the colour associated with the last difficulty measure of the system for that respective word.

For clarification, feedback about the correctness of the input is still omitted. Once again the accuracy of the user is being logged.

> ??? We could even do one type of evaluation per third of the vocab, to do some nice cross comparison between the groups.

After the participants are finished, they may see their scores if they are interested. 
After that they will have to fill in a short survey about the experiment, after which they are thanked and free to go.

## Data analysis
> ??? TODO

