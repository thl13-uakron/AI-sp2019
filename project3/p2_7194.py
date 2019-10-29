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
                               for i in range(len(dataset.attributeTypes))]
                          for c in dataset.classVals}
        self.types = dataset.attributeTypes
        self.labels = dataset.attributeNames
        self.prior = {c : len([X
                               for X in dataset.instances
                               if X[-1] == c])
                          / len(dataset.instances)
                      for c in dataset.classVals}
        return

    # view the set of recorded values for a particular attribute across all classes
    def get_unique_attribute_values(self, i):
        return set([x for c in self.instances for x in self.instances[c][i]])

    # view the set of available classes
    def get_classes(self):
        return [c for c in self.prior]

    # write .bin file using classification data
    def write_to_bin(self, filename):
        return
    
    # attempt to retrieve classification data from .bin file
    # return whether or not file operation was successful
    def get_from_bin(self, filename):
        return False

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
        prob = self.get_prior(c)
        for i in range(len(self.types) - 1):
            prob *= self.get_inverse(i, X[i], c)
        return prob

    # return c with highest p(c|X) among all classes in C for given instance X
    def classify(self, X):
        C = self.get_classes()
        maxC = None
        maxProb = 0
        
        for c in C:
            prob = self.get_posterior(X, c)
            if prob > maxProb:
                maxProb = prob
                maxC = c
            
        return maxC

class ConfusionMatrix:
    # matrix is 2d table in which cell (x, y) measures how many items in the
    # dataset of class x get classified as y using the classifier
    # instances where x == y indicate accurate classifications
    matrix = {}
    accuracy = 0

    # create matrix
    def __init__(self, dataset, classifier):
        # get structure 
        self.matrix = {c1 : {c2 : 0
                             for c2 in dataset.classVals}
                       for c1 in dataset.classVals}

        # fill values and calculate accuracy
        for i in range(len(dataset.instances)):
            actual = dataset.instances[dataset.className][i]
            classified = classifier.classify(dataset.instances[i])
            
            self.matrix[actual][classified] += 1
            self.accuracy += 1 if actual == classified else 0

        self.accuracy /= len(dataset.instances)

    # display and format contents of matrix
    def print(self):
        [print(c, self.matrix[c]) for c in self.matrix]
        return

# classification info stored in local memory
_dataset = Dataset()
_classifier = Classifier()

# menu function
def menu():
    while True:
        print("\n(1) Generate New Classifier")
        print("(2) Load and Test Classifier")
        print("(3) Classify New Cases")
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
        print("[Error] Input file not found")
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
    # 1) get user input for name of .bin file containing classification model, retrieve contents
    # 2) get user input for name of .arff file containing testing data, retrieve contents
    # 3) apply classifier to training data and generate confusion matrix
    # 4) print confusion matrix

    # 1)
    global _classifier
    classifierFile = input("\nEnter the name of the classifier file (.bin) to load, or leave the field empty to use the existing classifier: ")
    if _classifier.get_from_bin(classifierFile):
        print("Classifier loaded from file " + classifierFile)
    elif classifierFile == "":
        print("Blank input. Using currently loaded classification model...")
    else:
        print("Input file not found. Using currently loaded classification model...")

    # 2)
    global _dataset
    datasetFile = input("\nEnter the name of the dataset file (.arff) to load, or leave the field empty to use the existing dataset: ")
    if _dataset.get_from_arff(datasetFile):
        print("Dataset loaded from file " + datasetFile)
    elif classifierFile == "":
        print("Blank input. Using currently loaded dataset...")
    else:
        print("Input file not found. Using currently loaded dataset..")

    # 3)
    try:
        print("\nTesting...")
        _confusionMatrix = ConfusionMatrix(_dataset, _classifier)

        # 4)
        print("\nConfusion Matrix:")
        _confusionMatrix.print()
        print("Accuracy: {0}%".format(_confusionMatrix.accuracy * 100))
        
    except ZeroDivisionError:
        print("[Error] Attempting to work with empty dataset")

    except KeyError:
        print("[Error] Attempting to work with classifier that doesn't match dataset")
    
    return

# third menu option
def test_new_cases():
    # 1) prompt user for name of classifer file, retrieve contents (last loaded classifier used if no usable filename given)
    # 2) generate submenu with options to a) apply the classifier to a new case determined by entering each value individually,
    #    b), apply the classifier to a new case determined by a single text input or c) quit
    # a1), b1) prompt user for the attribute values as specified in the selection
    # ab2) apply classifier to case and output result
    # ab3) return to submenu
    # c1) return to menu

    # 1)
    global _classifier
    classifierFile = input("\nEnter the name of the classifier file (.bin) to load, or leave the field empty to use the existing classifier: ")
    if _classifier.get_from_bin(classifierFile):
        print("Classifier loaded from file " + classifierFile)
    elif classifierFile == "":
        print("Blank input. Using currently loaded classification model...")
    else:
        print("Input file not found. Using currently loaded classification model...")

    # used for input prompt
    attributeRanges = {_classifier.labels[i]:
                       _classifier.types[i] if _classifier.types[i] == _numeric
                       else _classifier.get_unique_attribute_values(i)
                       for i in range(len(_classifier.labels))}

    if (len(attributeRanges) == 0):
        print("[Error] Classifier appears to contain no data")

    # 2)
    while True:
        print("\n(A) Enter a New Case, Input by Attribute")
        print("(B) Enter a New Case, Single Input")
        print("(C) Return to Main Menu")

        choice = input("Select an Option: ")
        choice = choice.lower()

        if choice == "c":
            # c1)
            return
        
        elif choice in ("a", "b"):
            case = []
            # a1)
            
            # b1)

            # ab2)

            # ab3)

        else:
            print("Invalid selection. Please try again.")
    
    return

# driver function
def py_nb():
    menu()
