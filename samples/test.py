import json

jdata = json.load(open("configs.json"))

print jdata
print("\n\n\n\n")

for item in jdata:
	for subitem in jdata[item]:
		print subitem