import re
# NOTE: all rules for version string validity and precedence are from https://semver.org/spec/v2.0.0.html ****************************

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
    #print ("both are valid")
    return std_list


def rule9(string):
        # rule 9: A pre-release version MAY be denoted by appending a hyphen and a series of dot separated identifiers immediately following the patch version.
        # Identifiers MUST comprise only ASCII alphanumerics [0-9A-Za-z]. Identifiers MUST NOT be empty. Numeric identifiers MUST NOT include leading zeroes.
         
        # only ascii alphanumerics and hypen
        invalid = "[^0-9A-Za-z\.]"
        
        # check that only one identifier and it is non empty
        spl_str = string.split('-')
        if len(spl_str) > 2 or '' in spl_str:
            #print ("yo")
            return -1
        identifier = spl_str[1]
        match = re.search(invalid,identifier)
        if match:
            return -1 # invalid
        #print ("pre_rel is valid")
        return identifier
        

def prim_invalid_check(string):
    # check it has no invalid chars
    invalid_1 = "[^0-9A-Za-z-+\.]"
    # check it ends with only alphanumeric chars
    invalid_2 = "[^0-9A-Za-z]$"
    if (re.search(invalid_1,string) is not None or re.search(invalid_2,string) is not None):
        return -1 # invalid
    return 1

def remove_build_meta_data(string):
    if '+' in string:
        ret = string.split('+')
        if len(ret) > 2 or '' in ret: # i.e more than one occurence of '+', -> invalid
            print ("here")
            return -1
        return ret[0]
    return string

def method(string1, string2):
    print ("input strings: ", string1, " ", string2)
    
    # check 0: make sure no invalid char in string
    if prim_invalid_check(string1) < 1:
        print (string1, " is invalid")
        return
    if prim_invalid_check(string2) < 1:
        print (string2, " is invalid")
        return
    # check for meta-data info, if present (in correct format) remove it. this data is irrelevant for precedence check. as per rule 10
    build_check = remove_build_meta_data(string1)
    if type(build_check) is int and build_check < 1:
        print (string1, " is invalid")
        return
    string1 = build_check
    build_check = remove_build_meta_data(string2)
    if type(build_check) is int and build_check < 1:
        print (string2, " is invalid")
        return
    string2 = build_check

    # check 1
    std_list = rule2(string1,string2)
    if type(std_list) is int:
        if std_list == 1:
            print (string1, " is invalid")
            return
        else:
            print (string2, " is invalid")
            return

    # passed check 1, do precedence check (if difference found here, can avoid looking at rest of strings)
    std_prec = maj_min_patch_precedence(std_list[0],std_list[1])
    #print ("does it get here")
    #print (std_prec)
    if std_prec > 0:
        print (string1, " is greater")
        return
    elif std_prec < 0:
        print (string2, " is greater")
    else:
        #print ("then here")
        # X.Y.Z for both strings are equal,check for pre_rel info, if present, check if valid  # check 2
        if '-' in string1 and '-' in string2:
            # both strings have pre-rel info, check if their valid
            #print ("both have pre_rel")
            pre_rel_1 = rule9(string1)
            #print ("gets here")
            if type(pre_rel_1) is int and pre_rel_1 < 1:
                print (string1, " is invalid")
                return
            pre_rel_2 = rule9(string2)
            if type(pre_rel_2) is int and  pre_rel_2 < 1:
                print (string2, " is invalid")
                return

            # both are valid, check precedence
            pre_prec = pre_rel_precedence(pre_rel_1, pre_rel_2)
            if pre_prec > 0:
                print (string1, " is greater")
                return
            elif pre_prec < 0:
                print (string2, " is greater")
            else:
                print ("both strings are equal")

        elif '-' in string1 and '-' not in string2:
            # pre_rel info only in string1, check if in valid format
            pre_rel_1 = rule9(string1)
            if type(pre_rel_1) is int and  pre_rel_1 < 1:
                print (string1, " is invalid")
                return
            # as per rule 9: Pre-release versions have a lower precedence than the associated normal version
            print (string2, " is greater")
        elif '-' in string2 and '-' not in string1:
            # pre_rel info only in string2, check if in valid format
            pre_rel_2 = rule9(string2)
            if type(pre_rel_2) is int and pre_rel_2< 1:
                print (string2, " is invalid")
                return
            # as per rule 9: Pre-release versions have a lower precedence than the associated normal version
            print (string1, " is greater")
        else:
            # both strings have same X.Y.Z info and same pre_rel info
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
        # do alphabetical ordering check
        prec = alphaCheck(str1,str2)
        if prec > 0:
            return 1
        elif prec < 0:
            return -1
        else:
            continue
        
    return 0



# alpha sort check
def alphaCheck(input1, input2):
    if input1 == input2:
        return 0
    sort_seq = sorted([input1,input2])
    if input1 == sort_seq[0]:
        return -1
    else:
        return 1

def maj_min_patch_precedence(input1,input2):
    # as per rule 11: precedence is determined by the first difference when comparing each of these identifiers from left to right as follows: 
    # Major, minor, and patch versions are always compared numerically.
    # method returns 1 if string 1 is greater, -1 if string 2 is greater, 0 if both equal
    for str1,str2 in zip(input1.split('.'),input2.split('.')):
        if int(str1)>int(str2):
            return 1
        elif int(str2)>int(str1):
            return -1
    return 0

def test_cases():
    # invalid strings
    s1_inv = ["123", "1.0.0.@#$","1.0.0.", "1.0.o-alpha", "1..0.0","alhpa-1.0.0","1.0.0-","1.0.0+","1.0.0", "1.0.0-alhpa.,,."]
    s2 = "1.0.0"
    # greater than strings
    s1_gre = ["1.0.0-alpha" , "1.0.0-alpha.1" , "1.0.0-alpha.beta" , "1.0.0-beta" , "1.0.0-beta.2" , "1.0.0-beta.11" , "1.0.0-rc.1"]
    # equal string
    s1_eq = ["1.0.0-alpha.beta", "1.0.0-alpha.beta+1.1.0"]
    for s1 in s1_inv:
        method(s1,s2)
    for s1 in s1_gre:
        method(s1,s2)
    for s1 in s1_eq:
        s2 = "1.0.0-alpha.beta"
        method(s1,s2)


if __name__ == '__main__':
    s1 = "1.0.0-alpha+123132"
    s2 = "1.0.0-alpha"
    #method(s1,s2)
    test_cases()
