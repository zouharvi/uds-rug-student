- meaning is the relation between natural language expressions and their extra-linguistic referents
- this is unlike phonetics, morphology and syntax, which is defined within the language

## syllogisms
- schematic patterns for correct arguments (modues ponens, modus tollens)

## Frege
- distinguish between sense (Sinn) and  reference (Bedeutung)


## Truth-conditional formal semantics
- sentence and formula are true in the same possible worlds:
- "john is a snowman" <=> snowman(john)


## model structure
- formal representation of a possible situation, defined by a universe (U) and an interpretation function (V)
```
U = {e1, e2, e3, e4, e5}
V(snowman) = {e1, e2, e3}
V(john) = {e1}
V(white) = {e1, e2, e3, e4}
```
- out of this we can make reasoning based on the subset property: "john is a snowman", "every snowman is white"

## first-order predicate logic
- defines under what conditions a model makes a formula true
- looks only at properties of entities (relations)
- terms: variables union constants, terms can have equality 
- atomic formulas: R(t1,..tn), t1, .. tn
- well formed-formulas: closure under logical operators

### interpretation
- V(constant) \in U
- V(predicate) \subseteq U^n for n>=1
- V(predicate) \in {0,1} for zero arity
- g(variable) -> U
