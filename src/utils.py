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
                "conflict_interest_gov",
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
                "conflict_interest_med",
                "explanation",
                "information_provision",
                "critical_attitude",
                # "meaning_making",
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
                "too_substantive",
                "reduce_urgency"
            ]
        }
    },
    "not_interesting": "not_interesting"
}

def reverse_ontology(val, stack=[], ontology_rev={}):
    if type(val) is str:
        if val in ontology_rev:
            print(f"WARNING: {val} is in the ontology at least twice")
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

def print_ontology(ontology):
    for k,v in ontology.items():
        print(k,v)

def read_data(path, reviews=False, ontology_level=1):
    with open(path, "r") as f:
        data = list(csv.reader(f))

    if not reviews:
        ontology_rev = reverse_ontology(ONTOLOGY)
        ontology_rev = ontology_level(ontology_rev, level=ontology_level)
        data = [
            (sent_txt, ontology_rev[sent_label])
            for sent_txt, sent_label in data
        ]
        used_labels = {sent_label for _sent_txt, sent_label in data}
        all_labels = set(ontology_rev.values())
        print(all_labels-used_labels, "is not represented")
    return data