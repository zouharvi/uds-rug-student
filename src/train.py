from data.ontonotes import OntoNotesEmbd, tags_order

data = OntoNotesEmbd("data/embedding_").get("test")
classes_map, classes_count = tags_order(data)
print(classes_map)



print(data[0].keys())
input()