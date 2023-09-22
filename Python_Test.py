
import os                               #import necessary libraries
import sys
import shutil
import hashlib
import time

def hash_file(file_path):                 # calculate hashfile for a file path 
   
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:     
        while True:
            data = file.read(4096)          #read chunks of 4KB of the file
            if not data:
                break
            hasher.update(data)             #update the hasher object 
    return hasher.hexdigest()

def synchronize_folders(source_folder, replica_folder, log_file):       
  
        for root, dirs, files in os.walk(source_folder):             # looking in source folder 
            

            for file in files:
                source_file_path=os.path.join(root,file)                                                            #create source and replica file path
                replica_file_path=os.path.join(replica_folder, os.path.relpath(source_file_path,source_folder))
                
                if not os.path.exists(replica_file_path) or hash_file(source_file_path) != hash_file(replica_file_path):   #if a file does not exist or is different in replica folder, it will create/modify the file
                    shutil.copy2(source_file_path, replica_file_path)
                    source_file_hash = hash_file(source_file_path)
                    log_entry = f"File copied: {source_file_path} -> {replica_file_path} (MD5: {source_file_hash})\n"       
                    log_file.write(log_entry)                                                                               #log entry for file: creation or modification
                    print(log_entry.strip())




            for dir in dirs:
            
                source_dir_path=os.path.join(root,dir)                                                          #create source and replica direcory path
                replica_dir_path=os.path.join(replica_folder, os.path.relpath(source_dir_path,source_folder))
                
                if not os.path.exists(replica_dir_path):
                    
                    shutil.copytree(source_dir_path, replica_dir_path)                                          #create directory in replica folder
                    log_entry = f"Directory copied: {source_dir_path} -> {replica_dir_path} \n"                 
                    log_file.write(log_entry)                                                                   #log entry for the creation of directory
                    print(log_entry.strip())



        for root,dirs,files in os.walk(replica_folder, topdown=False):                                  # looking in replica folder
            
            for file in files:
                
                replica_file_path = os.path.join(root, file)                                                            #creating replica and source file path
                source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))
                   
                if not os.path.exists(source_file_path):                                                                
                    os.remove(replica_file_path)                                                                        #remove replica file path in case it does not exist in source
                    log_entry = f"File removed: {replica_file_path}\n"                                                 
                    log_file.write(log_entry)                                                                            #log entry for removing file
                    print(log_entry.strip())

            for dir in dirs:

                replica_dir_path=os.path.join(root,dir)                                                                  #creating replica and source directory path
                source_dir_path = os.path.join(source_folder, os.path.relpath(replica_dir_path, replica_folder))
                
                if not os.path.exists(source_dir_path):
                    shutil.rmtree(replica_dir_path)                                              #remove replica directory path in case it does not exist in source
                    log_entry = f"Directory removed: {replica_file_path}\n"                     
                    log_file.write(log_entry)                                                    #log entry
                    print(log_entry.strip())



if __name__ == "__main__":
    if len(sys.argv) != 5:                                                                          # make sure the number of arguments provided in the command line is correct
        print("Usage: python sync_folders.py <source_folder> <replica_folder> <log_file>")
        sys.exit(1)

    source_folder = sys.argv[1]                                                                     #allocation of the arguments
    replica_folder = sys.argv[2]
    log_file_path = sys.argv[3]
    sync_interval = int(sys.argv[4])

    with open(log_file_path, "a") as log_file:                                                      #opens log file in append mode
        while True:
            synchronize_folders(source_folder, replica_folder, log_file)                            #call the syncronize_folders function
            print("Synchronization completed. Waiting for the next interval:")
            time.sleep(sync_interval)                                                                          # Interval of time 