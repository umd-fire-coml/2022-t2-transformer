import os
# i move all to one folder and remove the names to shorten the path files
os.chdir("C:\\Users\\drago\\Downloads\\adl-piano-midi")
count = 0
for i in os.listdir("."):
    path = i
    for j in os.listdir(path):
        path2 = path + "\\" + j
        for k in os.listdir(path2):
            path3 = path2 + "\\" + k
            for music_name in os.listdir(path3):
                count += 1
                music_path = path3 + "\\" + music_name
                os.rename(music_path, str(count) + ".mid")