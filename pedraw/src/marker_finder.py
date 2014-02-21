import sys
file_name=sys.argv[1]


#below we construct a dictionary. The keys are persons, the values are lists, in each list, there are Id, Name, Sex, Mother, Father, Condition, which will be used in writing csv file; and a list containing pairs of markers 
# person_info_dict={}
# person_list=[]  #also keep a person list to loop over the person_info_dict
# with open(file_name,'r') as read_file:
#     for line in read_file:
#         if not line.startswith('#'):
#             info=line.strip().split()
#             familyID=info[0]
#             personalID=info[1]
#             Name=familyID+':'+personalID
#             person_list.append(Name)
#             Id='F'+familyID+'P'+personalID
#             if info[2]=='0':
#                 Father=''
#             else:
#                 Father='F'+familyID+'P'+info[2]
#             if info[3]=='0':
#                 Mother=''
#             else:
#                 Mother='F'+familyID+'P'+info[3]
#             if info[4]=='1':
#                 Sex='male'
#             else:
#                 Sex='female'
#             if info[5]=='1':
#                 Condition='normal'
#             else:
#                 Condition='affected'
#             alleles=info[6:]
#             person_info=[Id,Name,Sex,Mother,Father,Condition,alleles]
            
#             person_info_dict[Name]=person_info
            #how to find the markers according to index now?
            #No.1 pair of markers     person_info_dict[Name][6][0:2]
            #No.2 pair of markers     person_info_dict[Name][6][2:4]
            #No.3 pair of markers     person_info_dict[Name][6][4:6]
            #No.x pair of markers     person_info_dict[Name][6][2x-2:2x]
           

# #use the person_info_dict to write a csv file
# with open (file_name+'.csv','w') as csv_file:
#     csv_file.write('Id'+'|'+'Name'+'|'+'Sex'+'|'+'Mother'+'|'+'Father'+'|'+'Condition'+'\n')
#     for item in person_list:
#         new_line=person_info_dict[item][0]+'|'+person_info_dict[item][1]+'|'+person_info_dict[item][2]+'|'+person_info_dict[item][3]+'|'+person_info_dict[item][4]+'|'+person_info_dict[item][5]+'\n'
#         csv_file.write(new_line)


#now let user decide what person and marker they want to see
person=raw_input('person: ')
marker_index=int(raw_input('marker index: '))
print(person_info_dict[person][6][2*marker_index-2:2*marker_index])
