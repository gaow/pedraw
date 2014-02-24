def haplotype_finder(ped_file_name, map_file_name, variant_name, variant_pos):
    
    ###
    #
    ###
    #in this part, we read the map file, and creat two dictionaries, in order to find variant index given variant name or variant position
    
    count=0
    name_index_dict={}  #the dictionary is used to find index giving variant name
    position_index_dict={} #the dictionary is used to find index giving variant position
    
    with open(map_file_name,'r') as read_map_file:
        for line in read_map_file:
            if not line.strip().startswith('#'):
                count=count+1
                info=line.split()  #a list
                name_index_dict[info[1]]=count  #keys are variant names, values are indexes
                position_index_dict[info[0]+':'+info[2]]=count  #keys are variant positions, values are indexes
    
    #also, I will creat 2 lists, one is the variant names; the other is variant positions, we may need them later.
    names_list=name_index_dict.keys()
    positions_list=position_index_dict.keys()
    
    
    ###
    #
    ###
    #in this part, user gives us variant names and variant positions, and we give the ordered indexes of variants
    
    #first, when user gives us variant names, we find indexes
    variant_names=variant_name.split() #this is a list
    #below, I find the indexes of variants user specify, put them in a list
    variant_names_indexes=[]
    for item in variant_names:
        variant_names_indexes.append(name_index_dict[item])
    
    #second, when user gives us variant positions, we find indexes
    variant_positions=variant_pos.split()  #this is a list
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
                    
    #however, user may give us some repeated variants, so we only keep unique variants; also, user may give the variants in an unordered way, so we have to reorder them
    unique_variant_indexes_set=set(variant_names_indexes+variant_positions_indexes) #use set to get uniq value
    variant_indexes=list(unique_variant_indexes_set) #put them in a list so that we can sort them
    variant_indexes.sort()  #sort those indexes in ascending order
    
    
    #we reorder them, but we have to tell user the order of the variants
    #so we invert the name_index_dict, the keys are indexes, values are variants names
    index_name_dict={}
    for key in name_index_dict:
        index_name_dict[name_index_dict[key]]=key
    #get the variant names in order
    variant_names_sorted=[]
    for item in variant_indexes:
        variant_names_sorted.append(index_name_dict[item])
    
    #with same logic, we invert the position_index_dict, the keys are indexes, values are variants names
    index_position_dict={}
    for key in position_index_dict:
        index_position_dict[position_index_dict[key]]=key
    #get the variant positions in order
    variant_positions_sorted=[]
    for item in variant_indexes:
        variant_positions_sorted.append(index_position_dict[item])
    
    #now we have 3 lists: 
    #variant_indexes, which we used to find variants; 
    #variant_names_sorted, which we used to inform user the order of variants we display
    #variant_positions_sorted, which we used to inform user the order of variants we display
    #write a log file:
    with open('ordered_variants.log','w') as write_log_file:
        write_log_file.write('Below are ordered variant names:\n')
        write_log_file.write(str(variant_names_sorted)+'\n')
        write_log_file.write('Below are ordered variant positions:\n')
        write_log_file.write(str(variant_positions_sorted)+'\n')
    
    
    ###
    #
    ###
    #below we construct a dictionary. The keys are 'Id's required by csv file in 'F{}P{}' format, the values are lists, each list contains pairs of markers 
    #the goal of this part is we read a ped file, and can find variants according to variant indexes
    person_variants_dict={}
    with open(ped_file_name,'r') as read_ped_file:
        for line in read_ped_file:
            if not line.startswith('#'):
                info=line.strip().split()
                Id='F{}P{}'.format(info[0],info[1])                    
                person_variants_dict[Id]=info[6:]
                #how to find the markers according to index now?
                #No.1 pair of markers     person_variants_dict[Id][0:2]
                #No.2 pair of markers     person_variants_dict[Id][2:4]
                #No.3 pair of markers     person_variants_dict[Id][4:6]
                #No.x pair of markers     person_variants_dict[Id][2x-2:2x]
                
                
    #At last, we get each person's haplotype given variant indexes. We will create a dictionary to put such information
    person_haplotype_dict={}
    for person in person_variants_dict:
        alleles=[]
        for index in variant_indexes:
            alleles=alleles+person_variants_dict[person][2*index-2:2*index]
        haplotype='\\'
        for item in alleles:
            haplotype=haplotype+item+'\\'
        person_haplotype_dict[person]=haplotype
    
    return person_haplotype_dict
    
    
if __name__=='__main__':
    import sys
    ped_file_name=sys.argv[1]
    map_file_name=sys.argv[2]
    variant_name=raw_input('--variant_name')
    variant_pos=raw_input('--variant_pos')
    for person in haplotype_finder(ped_file_name, map_file_name, variant_name, variant_pos):
        print(person, haplotype_finder(ped_file_name, map_file_name, variant_name, variant_pos)[person])
    
