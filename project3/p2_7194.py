# Program written by Thomas Li
# From 14 October 2019 to

from scipy.io import arff

# indicators for the range of certain attributes
_numeric = "numeric"
_nominal = "nominal"

class Dataset:
    # array of data items generated from scipy library
    # can be accessed by index, returning the attributes for single item
    # or by attribute label, returning every value of the attribute in the set
    instances = []
    
    # all attributes are marked as either numeric (continuous) or nominal
    # (discrete), with the range of values determined by what shows up in
    # the dataset
    attributeNames = ()
    attributeTypes = ()

    # since classification involves discrete labels (as opposed to prediction),
    # the class is assumed to contain a set of nominal values
    className = ""
    classVals = ()
    
    # attempt to retrieve .arff file contents and convert into data object
    # return whether or not file operation was sucessful
    def get_from_arff(self, filename):
        try:
            data, metadata = arff.loadarff(filename)
            labels = metadata.names()
            types = metadata.types()
            
            self.instances = data
            self.attributeNames = labels[0:-1]
            self.className = labels[-1]
            self.attributeTypes = types[0:-1]

            self.classVals = set([X[-1] for X in data])
            
            return True
        
        except FileNotFoundError as e:
            print(e)
            return False

class Classifier:
    # store instances of each attribute value for items of each class value
    # in the dataset in addition to whether an attribute is numeric or nominal
    # to allow the calculation of conditional inverse probabilities
    instances = {}
    types = []
    labels = []

    # store prior probabilities of each class value
    prior = {}

    # obtain attribute instances and probabilities from dataset
    def get_from_dataset(self, dataset):
        self.instances = {c : [[X[i] for X in dataset.instances
                                if X[-1] == c]
                               for i in range(len(dataset.attributeTypes) - 1)]
                          for c in dataset.classVals}
        self.types = dataset.attributeTypes
        self.labels = dataset.attributeNames
        self.prior = {c : len([X
                               for X in dataset.instances
                               if X[-1] == c])
                          / len(dataset.instances)
                      for c in dataset.classVals}
        return

    # write .bin file using classification data
    def write_to_bin(self, filename):
        return
    # attempt to retrieve classification data from .bin file
    # return whether or not file operation was successful
    def get_from_bin(self, filename, dataset):
        return

    # get p(c) for a single classification c given classification data
    def get_prior(self, c):
        return self.prior[c]
    
    # get p(x|C) for a single hypothesis x and single classification c
    def get_inverse(self, attributeIndex, x, c):
        # conditional set of attribute values classified as c
        vals = self.instances[c][attributeIndex]
        
        if self.types[attributeIndex] == _numeric:
            # continuous values - get probability through statisical methods
            return 1
        else:
            # discrete values - get probability through number of occurences
            return len([v for v in vals if v == x]) / len(vals)
        
    # get p(C|X) for a given instance X and a given class c
    def get_posterior(self, X, c):
        p = self.get_prior(c)
        for i in range(len(self.types) - 1):
            p *= self.get_inverse(i, X[i], c)
        return p

    # return c with highest p(c|X) among all classes in C for given instance X
    def classify(self, X):
        C = self.prior
        maxC = None
        maxP = 0
        
        for c in C:
            p = self.get_posterior(X, c)
            if p > maxP:
                maxP = p
                maxC = c
            
        return maxC

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

    # 2)
    print("Generating dataset...")
    if not _dataset.get_from_arff(dataFile):
        return

    # 3)
    print("Generating classifier...")
    _classifier.get_from_dataset(_dataset)

    # 4)
    print("Saving classifier...")
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
    # a1)
    # a2) prompt user for value of each attribute
    # a3) apply classifier to case and output result
    # a3) return to submenu
    # b1) return to menu
    return

# driver function
def py_nb():
    menu()
