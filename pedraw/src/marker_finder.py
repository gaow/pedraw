import sys
file_name=sys.argv[1]


#below we construct a dictionary. The keys are persons, the values are lists containing pairs of markers 
person_marker_dict={}
with open(file_name,'r') as read_file:
    for line in read_file:
        if not line.startswith('#'):
            info=line.strip().split(' ')
            familyID=info[0]
            personalID=info[1]
            person_marker_dict[familyID+':'+personalID]=info[6:]
            #how to find the markers according to index now?
            #No.1 pair of markers     person_marker_dict[marker_index][0:2]
            #No.2 pair of markers     person_marker_dict[marker_index][2:4]
            #No.3 pair of markers     person_marker_dict[marker_index][4:6]
            #No.x pair of markers     person_marker_dict[marker_index][2x-2:2x]
            
#now let user decide what person and marker they want to see
person=raw_input('person: ')
marker_index=int(raw_input('marker index: '))
print(person_marker_dict[person][2*marker_index-2:2*marker_index])
