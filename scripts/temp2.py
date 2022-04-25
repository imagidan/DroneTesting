label_text = open("../lpr/us_lp_characters.txt", "r").readlines()
labels = []
for line in label_text:
    labels.append(line[0])

print(labels)