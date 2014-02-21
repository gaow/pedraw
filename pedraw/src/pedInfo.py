#!/usr/bin/env python

import random

class restoreStruct():
    '''
    obtain generation information for each individual in the family
    and restore family structure
    '''
    def __init__(self, familyID, familyDict):
        self.familyID = familyID
        self.familyDict = familyDict
        # create a dict and use individual ids as keys
        famInfo = {}
        # check individual IDs, no '0' allowed
        self.checkIndividualIDs(self.familyID, self.familyDict)
        # check sex (all fathers should be males, mothers should be females)
        self.checkSex(self.familyID, self.familyDict)
        # retrieve family related info
        for idx, indID in enumerate(familyDict['individualID']):
            famInfo[indID] = {'indID': indID, 'indIdx': idx, 'sex': familyDict['sex'][idx], 'trait': familyDict['trait'][idx], 'fatherID': familyDict['fatherID'][idx], 'motherID': familyDict['motherID'][idx], 'fatherFatherID': self.getFatherFatherID(indID), 'fatherMotherID': self.getFatherMotherID(indID), 'motherFatherID': self.getMotherFatherID(indID), 'motherMotherID': self.getMotherMotherID(indID), 'childIDs': self.getChildIDs(indID), 'spouseIDs': self.getSpouseIDs(indID), 'ancestorIDs':[], 'offspringIDs':[]} 
        self.famInfo = famInfo
        # reconstruct info about which generation does each individual belong to
        # assuming the most distant common ancestors are at generation 1
        self.addGenInfo(indIDs = self.familyDict['individualID'])
        # add "ancestorIDs:[...]" and "offspringIDs":[...] info to each individual
        # to trace IDs of all ascending and descending relatives of such individual 
        self.addAncestorOffspringInfo()
        return
    
    
    def checkIndividualIDs(self, familyID, familyDict):
        '''
        check individual IDs to be '0' free and unique
        '''
        if 0 in familyDict['individualID']:
            idx0 = familyDict['individualID'].index(0)
            raise ValueError("Individual ID cannot be 0 --> individual #%d in family %s" % (idx0+1, str(familyID)))
        # check uniqueness
        if len(set(familyDict['individualID'])) < len(familyDict['individualID']):
            raise ValueError("Duplicated individual IDs found in family %s" % familyID)
        return
    
        
    def checkSex(self, familyID, familyDict, maleCoding=['1', 'M', 'male', 'MALE'], femaleCoding=['2', 'F', 'female', 'FEMALE']):
        '''
        check sex for fathers and mothers 
        '''
        for (fatherID, motherID) in zip(familyDict['fatherID'], familyDict['motherID']):
            if fatherID in familyDict['individualID']:
                fatherIdx = familyDict['individualID'].index(fatherID)
                if str(familyDict['sex'][fatherIdx]) not in  maleCoding:
                    raise ValueError("Individual %s in family %s is specified as father but with incorrect gender %s" % (str(fatherID), str(familyID), str(familyDict['sex'][fatherIdx])))
            if motherID in familyDict['individualID']:
                motherIdx = familyDict['individualID'].index(motherID)
                if str(familyDict['sex'][motherIdx]) not in femaleCoding:
                    raise ValueError("Individual %s in family %s is specified as mother but with incorrect gender %s" % (str(motherID), str(familyID), str(familyDict['sex'][motherIdx])))
        return
    
    
    def _sortIndIDsByGen(self):
        indIDsByGen = {}
        for indID in self.familyDict['individualID']:
            if indIDsByGen.has_key(self.famInfo[indID]['gen']):
                indIDsByGen[self.famInfo[indID]['gen']].append(indID)
            else:
                indIDsByGen[self.famInfo[indID]['gen']] = [indID]
        indIDs_sorted = []
        gens = indIDsByGen.keys()
        gens.sort()
        for gen in gens:
            indIDs_sorted.extend(indIDsByGen[gen])
        return indIDs_sorted
    
    
    def addAncestorOffspringInfo(self):
        '''
        '''
        indIDs_sorted = self._sortIndIDsByGen()
        ## assign each ind's ancestors' IDs in sequential order of generational numbers (top down approach)
        for indID in indIDs_sorted:
            # append ind's parents to ind's ancestorIDs
            # and extend ind's partents' ancestorIDs to ind's ancestorIDs
            fatherID, motherID = self.famInfo[indID]['fatherID'], self.famInfo[indID]['motherID']
            if fatherID is not '0':
                self.famInfo[indID]['ancestorIDs'].append(fatherID)
                self.famInfo[indID]['ancestorIDs'].extend(self.famInfo[fatherID]['ancestorIDs'])
            if motherID is not '0':
                self.famInfo[indID]['ancestorIDs'].append(motherID)
                self.famInfo[indID]['ancestorIDs'].extend(self.famInfo[motherID]['ancestorIDs'])
            self.famInfo[indID]['ancestorIDs'] = list(set(self.famInfo[indID]['ancestorIDs']))
        ## assign each ind's offspringIDs according to ancestorIDs info
        for indID in indIDs_sorted:
            for ancInd in self.famInfo[indID]['ancestorIDs']:
                self.famInfo[ancInd]['offspringIDs'].append(indID)

        return
    
    
    def recodeGenInfo(self, indIDs):
        genInfo = [self.famInfo[i]['gen'] for i in indIDs]
        if min(genInfo) < 1:
            for i in indIDs:
                self.famInfo[i]['gen'] += (1-min(genInfo))
        return   
        
    
    def addGenInfo(self, indIDs):
        '''
        This function adds generational information to self.famInfo dict.
        Most ancestral founder individuals are given 'gen=1' while
        gen=2,3,... are assigned to offspring and married-in founder(s)/spouses(s)
        (it can handle the situation where a single family ID includes mixed pedigree structures <-->
        individuals belonging to same 'family ID' but are not necessarily all related to each other)
        '''
        # assign gen info to relatives of any individual (randomly selected) recursively
        self.indsAddedGenInfo = []
        ind = random.choice(indIDs)
        self.famInfo[ind]['gen'] = 1
        self.indsAddedGenInfo.append(ind)
        self._setGen(ind, gen=1)
        # recode gen info if min(ind['gen']) < 1
        self.recodeGenInfo(self.indsAddedGenInfo)
        # check if all inds have been assigned gen info
        try:
            assert [self.famInfo[i].has_key('gen') for i in self.familyDict['individualID']].count(True) == len(self.familyDict['individualID'])
        except Exception:
            probIDs = list(set(indIDs).symmetric_difference(set(self.indsAddedGenInfo)))
            self.addGenInfo(indIDs = probIDs)
        return
    
    
    def _funcGen(self, relativeID, relativeGen):
        if relativeID != '0' and relativeID not in self.indsAddedGenInfo:
            # assign generation info for indID's relative
            self.famInfo[relativeID]['gen'] = relativeGen
            self.indsAddedGenInfo.append(relativeID)
            # assign gen info for relative's relatives recursively
            self._setGen(indID=relativeID, gen=relativeGen)
        return
    
        
    def _setGen(self, indID, gen=1):
        '''
        set genenration info to direct relatives (parents, spouse and offspring) of a given ind recursively
        until all relatives of that ind have been successfully assigned gen info
        '''
        # father
        fatherID = self.famInfo[indID]['fatherID']
        self._funcGen(relativeID=fatherID, relativeGen=gen-1)
        # mother
        motherID = self.famInfo[indID]['motherID']
        self._funcGen(relativeID=motherID, relativeGen=gen-1)
        # spouses
        spouseIDs = self.famInfo[indID]['spouseIDs']
        [self._funcGen(relativeID=i, relativeGen=gen) for i in spouseIDs]
        # offspring
        childIDs = self.famInfo[indID]['childIDs']
        [self._funcGen(relativeID=i, relativeGen=gen+1) for i in childIDs]
        return    
        
    
    def idxByID(self, indID):
        return self.familyDict['individualID'].index(indID)
    
    
    def isMale(self, indID, maleCoding=['1', 'M', 'male', 'MALE']):
        sex = self.familyDict['sex'][self.idxByID(indID)]
        return True if sex in maleCoding else False
    
    
    def isFemale(self, indID, femaleCoding=['2', 'F', 'female', 'FEMALE']):
        sex = self.familyDict['sex'][self.idxByID(indID)]
        return True if sex in femaleCoding else False
            
    
    def _getIndices(self, element, myList):
        return [i for i, x in enumerate(myList) if x == element]
    
    
    def getFatherID(self, indID):
        if indID not in self.familyDict['individualID']:
            return '0'
        return self.familyDict['fatherID'][self.idxByID(indID)]
    
    
    def getMotherID(self, indID):
        if indID not in self.familyDict['individualID']:
            return '0'
        return self.familyDict['motherID'][self.idxByID(indID)]
    
    
    def getFatherFatherID(self, indID):
        fatherID = self.getFatherID(indID)
        return self.getFatherID(fatherID)
    
    
    def getFatherMotherID(self, indID):
        fatherID = self.getFatherID(indID)
        return self.getMotherID(fatherID)
    
    
    def getMotherFatherID(self, indID):
        motherID = self.getMotherID(indID)
        return self.getFatherID(motherID)
    
    
    def getMotherMotherID(self, indID):
        motherID = self.getMotherID(indID)
        return self.getMotherID(motherID)
    
    
    def getChildIDs(self, indID):
        # if male 
        if self.isMale(indID):
            offspringIdxes = self._getIndices(indID, self.familyDict['fatherID'])
        # if female
        elif self.isFemale(indID):
            offspringIdxes = self._getIndices(indID, self.familyDict['motherID'])
        # if unknown
        else:
            return []
        return [x for i,x in enumerate(self.familyDict['individualID']) if i in offspringIdxes]
        
    
    def getSpouseIDs(self, indID):
        '''
        For an individual it is possible to have multiple spouses
        '''
        childIDs = self.getChildIDs(indID)
        # return [] if individual does not have any offspring
        if len(childIDs) == 0:
            return []
        # if male
        if self.isMale(indID):
            tmp = list(set([self.getMotherID(x) for x in childIDs]))
        # if female
        elif self.isFemale(indID):
            tmp = list(set([self.getFatherID(x) for x in childIDs]))
        else:
            return []
        # remove '0' if any
        if '0' in tmp:
            tmp.remove('0')
        return tmp
    

class readFiles():
    '''
    This class consists of functions that read multiple types of files
    '''
    def __init__(self, path=None, *args, **kwargs): 
        if path is not None:
            os.chdir(path)
    
    def _readlines(self, fileName, suffix):
        '''
        read file and return lines of strings
        '''
        # if filename ends with suffix remove suffix
        if fileName.endswith(suffix):
            fileName = fileName[:-(len(suffix)+1)]
        try:
            fi = open(fileName+'.'+suffix, 'r')
            lines = fi.readlines()
            fi.close()
            return lines
        except Exception:
            raise ValueError("Cannot find %s" % fileName+'.'+suffix)
            
    
    def _splitLine(self, line, sep=' '):
        '''
        split a single-line string by 'sep' and remove the end of line '\n'
        '''
        tmp = line.rstrip('\n')
        return tmp.split(sep)
                    
    
    def _recodeTraitInfo(self, trait):
        '''
        recode 'nan, na, none, null' to nan, otherwise to numeric value
        '''
        try:
            if trait.lower() in ('na', 'null', 'none', 'nan', 'missing', 'n/a'):
                return '0'
            else:
                return trait
        except:
                return trait
    
    
    def ped(self, pedFileName):
        '''
        read *.ped file and return a dict obj 'pedInfo{}' with keys as family ids.
        Each value of 'pedInfo{}' is a dict obj with lists of info,
        such as person ids, father ids, mother ids, gender and trait phenotype,
        for all individuals included in the corresponded family.
        Note! Only information contained in the first 6 columns will be parsed and useful.
        '''
        lines = self._readlines(pedFileName, 'ped')
        pedInfo = {}
        for l in lines:
            tmp = self._splitLine(l, ' ')
            try: 
                familyID, individualID, fatherID, motherID, sex, trait = tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], self._recodeTraitInfo(tmp[5])
                if pedInfo.has_key(familyID):
                    pedInfo[familyID]['individualID'].append(individualID)
                    pedInfo[familyID]['fatherID'].append(fatherID)
                    pedInfo[familyID]['motherID'].append(motherID)
                    pedInfo[familyID]['sex'].append(sex)
                    pedInfo[familyID]['trait'].append(trait)
                else:
                    pedInfo[familyID] = {'individualID':[individualID],
                        'fatherID':[fatherID],
                        'motherID':[motherID],
                        'sex':[sex],
                        'trait':[trait]}    
            except: # skip lines of comments in ped file
                continue
        return pedInfo
    
    
if __name__ == '__main__':
    import sys
    pedFile = sys.argv[1]
    pedInfo = readFiles().ped(pedFile)
    familyIDs = pedInfo.keys()
    familyDicts = pedInfo.values()
    #
    familyInfo = {}
    for ID, famDict in zip(familyIDs, familyDicts):
        familyInfo[ID] = restoreStruct(ID, famDict).famInfo
    print familyInfo
    
    
    
