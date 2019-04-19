import struct,glob,os

header_format = "4s18i"
header_size = struct.calcsize(header_format)

inst_format = "7f3i"
inst_size = struct.calcsize(inst_format)

cars_format = "4f8i"
cars_size = struct.calcsize(cars_format)




# ----- Functions -----

def get_files_with_extention(str_extention):
    str_extention = "./bin/*." + str_extention
    return glob.glob(str_extention)

def file_dir(dirName,fileName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    if os.path.exists(dirName+"/"+fileName):
        os.remove(dirName+"/"+fileName)

def checks(file_names):
    global header_size
    for y in file_names:
        file_name = y[6:]
        with open(y, 'rb') as f:
            try:
                data = struct.unpack(header_format,f.read()[:header_size])
            except:
                print("\nError opening file (" + file_name +")! Press return to restart program...\n\n-----\n\n\n")
                main()
                
            print("Successfully opened file (" + file_name +").")

            convert_bin2text(data[1],data[5],file_name,y)
        header_size = struct.calcsize(header_format)
     

def convert_bin2text(inst_instances,car_instances,file_name,input_file):
    global header_size
    file_dir("text",file_name)

    with open("text/"+file_name, 'a+') as w:
        w.write("# This file has been converted using Bin2Text Converter by Grinch_ \ninst\n")
        for x in range(inst_instances):
            with open(input_file, 'rb') as r:
                try:
                    data = struct.unpack(inst_format,r.read()[header_size:(header_size+40)])
                except:
                    print("\nError processing inst of file (" + file_name +")! Press return to restart program...\n\n-----\n\n\n")
                    input()
                    main()

                text_ipl = str(data[7]) + ' , '+'dummy' + ' , ' + str(data[8]) + ' , ' + str(data[0]) + ' , ' + str(data[1]) + ' , ' + str(data[2]) + ' , ' + str(data[3]) + ' , ' + str(data[4]) + ' , ' + str(data[5]) + ' , ' + str(data[6]) + ' , ' + str(data[9]) 
                w.write(text_ipl)
                w.write("\n")                
            header_size += 40
        w.write("end\ncars\n")
        for x in range(car_instances):
            with open(input_file, 'rb') as r:
                try:
                    data = struct.unpack(cars_format,r.read()[header_size:(header_size+48)])
                except:
                    print("\nError processing car of (" + file_name +")! Press return to restart program...\n\n-----\n\n\n")
                    input()
                    main()
                w.write(''.join(str(data)[1:-1]))
                w.write("\n")
                    
            header_size += 48
        w.write("end\n")
    print("Successfully processed file (" + file_name +").\n")

def main():
    print("Bin2Text Converter v1.0\n\nPut all the binary ipl files in bin directory.Press return to continue")
    input()
    if not os.path.exists("bin"):
        os.mkdir("bin")
        print("Bin directory doesn't seem to exist.Creating it.")

    file_names = get_files_with_extention("ipl")
    if len(file_names) != 0 :
        print("Found IPL files: " + str(file_names) + "\n")
        checks(file_names)
    else:
        print("No IPL files found")
    print("Press return to restart...")
    input()
    main()
# ---------------------


#----Main-----s
main()
print("\nTask completed successfully.")