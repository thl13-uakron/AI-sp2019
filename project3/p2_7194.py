# Program written by Thomas Li
# From 14 October 2019 to

from scipy.io import arff

# indicators for the range of certain attributes
_numeric = "<f8"

class Dataset:
    instances = []
    attributeNames = ()
    attributeRanges = ()
    className = ""
    classRange = None
    
    # attempt to retrieve .arff file contents and convert into data object
    # return whether or not file operation was sucessful
    def get_from_arff(self, filename):
        try:
            data, metadata = arff.loadarff(filename)
            
            self.instances = data
            
            return True
        
        except FileNotFoundError as e:
            print(e)
            return False

class Classifier:
    # store probabilities of p(x) and p(x|c) for all hypothoses x and all
    # classes c in the given dataset
    prior = {}
    inverse = {}
    def get_from_dataset(self, dataset):
        return

    # write .bin file using classification data
    def write_bin(self, filename):
        return
    # attempt to retrieve classification data from .bin file
    # return whether or not file operation was successful
    def get_from_bin(self, filename, dataset):
        return

    # get p(x) for a single hypothesis x given classification data
    def get_prior(self, x):
        return
    # get p(x|C) for a single hypothesis x and single class c
    def get_inverse(self, x, c):
        return
    # get p(C|X) for a given instance X and a given class c
    def get_posterior(self, X, c):
        return

    # return c with highest p(c|X) among all classes in C for given instance X
    def classify(self, X, C):
        return

# classification info stored in local memory
_dataset = Dataset()
_classifier = Classifier()

# menu function
def menu():
    while True:
        print("\n(1) Generate New Classifier")
        print("(2) Load and Test Classifier")
        print("(3) Enter New Cases")
        print("(4) Quit")

        choice = input("Select An Option: ")

        if choice == "1":
            learn_classifier()
        elif choice == "2":
            load_and_test()
        elif choice == "3":
            test_new_cases()
        elif choice == "4":
            return
        else:
            print("Invalid Selection. Please Try Again.")

# first menu option
def learn_classifier():
    # 1) get user input for name of .arff input file
    # 2) process contents of input file
    # 3) generate naive bayesian classifier from input data
    # 4) save output data to .bin file with same name as input file
    global _dataset, _classifier

    # 1)
    dataFile = input("\nEnter the name of the file containing the dataset (.arff): ")
    if not _dataset.get_from_arff(dataFile):
        return

    # 2)
    print(_dataset.instances)

    # 3)

    # 4)
    classifierFile = dataFile.replace(".arff", ".bin")
    print("Classifier information saved to " + classifierFile)
        
    return

# second menu option
def load_and_test():
    # 1) get user input for name of previously saved .bin file containing classification model
    # 2) get user input for name of .arff file containing testing data
    # 3) process contents of model file and testing file
    # 4) apply classifier to training data and generate confusion matrix
    # 5) print confusion matrix
    return

# third menu option
def test_new_cases():
    # 1) generate submenu with options to a) apply the classifier to a new case or b) quit
    # 
    return

# driver function
def py_nb():
    menu()
