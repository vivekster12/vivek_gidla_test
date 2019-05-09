def method(in1, in2):
    # identify the line that starts before
    if in1[0] < in2[0]:
        # input 1 starts before input 2
        line1 = in1
        line2 = in2
    elif in1[0] > in2[0]:
        line1 = in2
        line2 = in1
    else:
        # both lines have same start point ... -> overlap
        return True

    if line1[1] >= line2[0]:
        # end of input1 comes after or at the start of input2. ... -> overlap
            return True
        else:
            return False
