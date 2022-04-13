import csv
from itertools import combinations
from collections import defaultdict


class CarSet:
    counter = 0
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__.update(kwargs)
        self.calc_stats()
        CarSet.counter += 1

    def calc_stats(self):
        statdict = defaultdict(int)
        for key, value in self.__dict__.items():
            if type(value) is dict:
                statdict["power"] += int(value["power"])
                statdict["aero"] += int(value["aero"])
                statdict["grip"] += int(value["grip"])
                statdict["reliability"] += int(value["reliability"])
                statdict["pitstop"] += float(value["pit"])
        statdict["total"] += (
            statdict["power"]
            + statdict["aero"]
            + statdict["grip"]
            + statdict["reliability"]
        )
        self.__dict__.update(statdict)

    def __str__(self):
        string = "Parts\n"
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                for i, j in value.items():
                    string += f"{i}: {j:15}"
                string += "\n"
        string += f"\nStats\n"
        string += (
            f"Total: {self.total} Power: {self.power} Aero: {self.aero} "
            f"Grip: {self.grip} Reliability: {self.reliability} Pitstop: {self.pitstop}\n\n"
        )
        return string


parts = open("parts.csv")
partsDict = defaultdict(list)
setslist = []
partsReader = csv.DictReader(parts)

for i in partsReader:
    #print(i)
    partsDict[i["type"]].append(i)

for brake in partsDict["Brake"]:
    for gearbox in partsDict["Gearbox"]:
        for rearwing in partsDict["Rearwing"]:
            for frontwing in partsDict["Frontwing"]:
                for suspension in partsDict["Suspension"]:
                    for engine in partsDict["Engine"]:
                        setslist.append(
                            CarSet(
                                brake=brake,
                                gearbox=gearbox,
                                rearwing=rearwing,
                                frontwing=frontwing,
                                suspension=suspension,
                                engine=engine,
                            )
                        )


sortminpittime = sorted(
    setslist,
    key=lambda x: (-x.pitstop),
    reverse=True,
)[:4]
sortmaxtotal = sorted(
    setslist,
    key=lambda x: (x.total),
    reverse=True,
)[:4]

outputfile = open("output.txt", "w")

outputfile.write("Minimum Pit Stop Time\n")
for i in sortminpittime:
    outputfile.write(str(i))

outputfile.write("\n" * 5 + "Maximum Total Overall\n")
for i in sortmaxtotal:
    outputfile.write(str(i))

print(CarSet.counter)
parts.close()
outputfile.close()
