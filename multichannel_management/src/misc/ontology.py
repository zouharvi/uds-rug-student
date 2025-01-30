ONTOLOGY_OLD = {
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
    "not_interesting": "not_interesting",
}

ONTOLOGY = {
    "effective": ["effective", "communication", "interesting"],
    "ineffective": ["ineffective", "communication", "interesting"],
    "communication": ["communication", "interesting"],
    "citizen": ["citizen", "role_responsibility", "interesting"],
    "media": ["media", "role_responsibility", "interesting"],
    "government": ["government", "role_responsibility", "interesting"],
    "role_responsibility": ["role_responsibility", "interesting"],
    None: "not_interesting",
}