import csv, collections

raw_data = collections.defaultdict(lambda: [])
with open("monster_data.csv") as f:
	reader = csv.DictReader(f)
	for row in reader:
		raw_data[row["section"]].append(row)

bosses = []

print("monsters = [")
for key in sorted(raw_data.keys()):
	if key and key.isdigit():
		print("    [ # section %s" % key)
		for row in raw_data[key]:
			if row["P-Difficulty"].isdigit() and row["E-Difficulty"].isdigit():
				name = "".join(filter(lambda ch: ch.isalpha(), row["Monster"]))
				if row["P-Difficulty"] == "100" and row["E-Difficulty"] == "100":
					bosses.append("_MonsterCreator(%s,%s,%s,%s,%s,%s)," % (name, row["Health"], row["Attack"], row["Defense"], row["Gold"], row["section"]))
				else:
					print("        _MonsterCreator(%s,%s,%s,%s,%s,%s,%s,%s)," % (name, row["Health"], row["Attack"], row["Defense"], row["Gold"], row["section"], row["P-Difficulty"], row["E-Difficulty"]))
		print("    ],")
print("]")
print()
print("bosses = [")
for boss in bosses:
	print("    %s" % boss)
print("]")
