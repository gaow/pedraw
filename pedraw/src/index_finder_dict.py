###
#
###
#in this part, we read the map file, and creat two dictionaries, in order to find variant index given variant name or variant position
import sys
file_name=sys.argv[1]

count=0
name_index_dict={}  #the dictionary is used to find index giving variant name
position_index_dict={} #the dictionary is used to find index giving variant position

with open(file_name,'r') as read_file:
    for line in read_file:
        if not line.strip().startswith('#'):
            count=count+1
            info=line.split()  #a list
            name_index_dict[info[1]]=count  #values are indexes
            position_index_dict[info[0]+':'+info[2]]=count  #values are indexes

#also, I will creat 2 lists, one is the variant names; the other is variant positions, we will need them later.
names_list=name_index_dict.keys()
positions_list=position_index_dict.keys()


###
#
###
#in this part, user gives us variant name, and we give the ordered indexes of variants
variant_names=raw_input('--variant-name').split() #this is a list
#below, I find the indexes of variants user specify, put them in a list
variant_names_indexes=[]
for item in variant_names:
    variant_names_indexes.append(name_index_dict[item])

#however, user may give the variants in an unordered way, so we have to reorder them
variant_names_indexes.sort()  #sort those indexes in ascending order
#we reorder them, but we have to tell user the order of the variants
#so we invert the name_index_dict, the keys are indexes, values are variants names
index_name_dict={}
for key in name_index_dict:
    index_name_dict[name_index_dict[key]]=key
#get the variant names in order
variant_names_sorted=[]
for item in variant_names_indexes:
    variant_names_sorted.append(index_name_dict[item])

#now we have 2 lists: variant_names_indexes, which we used to find variants; variant_names_sorted, which we used to inform user the order of variants we display
print(variant_names_indexes)
print(variant_names_sorted)

###
#
###
#in this part, user gives us variant positions, and we give the ordered indexes of variants
variant_positions=raw_input('--variant-pos').split()  #this is a list
#it is like ['22:2.5-10.0','22:20.0','5:50.0-60.0']
#below, I find the indexes of variants user specify, put them in a list
variant_positions_indexes=[]
for item in variant_positions:
    #if there is no '-', it is easy, we search in dictionary directly
    if '-' not in item:
        variant_positions_indexes.append(position_index_dict[item])
    #if there is '-', means it is a range, then we need to get chromosome and positions range
    else:
        pos=item.split(':')  #like ['22','2.5-10.0']
        chr=pos[0]
        cM=pos[1].split('-') #like ['2.5','10.0']
        #now we go through the positions_list, if any position in that list is in the range, we go to postion_index_dict dictionary to get its index
        for item1 in positions_list:
            if chr==item1.split(':')[0] and float(cM[0])<=float(item1.split(':')[1])<=float(cM[1]):
                variant_positions_indexes.append(position_index_dict[item1])

#however, user may give the variants in an unordered way, so we have to reorder them
variant_positions_indexes.sort()  #sort those indexes in ascending order
#we reorder them, but we have to tell user the order of the variants
#so we invert the position_index_dict, the keys are indexes, values are variants names
index_position_dict={}
for key in position_index_dict:
    index_position_dict[position_index_dict[key]]=key
#get the variant names in order
variant_positions_sorted=[]
for item in variant_positions_indexes:
    variant_positions_sorted.append(index_position_dict[item])

#now we have 2 lists: variant_positions_indexes, which we used to find variants; variant_positions_sorted, which we used to inform user the order of variants we display
print(variant_positions_indexes) 
print(variant_positions_sorted)

