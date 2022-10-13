import command
import os

def calculate_empty_rss(path):
    command_line = f"temp/empty-model-rss {path}"
    # res = command.run([command_line])
    res = os.system(command_line)


dimension = 2
co = 16
rsss = []
for i in range(1, 6):
    path = f"temp/{dimension}d-results/{i}/tensors/numnoise/dataset-co{co}.fuzzy_tensor"
    rsss.append	(calculate_empty_rss(path))

# average_rss = sum(rsss)/len(rsss)
print(f"Analysis for {dimension}d-co{co}")
print(rsss)
# print(average_rss)

