# Program written by Thomas Li
# From 14 October 2019 to 3 November 2019

# This is a program that can generate classification models for .arff files.
# For the scope of this project, this program only handles nominal attribute values.

from scipy.io import arff

# indicators for the range of certain attributes
_numeric = "numeric"
_nominal = "nominal"

# converting between bytes and strings
_encoding = "ASCII"

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
    # store inverse probabilities for each attribute value and class value
    inverse = {}

    # store the names and types of each attribute label
    types = []
    labels = []

    # store prior probabilities of each class value
    prior = {}

    # obtain attribute instances and probabilities from dataset
    def get_from_dataset(self, dataset):
        self.inverse = {c.decode(_encoding) :
                        [{x.decode(_encoding) :
                        len([case for case in cases if case[i] == x]) / len(cases)
                          for x in set(dataset.instances[dataset.attributeNames[i]])
                          for cases in [[h for h in dataset.instances if h[-1] == c]]}
                         for i in range(len(dataset.attributeNames))]
                        for c in dataset.classVals}
        self.types = dataset.attributeTypes
        self.labels = dataset.attributeNames
        self.prior = {c.decode(_encoding) :
                      len([X for X in dataset.instances if X[-1] == c])
                      / len(dataset.instances)
                      for c in dataset.classVals}
        return

    # view the set of available classes
    def get_classes(self):
        return [c for c in self.inverse]
    
    # view the set of recorded values for a particular attribute across all classes
    def get_unique_attribute_values(self, i):
        return [h for h in self.inverse[self.get_classes()[0]][i]]

    # write .json file using classification data
    def write_to_file(self, filename):
        return
    
    # attempt to retrieve classification data from .json file
    # return whether or not file operation was successful
    def get_from_file(self, filename):
        return False

    # get p(c) for a single classification c given classification data
    def get_prior(self, c):
        return self.prior[c]
    
    # get p(x|C) for a single hypothesis x and single classification c
    def get_inverse(self, attributeIndex, x, c):
        # conditional set of attribute values classified as c
        if self.types[attributeIndex] == _numeric:
            # continuous values - get probability through statisical methods
            return 1
        else:
            # discrete values - get probability through number of occurences
            return self.inverse[c][attributeIndex][x]
        
    # get p(C|X) for a given instance X and a given class c
    def get_posterior(self, X, c):
        prob = self.get_prior(c)
        for i in range(len(self.types) - 1):
            prob *= self.get_inverse(i, X[i], c) if X[i] in self.get_unique_attribute_values(i) else 1
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
        self.matrix = {c1 : {c2 : 0 for c2 in classifier.get_classes()}
                       for c1 in classifier.get_classes()}

        # fill values and calculate accuracy
        
        for i in range(len(dataset.instances)):
            actual = dataset.instances[dataset.className][i].decode(_encoding)
            classified = classifier.classify([x.decode(_encoding) for x in dataset.instances[i]])
            
            self.matrix[actual][classified] += 1
            self.accuracy += 1 if actual == classified else 0

        self.accuracy /= len(dataset.instances)
        

    # display and format contents of matrix
    def print(self):
        [print(c1 + " :",
               {c2 : self.matrix[c1][c2]
                for c2 in self.matrix[c1]})
         for c1 in self.matrix]
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
        print("[RuntimeError] Input file not found")
        return

    # 3)
    print("Generating classifier...")
    _classifier.get_from_dataset(_dataset)

    # 4)
    print("Saving classifier...")
    classifierFile = dataFile.replace(".arff", ".json")
    _classifier.write_to_file(classifierFile)
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
    classifierFile = input("\nEnter the name of the classifier file (.json) to load, or leave the field empty to use the existing classifier: ")
    if _classifier.get_from_file(classifierFile):
        print("Classifier loaded from file " + classifierFile)
    elif classifierFile == "":
        print("Blank input. Using currently loaded classification model...")
    else:
        print("Input file not found. Using currently loaded classification model...")
        
    if len(_classifier.get_classes()) == 0:
        print("[RuntimeError] Classifier appears to contain no data")
        return

    # 2)
    global _dataset
    datasetFile = input("\nEnter the name of the dataset file (.arff) to load, or leave the field empty to use the existing dataset: ")
    if _dataset.get_from_arff(datasetFile):
        print("Dataset loaded from file " + datasetFile)
    elif classifierFile == "":
        print("Blank input. Using currently loaded dataset...")
    else:
        print("Input file not found. Using currently loaded dataset..")

    if len(_dataset.instances) == 0:
        print("[RuntimeError] Dataset appears to contain no data")
        return

    # 3)
    try:
        print("\nTesting...")
        _confusionMatrix = ConfusionMatrix(_dataset, _classifier)

        # 4)
        print("\nConfusion Matrix:")
        _confusionMatrix.print()
        print("Accuracy: {0}%".format(_confusionMatrix.accuracy * 100))
        
    except ZeroDivisionError:
        print("[ZeroDivisionError] Attempting to work with empty dataset")

    except KeyError:
        print("[KeyError] Attempting to work with classifier that doesn't match dataset")
    
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
    classifierFile = input("\nEnter the name of the classifier file (.json) to load, or leave the field empty to use the existing classifier: ")
    if _classifier.get_from_file(classifierFile):
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
        print("[RuntimeError] Classifier appears to contain no data")
        return

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
            print("")
            case = []

            try:
                # a1)
                if choice == "a":
                    case = [(input("Enter a value for {0} ({1}): ".format(x, attributeRanges[x]
                                                                          if attributeRanges[x] == _numeric
                                                                          else [h for h in attributeRanges[x]]
                                                                          ))
                             ) for x in attributeRanges]
                
                # b1)
                if choice == "b":
                    prompt = "Enter the values for"
                    for x in attributeRanges:
                        prompt = prompt + "\n{0} (values: {1}), ".format(x, attributeRanges[x]
                                                               if attributeRanges[x] == _numeric
                                                               else [h for h in attributeRanges[x]
                                                                     ])
                    prompt = prompt + "\neach separated by a single space: "
                    case = input(prompt).split(" ")
                    
                # ab2)
                classification = _classifier.classify(case)
                print("\nCase {0} was classified as [{1}]".format([x for x in case], classification))
                if classification == None:
                    print("The case being classified as None means that either every class has a probability of 0 or there are no classes.")
                
                
            except IndexError:
                print("[IndexError] The entered case appears to not match the specified format")

        else:
            print("Invalid selection. Please try again.")
    
    return

# driver function
def py_nb():
    menu()
