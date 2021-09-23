# Experiment setup
This document outlines the main experimental procedure.
The requirements for this experiment are an internet-connected computer and the experiment software.
The overall estimated duration of the experiment is TODO minutes.

## Participants

The participants are required to not have any prior knowledge of Swahili or related languages, to not suffer from any learning disabilities nor colour-blindness.
We expect the volunteers to be international students.
They will be assigned to one of the three groups uniformly.

## Method

Each participant will be selected into a group. We define three groups:
- C0: No colour palette
- C1: Colour palette based on the difficulty of the word
- C2: Different colours per word

Each participant will receive a briefing document prior to the experiment where they are told what the main task is (learning Swahili vocabulary).
Importantly, they will not be disclosed in which group they are.

## Outline
The whole experiment can be split into the following phases which follow in sequential order:

1. PD: Discovery
2. PL: Learning
3. PT: Testing

TODO: PD, PL, PL, PL, PT0, PT1? How many learning phases?

The participants will fill in a questionnaire at the beginning of the experiment and at the end.
The reason for not joining them is because of the expected mental fatigue after the experiment is concluded.

### Discovery phase

In this phase, each participant will get to know the words in the vocabulary.
Concretely, each Swahili word will in turn be presented together with its English counterpart.
The participant is then tasked to retype the English word to stimulate participation.

### Learning phase

The participants will not be actively presented with the time they have left, to avoid a potential increase in stress.

During the learning phase, the participant will learn the new vocabulary.
All Swahili words from the vocabulary are in turn presented to the participant, their occurrence and repetition determined by the model by Sense et al. (2016).
During each turn, the participant is tasked to produce the English translation without any time limit.

There are two situations:
- The participant produces the correct translation.
  In this case, a positive message (e.g. _Correct!_) is displayed until the participant presses Enter to display the next word.
- The participant fails to produce the correct translation.
  In this case, a negative message (e.g. _Incorrect_) is displayed together with the correct translation.
- TODO: how about small spelling mistakes? TODO: do we force the participants to type the correct words?

The learning phase will stop whenever TODO minutes have passed regardless of how many words were processed by the participant.
This is followed by a mandatory break and repeated TODO times.

### Evaluation phase

The evaluation phase is held after TODO minutes after the last learning phase, to assure that the participants actually learned the words, rather than remembering them in their short-term memory.
TODO: Here we have to determine whether we want to do the same as in Van den Broek et al. (2019) and do evaluation like one week after discovery and learning. V: we definitely don't have the time budget for that. We'll have at most a few minutes.

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
TODO: do we shuffle again or keep ordering from PT0?
The feedback is still omitted though it may be present at the end of the experiment for a small morale boost.

## Design

The design base is black text on a white background in the centre of the screen with an input field below the English word. 

Based on the group the participant is placed in, the words will be presented either as:
- P0: white background, 
- P1: the word background is highlighted by the colour corresponding to the difficulty
- P2: the word is presented with its associated colour

The discovery and learning phase will contain these colourings though, for testing, it will depend on the specific subphase.
It will be disabled in PT0 and enabled in PT1.
