# file - collections of data storing in permanent memory at specific location for future use.
#types of file - text(string,number,alphanumeric) and binary(other than text) ex: image
#file operatios- CRUD
#modes of file- Create(x), Read(r), Write(w-overwrite), Append(a)-add extra data inside existing file without overwrite

#1. Create a file syntax: file_object = open("filename", "Accessmode")
""" file_handle = open("create_new.txt", "x") #or complete location
    #file_handle = open("D:/Devops/kode-kloud-test/python-practice/create_new.txt", "x")
 """
#2. Write a file
""" file = open('create_new.txt','w')
file.write('content writing inside a file')
file.close() """

#3. write(accept only string content,use for single line) and writelines(accept list or string, use for multilines)
""" fruits = ['apple\n', 'banana\n', 'cherry']
file_list = open('D:/Devops/kode-kloud-test/python-practice/create_new.txt', 'w')
file_list.writelines(fruits)
file_list.close() """

#4. append a file
""" file = open('create_new.txt','a')
file.write('content writing inside a file')
file.close()  """
#5.Read a muliti line file.
""" multi_line= open('D:/Devops/kode-kloud-test/python-practice/create_new.txt', 'r')
for each_line in multi_line:
    print(each_line, end="")
 """
#6.Read line from a file.
""" multi_line= open('D:/Devops/kode-kloud-test/python-practice/create_new.txt', 'r')
print(multi_line.readline())
 """
#7.Read line from a file dispaly as list.
""" multi_line= open('D:/Devops/kode-kloud-test/python-practice/create_new.txt', 'r')
print(multi_line.readlines()) """

#8.Read a muliti line file and write this content on new file.
""" f1 = open('create_new.txt','r')
wf2= open('write.txt', 'w')
for data in f1:
    wf2.write(data) """

#9.Read a binary file(ex:image)
""" img_f1= open('kk.png','rb') #rb-means readbinary
for i in img_f1:
    print(i) #output as pixel value
 """
#10.Read a binary line file and save this as new binaryfile.
img_f1= open('kk.png','rb') #rb-means readbinary
wf2=open('wkk.png','wb')
for i in img_f1:
    wf2.write(i)
 