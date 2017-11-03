import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

with open('trainingsets.json') as f:
	ff = json.load(f)

preselections = ff['preselections']
trainings = ff['trainings']

for tkey in trainings:
	trainings[tkey]["preselection"] = preselections[trainings[tkey]["preselection"]]

pp.pprint(trainings["mvaIsolation3HitsDeltaR05opt2aLTDB_1p0"])
