# -*- coding: utf-8 -*-


import cv2
import time
import numpy as np
import os
import sqlite3


# ctrl-c to stop pour arrêter l'executation de programme

# constantes
IM_HEIGHT = 400
IM_WIDTH = 400
TIME_INTERVAL = 2 #interval de temps de sauvegarde
font = cv2.FONT_HERSHEY_SIMPLEX
file_folder_name = time.strftime("%Y_%h_%d")

# variables d'initialisation
ID = 0
t = time.time()


#init sqlite file
if not os.path.exists("{0}/{1}".format(os.getcwd(), file_folder_name)):
    os.makedirs("{0}/{1}".format(os.getcwd(), file_folder_name))
fichierDonnees = "{0}/{1}/{2}".format(os.getcwd(), file_folder_name, "database.db")

if os.path.isfile(fichierDonnees):
    os.remove(fichierDonnees)
    print("file deleted")

output1 = "ID"
output1_type = "INTEGER"

output2 = "date"
output2_type = "DATETIME"

output3 = "conformity"
output3_type = "INTEGER"

list_output = [output1, output2, output3]
list_output_type = [output1_type, output2_type, output3_type] 
table_name = "table_1"
conn = sqlite3.connect(fichierDonnees)
cur = conn.cursor()
for i in range(len(list_output)):
    if i == 0:
        cur.execute("CREATE TABLE {0} ({1} {2})".format(table_name, list_output[i], list_output_type[i]))
    else:
        cur.execute(
            "ALTER TABLE {0} ADD COLUMN {1} {2}".format(table_name, list_output[i], list_output_type[i]))

#boucle infinie
while True:
    if time.time() - t > TIME_INTERVAL:      
        
        im_zeros = np.zeros((IM_WIDTH, IM_HEIGHT, 3))
        
        
        path_to_save = "{0}/{1}/{2}".format(os.getcwd(), file_folder_name, ID)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
             
        
        cv2.putText(im_zeros, 
                    "ID : {0}".format(ID),
                    (0, int(IM_HEIGHT/2)), 
                    font,
                    2,
                    (255, 255, 255),
                    2)
                    
        cv2.imwrite("{0}/IM_ID_{1}_1.jpg".format(path_to_save, ID), im_zeros)  
        cv2.imwrite("{0}/IM_ID_{1}_2.jpg".format(path_to_save, ID), im_zeros)         
        
        
        print("{0}/IM_ID_{1}.jpg".format(path_to_save, ID))
        
        output_DATETIME = time.strftime("%d_%m_%Y_%H_%M_%S")

        list_output_label = ["ID", "date", "conformity"]
        random_conformity = np.random.randint(2, size=1)[0]
        print("random_conformity", random_conformity)
        list_output_value = [ID, output_DATETIME, random_conformity]
        
        #fill sql file
        conn = sqlite3.connect(fichierDonnees)
        cur = conn.cursor()
        table_name = "table_1" 

        cur.execute(
            "INSERT INTO {0}({1}) VALUES({2})".format(table_name, str(list_output_label).strip('[]'),
                                                      str(list_output_value).strip('[]')))
        conn.commit()

        cur.close()
        conn.close()
        
        ID += 1
        t = time.time()
