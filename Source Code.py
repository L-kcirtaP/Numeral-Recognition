
··· Python

import math
import time

'''------------------------------------|Handle the Data|------------------------------------'''

def data2vector(filename, vector = ''):
    f = open(filename, 'r')
    f = f.readlines()
    data = []
    for line in f:
        data.append(line.strip('\n'))
    vector_dic = {}
    vector_lst = []
    for i in data:
        if len(i.strip()) != 1:
            # Complete the 1024-dimensional vector.
            vector += i
        else:
            # Label the vectors with the corresponding number.            
            answer =int(i.strip())
            for v in vector:
                vector_lst.append(int(v))
            label = vector_dic.get(answer, [])
            label.append(tuple(vector_lst))
            vector_dic[answer] = label
            vector = ''
            vector_lst = []
    # Return the final dictionary: one number corresponds to some vector labels.
    return vector_dic

'''------------------------------------|Define the Computation|------------------------------------'''

def vector_add(v, w):
    """adds two vectors componentwise"""
    return [v_i + w_i for v_i, w_i in zip(v, w)]

def vector_subtract(v, w):
    """subtracts two vectors componentwise"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]

def vector_or(v, w):
    """boolean 'or' two vectors componentwise"""
    return [v_i or w_i for v_i, w_i in zip(v, w)]

def vector_and(v, w):
    """boolean 'and' two vectors componentwise"""
    return [v_i and w_i for v_i, w_i in zip(v, w)]

def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return sum(v_i * v_i for v_i in v)

def distance(v, w):
    s = vector_subtract(v, w)
    return math.sqrt(sum_of_squares(s))

def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))

def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def vector_sum(vectors):
    return reduce(vector_add, vectors)

def scalar_multiply(c, v):
    return [round(c * v_i,2) for v_i in v]

def vector_mean(vectors):
    """compute the vector whose i-th element is the mean of the
    i-th elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1 / n, vector_sum(vectors))

'''------------------------------------|Output the Training|------------------------------------'''

def output_train():
    training_dict = data2vector('digit-training.txt')
    print('   Beginning of training @ ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print('-' * 50)
    print('{: ^50}'.format('Training Info'))
    print('-' * 50)
    total = 0
    for number in range(10):
        print(' ' * 20 + str(number) + ' = ' + str(len(training_dict[number])))
        total += len(training_dict[number])
    print('-' * 50)
    print('  Total Sample = %d'%(total))
    print('-' * 50 + '\n')

'''------------------------------------|Define the Test Method|------------------------------------'''

def test(number):
    testing_vector = data2vector('digit-testing.txt')
    train_vector = data2vector('digit-training.txt')
    correct = 0

    training_mean = {}
    # Train using the mean of all vector, i.e. 1nn model.
    for i in range(10):
        training_mean[i] = vector_mean(train_vector[i])

    for value in range(len(testing_vector[number])):
        value_list = []
        for answer in range(10):
            value_list.append(squared_distance(testing_vector[number][value], training_mean[answer]))
        if value_list.index(min(value_list)) == number:
            correct += 1
    return correct

'''------------------------------------|Output the Test|------------------------------------'''
def output_test():
    testing_vector = data2vector('digit-testing.txt')
    print('-' * 50)
    print('{: ^50}'.format('Testing Info'))
    print('-' * 50)
    total_correct = 0
    total_test = 0
    for number in range(10):
        correct = test(number)
        total_correct += correct
        total_test += len(testing_vector[number])
        if correct != len(testing_vector[number]):
            print(' ' * 15 + str(number) + ' = ' + str(correct) + ',\t' + str(len(testing_vector[number]) - correct) + ',\t' + str('%.2f' % (correct / (len(testing_vector[number]))))[2:4] + '%')
        else:
            print(' ' * 15 + str(number) + ' = ' + str(correct) + ',\t' + str(0) + ',\t100%')
    print('-' * 50)
    print(' ' * 8 + 'Accuracy = ' + str(total_correct / total_test)[2:6][:2] + '.' + str(total_correct / total_test)[2:6][2:] + '%')
    print(' ' * 3 + 'Correct/Total = ' + str(total_correct) + '/' + str(total_test))
    print('-' * 50)
    print('     End of Training @ ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

'''------------------------------------|Make Predictions|------------------------------------'''

predict_vector = data2vector('digit-predict.txt')
def predict():
    global predict_vector
    global predict_list
    predict_list = []
    train_vector = data2vector('digit-training.txt')
    # Use the mean of training vectors to predict.
    training_mean = {}
    for i in range(10):
        training_mean[i] = vector_mean(train_vector[i])
    
    for array in range(len(predict_vector[0])):
        value_list = []
        for number in range(10):
            value_list.append(squared_distance(predict_vector[0][array], training_mean[number]))
        predict_list.append(value_list.index(min(value_list)))

'''------------------------------------|Output the Prediction|------------------------------------'''

def output_predict():
    predict()
    global predict_list
    print('-' * 50)
    print('{: ^50}'.format('Predictions by Machine:'))
    print('-' * 50)
    for pred in predict_list:
        print('{: ^50}'.format(pred))
    print('{:-^50}'.format('END'))

 ···
