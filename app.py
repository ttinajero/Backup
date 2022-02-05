import os
import string
import re
import shutil
import time
from datetime import date

OLD_FOLDER = r""
NEW_FOLDER = r""
num_files = 0
num_files_c = 0
num_copied = 0
TIME_NOW = time.time()
TIME_NOW_S = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(TIME_NOW))
OLD_LOGFILE = ""
NEW_LOGFILE = ""

carpeta_origen = os.path.abspath('') #Aqui va la carpeta donde estan los archivos origen
carpeta_destino = os.path.abspath('/respaldo')


def get_mod_time(full_path):
  modified_t = os.path.getmtime(full_path)
  modified_t_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(modified_t))
  return modified_t, modified_t_str


print ("PROGRAMA: LISTAR ARCHIVOS EN ORIGEN")
print (15*"-")
print("origen:", carpeta_origen)
print ("origen logfile:", carpeta_origen)


source_log = open('log_'+TIME_NOW_S,'w+')
source_log.write(50*"=" + "\n")
source_log.write("PROGRAMA: LISTA DE ARCHIVOS DE CARPETA ORIGEN\n") # *********************

log_text = ""

for root, dirs, files in os.walk(carpeta_origen):
    for fname in files:
        
        old_full_path = os.path.join(root, fname)

        matchObj = re.match( r'.*\$.*', old_full_path, re.I)
        if matchObj:
            break

        num_files += 1
        m_t, m_t_s = get_mod_time(old_full_path)
        log_text += m_t_s + "\t" + old_full_path +"\n"
        print ("- " + old_full_path)
        source_log.write(log_text)
    
print('Total de archivos: '+str(num_files)+"\n\n")

print ("PROGRAMA: COMPARAR ARCHIVOS CON DESTINO") # ***************************************

log_text = ""
log_new_files = ""

for root, dirs, files in os.walk(carpeta_origen):
    for fname in files:
      
        old_full_path = os.path.join(root, fname)
        new_full_path = os.path.join(str.replace(root,carpeta_origen,carpeta_destino, 1), fname)


        matchObj = re.match( r'.*\$.*', old_full_path, re.I)
        if matchObj:
            break

        num_files += 1
        m_t, m_t_s = get_mod_time(old_full_path)

        if not os.path.exists(new_full_path):
            num_files_c += 1
            log_text += "* " + m_t_s + "\t" + old_full_path +"\n"
            log_new_files += "* " + m_t_s + "\t" + old_full_path +"\n"
            print ("* No existe: " + old_full_path)
        else:
            new_m_t, new_m_t_s = get_mod_time(new_full_path)
            if (m_t - new_m_t) >  1:
                num_files_c += 1
                log_text += "* " + new_m_t_s + "\t" + old_full_path +"\n"
                log_new_files += "* " + new_m_t_s + "\t" + old_full_path +"\n"
                print ("* Modificado" + old_full_path)
            else:
                log_text += "- " + m_t_s + "\t" + old_full_path +"\n"
                print ("- Igual " + old_full_path)

print('Archivos totales:'+str(num_files)+' Archivos a respaldar:'+str(num_files_c)+ "\n")

source_log.write(log_text)
source_log.write(50*"=" + "\n")
source_log.write("Nuevos archivos a copiar\n" + 20*"=" + "\n")
source_log.write(log_new_files) 


source_log.close()