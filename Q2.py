import re

def rule2(string1, string2):
    # rule 2 of semantic version (2.0.0)
    # A normal version number MUST take the form X.Y.Z where X, Y, and Z are non-negative integers, and MUST NOT contain leading zeroes. 
    # X is the major version, Y is the minor version, and Z is the patch version. Each element MUST increase numerically.
    # method returns 1 if string 1 is in invalid format, 2 if string 2 is in invalid format. if both are valid, returns the X.Y.Z part of both strings 

    standard = "^[1-9][0-9]*\.[0-9]+\.[0-9]+" # if string doesn't have a match then its an invalid string
    std_list = [] # store the X.Y.Z version string here (if it is valid)
    match1 = re.search(standard,string1)
    if not match1:
        return 1
    match2 = re.search(standard,string2)
    if not match2:
        return 2
    std_list.append(match1.group())
    std_list.append(match2.group())

    # second, make sure none of Y,Z don't have a leading zero (already checked X does not lead with a 0)
    for i,string in enumerate(std_list):
        spl_str = string.split('.')
        for val in spl_str:
            if len(val)>1 and val[0] == '0':
                if i == 0:
                    return 1
                else:
                    return 2
    return std_list


#def rule9(string1,string2):


def method(string1, string2):
#    # rule 2 of semantic version (2.0.0)
#    # A normal version number MUST take the form X.Y.Z where X, Y, and Z are non-negative integers, and MUST NOT contain leading zeroes. X is the major version, Y is the minor version, and Z is the patch version. Each element MUST increase numerically. 
#    # first, strings must start with X.Y.Z
#    standard = "^[1-9][0-9]*\.[0-9]+\.[0-9]+"
#    # if string doesn't have a match then its an invalid string
#    std_list = []
#    for string in (string1,string2):
#        match = re.search(standard,string)
#        if not match:
#            print (string + " is invalid check 1")
#            return 
#        std_list.append(match.group())
#    
#    # second, make sure none of Y,Z don't have a leading zero (already checked X does not lead with a 0)
#    for string in std_list:
#        spl_str = string.split('.')
#        for val in spl_str:
#            if len(val)>1 and val[0] == '0':
#                print (string + " is invalid check 2")

    std_list = rule2(string1,string2)

    # now, compare X.Y.Z  version strings (if difference found here, can avoid looking at rest of strings)
    std_prec = maj_min_patch__precedence(std_list[0],std_list[1])
    if std_prec > 0:
        print (string1, " is greater")
        return
    elif std_prec < 0:
        print (string2, " is greater")
    else:
        # rule 9: A pre-release version MAY be denoted by appending a hyphen and a series of dot separated identifiers immediately following the patch version. 
        # Identifiers MUST comprise only ASCII alphanumerics and hyphen [0-9A-Za-z-]. Identifiers MUST NOT be empty. Numeric identifiers MUST NOT include leading zeroes.
        # need to refactor rule9 validity check!
        if '-' in string1 and '-' in string2:
            # both strings have pre-rel info

            #print ("need to do pre-version precedence checks")
            pre_rel = []
            for string in (string1,string2):
                temp = string.split('-')
                if len(temp) > 2:
                    print (string, " is invalid check 3")
                else:
                    pre_rel.append(temp[1])

            pre_prec = pre_rel_precedence(pre_rel[0],pre_rel[1])
            if pre_prec > 0:
                print (string1, " is greater")
                return
            elif pre_prec < 0:
                print (string2, " is greater")
            else:
                print ("both strings are equal")

        elif '-' in string1 and '-' not in string2:
            print (string2, " is greater")
        elif '-' in string2 and '-' not in string1:
            print (string1, " is greater")
        else:
            print ("both strings equal")
                

def pre_rel_precedence(input1,input2):
    # make them both same length
    split_1 = input1.split('.')
    split_2 = input2.split('.')
    while(len(split_1)<len(split_2)): split_1.append("\0")
    while(len(split_2)<len(split_1)): split_2.append("\0")

    for str1, str2 in zip(split_1,split_2):
        if str1 is not "\0" and str2 is not "\0":
            if str1.isdigit() and str2.isdigit():
                # if they are both digits, do numerical sort check
                if int(str1) > int(str2):
                    return 1
                elif int(str2) > int(str1):
                    return -1
            elif str1.isdigit() and not str2.isdigit():
                return -1
            elif str2.isdigit() and not str1.isdigit():
                return 1
        # do alpha sort check
        prec = alphaCheck(str1,str2)
        if prec > 0:
            return 1
        elif prec < 0:
            return -1
        else:
            continue
        
    return 0



# mght have to rename method
def alphaCheck(input1, input2):
    print ("hereere")
    print (input1, input2)
    if input1 == input2:
        print ("returning")
        print (input1, input2)
        return 0
    print ("but here")
    sort_seq = sorted([input1,input2])
    print (sort_seq, "here")
    if input1 == sort_seq[0]:
        return -1
    else:
        return 1

def maj_min_patch_precedence(input1,input2):
    # Precedence is determined by the first difference when comparing each of these identifiers from left to right as follows: Major, minor, and patch versions are always compared numerically.
    # method returns 1 if string 1 is greater, -1 if string 2 is greater, 0 if both equal
    for str1,str2 in zip(input1.split('.'),input2.split('.')):
        if int(str1)>int(str2):
            return 1
        elif int(str2)>int(str1):
            return -1
    return 0




if __name__ == '__main__':
    s1 = "1.0.0"
    s2 = "1.0.0-rc.1"
    method(s1,s2)
