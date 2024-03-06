def layer_store(data,layer):
    output_file_path = f"/home/kali/project/output/{layer}"
    with open(output_file_path, "w") as file:
        for links in data:
            file.write(f"{links}\n")