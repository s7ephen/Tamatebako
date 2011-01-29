#!/usr/bin/env python2.4
import matrix.matrix as mm
import pdb

class mmatrix(mm.matrix):
    def __init__(self, size):
       mm.matrix.__init__(self, size)

    def mean(self):
        """
            Return a mean vector as a list.
        """
        c,r = self.size(); float(c); float(r)
        mean_vector = []
        #the following should prolly be a list comprehension. --Stephen
        for i_c in range(c):
            column_tally = float(0)
            for i_r in range(r):
                column_tally += self[i_c, i_r]
                #print ("(%d, %d) %d %d") % (i_r, i_c, self[i_c, i_r], column_tally)
            #print "--------------"
            mean_vector.append(column_tally / r)
        print("Mean Vector:", repr(mean_vector))
        return(mean_vector)

    def covariance(self):
        """
            Return a variance/covariance matrix.
        """
        c,r = self.size(); float(c); float(r)
        mean_vector = self.mean()
        covariance_mat = mmatrix((c,r))
        for index_c in range(c):
            tally = float(0)
            for index2_c in range(c):
                for i in range(r):
                    #print self[index_c, i], self[index2_c, i]
                    tally += (self[index_c, i] - mean_vector[index_c])*(self[index2_c, i] - mean_vector[index_c])
                    print ("(%f - %f) * (%f - %f)") % (self[index_c, i], mean_vector[index_c], self[index2_c, i], mean_vector[index_c])
                    #print ("(%d, %d) %d") % (index_c, index2_c, tally)
                try:
                    temp = (1 / (r-1)) #'r' here is really "N" or 'number of observations
                except (ZeroDivisionError):
                    print("division by zero on this pairing.")
                    temp = 1
                #covariance_mat[index_c, index2_c] = float((tally/temp))
        
def get_user_matrix():
    """
        User is prompted for a series of values that are evaluated as a python
        list. A matrix object is formed based on this input and returned.
    """
    # I know its ugly to nest functions like this, but to show heirarchy in
    # help() docstrings, its kinda important.
    def _get_input(o_index):
        """
            Internal helper function...
        """
        user_list_str = raw_input("Observation #%d? " % (o_index))
        try:
            user_list = eval(user_list_str)
        except (SyntaxError, NameError):
            print "List syntax incorrect. Please re-enter"
            user_list = _get_input(o_index)
        return user_list 

    list_of_lists = user_list = list()
    homo_len = 0 #the number of features in each observation *MUST* be the same
    print "Reading observations in python list notation\n(ctrl-c or ctrl-d to stop)"
    o_index = 0 #observation counter
    while 1:
        try:
            user_list = _get_input(o_index)
            if (o_index == 0): #if first observation, set the standard
                homo_len = len(user_list)
                print "From now on I expect observations with only %d features" % (homo_len)
            if (len(user_list) == homo_len):
                list_of_lists.append(user_list)
                o_index+=1
            else:
                print "Warning, that observation did not have %d features. Please re-enter." % (homo_len)
                _get_input(o_index)
        except (KeyboardInterrupt, EOFError):
            print "\nBreak caught. Quitting observation input." 
            break
    observation_mat = mmatrix(list_of_lists)
    pdb.set_trace()
    return(observation_mat)

if __name__ == '__main__':
    user_matrix = get_user_matrix()
