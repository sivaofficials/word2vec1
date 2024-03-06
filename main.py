from src.unranked import DBpedia
from src import layer_store

iteration_limit = 20
counter = 0


seed_word= input("Enter the seed word: ")
status_code=DBpedia.check_seed(seed_word)
layer1_links=DBpedia.layer1(seed_word)
layer_store(layer1_links,"layer1.txt")

layer2_links = set()

for links in layer1_links:
    layer2 = DBpedia.layer2(links)
    layer2_links.update(layer2)  
    counter += 1
    if counter == iteration_limit:
        break

layer_store(layer2_links,"layer2.txt")

output_file_path = "/home/kali/project/output/layer2.txt"

with open(output_file_path, "r") as f:
    file_content = f.read()
links = file_content.split("\n")
removed_layer2 = [link.split("/")[-1] for link in links if link.strip()]

with open("/home/kali/project/output/layer2_santised.txt", "w") as file1:
        for term1 in removed_layer2:
            if ":" in term1:
              pass
            elif "," in term1:
              part=term1.split(",")

              file1.write(f"{term1[0]}\n")
              file1.write(f"{term1[-1]}\n")
            elif "(" in term1:
                part=term1.split("(")
                last_part = part[-1].rstrip(")")
                file1.write(f"{last_part}\n")
            else:
              file1.write(f"{term1}\n") 

layer2_sanitised=DBpedia.satisation("/home/kali/project/output/layer2_refined.txt")

with open("/home/kali/project/output/layer2_santised.txt", "w") as file2:
    for term in layer2_sanitised:
        if len(term) >= 28:
            pass
        else:
            file2.write(f"{term}\n") 



