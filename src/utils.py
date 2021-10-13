#!/usr/bin/env python3

import torch

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")
DEVICE_CPU = torch.device("cpu")

def binarize_label(sent_label):
    return (
        1 if sent_label == "music" else 0,
        1 if sent_label == "books" else 0,
        1 if sent_label == "health" else 0,
        1 if sent_label == "dvd" else 0,
        1 if sent_label == "software" else 0,
        1 if sent_label == "camera" else 0,
    )

ONTOLOGY = {
    "interesting": {
        "role_responsibility": {
            "government": [
                "conflict_interest",
                "social_norm",
                "crisis_response",
                "meaning_making",
                "clarification",
                "process_information",
                "support_for_affected",
                "coordination",
                "damage_limitation",
            ],
            "media": [
                "dynamic_nature_pandemic",
                "conflict_interest",
                "explanation",
                "information_provision",
                "critical_attitude",
                "meaning_making",
                "independence",
            ],
            "citizen": [
                "risk_perception",
                "affected_people",
                "inform",
                "follow_action",
                "social_assistance",
                "taking_initiatives",
                "critical_look",
            ]
        },
        "communication": {
            "effective": [
                "compel",
                "empathy",
                "leadership_posture",
                "role_models",
                "self_efficacy",
                "perceptual_efficacy",
                "consistency",
                "transparency",
                "clarity",
                "urgency",
                "relevance",
                "simple_effective",
                "argumentation",
                "persuation",
                "emphasizing_belonging",
                "target_audience",
                "citizen_engagement",
                "peripheral_communication",
            ],
            "ineffective": [
                "promises",
                "losing_sight_public_interest",
                "affective_response",
                "democratic_decision_making",
                "assign_blame",
                "deny_criticism",
                "authoritarian_selfishness",
                "no_communication",
                "perceptual_efficacy",
                "too_substantive",
                "reduce_urgency"
            ]
        }
    },
    "not_interesting": "not_interesting"
}

# replace None with parent keys
# ONTOLOGY =  {k:(v if v is not None else v) for k,v in ONTOLOGY.items()}

# TODO: class overlap

def reverse_ontology(val, stack=[], ontology_rev={}):
    if type(val) is str:
        ontology_rev[val] = stack
    elif type(val) is dict:
        for key, item in val.items():
            reverse_ontology(item, stack+[key], ontology_rev)
    elif type(val) is list:
        for item in val:
            reverse_ontology(item, stack, ontology_rev)
    else:
        raise Exception("Unknown type")
    return ontology_rev

def ontology_level(ontology, level=None):
    return {k:v[:level][0] for k,v in ontology.items()}

ontology_rev = reverse_ontology(ONTOLOGY)
ontology_rev = ontology_level(ontology_rev, level=1)

for k,v in ontology_rev.items():
    print(k,v)


        
print

# TODO: warning when class not represented