import pickle

def store_rst(decesion_tree,filename):

    writer = open(filename,'w')
    pickle.dump(decesion_tree,writer)
    writer.close()

def read_rst(filename):

    reader = open(filename,'rU')
    return pickle.load(reader)