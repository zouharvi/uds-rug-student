# Experiment setup
This document outlines the main experimental procedure.
The requirements for this experiment are an internet-connected computer and the experiment software.
The overall estimated duration of the experiment is 30-40 minutes.

## Participants

The participants are required to not have any prior knowledge of Swahili or related languages, to not suffer from any learning disabilities nor colour-blindness.
We expect the volunteers to be international students.
They will be assigned to one of the three groups uniformly.

## Method

Each participant will be selected into a group. We define three groups:
- C0: No colour palette
- C1: Colour palette based on the difficulty of the word
- C2: Different colours per word

Each participant will receive a briefing document prior to the experiment where they are told what the main task is (learning Swahili vocabulary) and the outline of the experiment.
They will also be told what the color codes in their example.
Importantly, they will not be disclosed information about other groups.

There will be possibly unlimited words words in total (see [Data](data.md)).
This is because we don't expect any user to see all the words because it's constrained by the SlimStampen providing them.

## Outline

The whole experiment can be split into the following two phases which follow in sequential order:

1. PL: Learning
2. PT: Testing

There is no explicit discovery phase.
When it's time to introduce a new word, the participant gets a study trial where one is given the answer and has to type in the answer.

The participants will fill in a questionnaire at the beginning of the experiment and at the end.
The reason for not joining them is because of the expected mental fatigue after the experiment is concluded.

### Learning phase

The participants will not be actively presented with the time they have left, to avoid a potential increase in stress.

During the learning phase, the participant will learn the new vocabulary.
All Swahili words from the vocabulary are in turn presented to the participant, their occurrence and repetition determined by the model by Sense et al. (2016).
During each turn, the participant is tasked to produce the English translation with the time limit of 60 seconds (they are not expected to reach this though).

There are two situations:
- The participant produces the correct translation.
  In this case, a positive message (e.g. _Correct!_) is displayed until the participant presses Enter to display the next word.
  - Small spelling mistakes, based on the Levenshtein distance, are accepted as correct
- The participant fails to produce the correct translation.
  In this case, a negative message (e.g. _Incorrect_) is displayed together with the correct translation.
  - The participant is not forced to type the correct answer.
  
The learning phase will stop whenever 20 minutes have passed regardless of how many words were processed by the participant.

### Evaluation phase

The evaluation phase is held after 5-10 minutes after the last learning phase, to assure that the participants actually learned the words, rather than remembering them in their short-term memory.
We will provide a filler task in-between, such as a game.
This filler task has to be checked to make sure that the user is actively engaged.

This phase is further split into two subphases:

#### PT0

All Swahili words from the vocabulary are presented one time in turn to the participant who has unlimited time to provide the correct answer.
Whenever the input is submitted, the next word is displayed without feedback to the user whether the past input was correct or not.
Some of the participants may encounter words that have only been seen during the discovery phase.
However, the learning phase duration will be finetuned to minimize the number of such participants.

Importantly, all the words are presented without the colours.

#### PT1

In the second part of testing, all the Swahili words are presented again, but for groups C1 and C2, the colours are activated again.
For C2 the associated colours will be used while for C1, the last difficulty estimate from the learning phase will be used.
The ordering for both tests is fixed and only the words which were learned are tested.
The feedback is still omitted though it may be present at the end of the experiment for a small morale boost.

## Design

The design base is black text on a white background in the centre of the screen with an input field below the English word. 

Based on the group the participant is placed in, the words will be presented either as:
- P0: white background, 
- P1: the word background is highlighted by the colour corresponding to the difficulty
- P2: the word is presented with its associated colour

The discovery and learning phase will contain these colourings though, for testing, it will depend on the specific subphase.
It will be disabled in PT0 and enabled in PT1.
