base_code = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dp = 4
esp = 1.0/(10**dp)
# NOTE: invalidity of number & base are not checked, base 2 might have 23467890 etc
# NOTE: Input does not accept HEX currently

# validator: return false if validate successfully
def validate_number(number):
    return (number.count('.') > 1)
def validate_base(base_from, base_to):
    return not((base_to.isdigit()) and (base_from.isdigit()))

# map [0,1,2] -> [(0,1),(1,2)]: [(digit_before_start, digit_before_end),...] & [0,1] -> [(0,1)]
def enumerator_for_split_number(arr):
    res = []
    index = 0
    for item in arr[0:len(arr)-1]:
        index+=1
        if(index == 0):
            res.append((item, arr[index]))
        else:
            res.append((item+1, arr[index]))
    return res

def biggest_index(base, number):
    i=0
    while(1):
        if(base**i>number):
            break
        else:
            i+=1
    return i-1

def get_symbol(number): # 10->"A", 11->"B"
    if(number == '.'):
        return '.'
    return base_code[int(number)]

def get_value(symbol):
    if(number == '.'):
        return '.'
    return base_code.index(symbol)

while(1):
    number=raw_input("number? ")
    if(number.strip() == ''):
        print "bye"
        break
    base_from=raw_input("base from? ")
    if(base_from.strip() == ''):
        print "bye"
        break
    base_to=raw_input("base to? ")
    if(base_to.strip() == ''):
        print "bye"
        break
    if(validate_base(base_from, base_to)):
        print "incorrect base format"
    elif(validate_number(number)):
        print "incorrect number format"
    else: # there is no problem for the format of input
        # get information of the number string
        number_of_dot = number.count('.') # actually will be 0 or 1
        number_splitted = number.split('.')
        digit_length_splitted_by_dot = map(lambda x: len(x), number.split('.'))
        total_digit_length = reduce(lambda x,y: x+y,digit_length_splitted_by_dot)
        endIndex = 0
        if (len(digit_length_splitted_by_dot) == 2):
            endIndex = -digit_length_splitted_by_dot[1]
        else:
            endIndex = 0
        index = 0
        step_1 = ''
        print(number+" in base-"+base_from)
        # step 1: decompose the number into base 10 first
        step_1_answer = 0
        if(number_of_dot == 0):
            for digit in number_splitted[0]:
                digit = get_value(digit)
                index += 1
                if(index == total_digit_length):
                    step_1 += str(digit)+' * '+base_from+'^('+str(total_digit_length-index)+')'
                    step_1_answer += int(digit)*(int(base_from)**(total_digit_length-index))
                else:
                    step_1 += str(digit)+' * '+base_from+'^('+str(total_digit_length-index)+') + '
                    step_1_answer += int(digit)*(int(base_from)**(total_digit_length-index))
        else:
            # before dot
            for digit in number_splitted[0]:
                digit = get_value(digit)
                index += 1
                step_1 += str(digit)+' * '+base_from+'^('+str(digit_length_splitted_by_dot[0]-index)+') + '
                step_1_answer += int(digit)*(int(base_from)**(digit_length_splitted_by_dot[0]-index))
            # after dot
            index = 0
            for digit in number_splitted[1]:
                digit = get_value(digit)
                index -= 1
                if(index == -digit_length_splitted_by_dot[1]):
                    step_1 += str(digit)+' * '+base_from+'^('+str(index)+')'
                    step_1_answer += int(digit)*(int(base_from)**(index))
                else:
                    step_1 += str(digit)+' * '+base_from+'^('+str(index)+') + '
                    step_1_answer += int(digit)*(int(base_from)**(index))
        print('= '+step_1)
        print('= '+str(step_1_answer)+" in base-10")
        # step 2: reconstruct the number in base_to
        # NOTE: currently is incorrect for decimal
        step_2 = '' # if base > 10, then will need String
        step_2_answer = []
        index = biggest_index(int(base_to), step_1_answer)
        while(1):
            # step_2_answer/(int(base_to)**index)
            # print (step_1_answer, base_to, index)
            coeff = int(step_1_answer/(int(base_to)**index))
            # FIXME: if coeff == 0 don't add to step
            step_2 += str(coeff)+" * "+base_to+"^("+str(index)+") + "
            if(index == -1):
                step_2_answer.append('.')
            step_2_answer.append(coeff)
            step_1_answer -= coeff*int(base_to)**index
            index -= 1
            if(step_1_answer <= esp and (index<endIndex or index<=-3)):
                step_2 = step_2[:-3]
                break
        print('= '+step_2)
        print('= '+''.join(map(get_symbol,step_2_answer))+' in base-'+base_to)
        print ''
        # step 3: show result
