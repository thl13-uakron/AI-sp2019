# Program written by Thomas Li
# From 14 October 2019 to

from scipy.io import arff

# menu function
def menu():
    while True:
        print("(1) Generate New Classifier")
        print("(2) Load and Test Classifier")
        print("(3) Enter New Cases")
        print("(4) Quit")

        choice = input("Select An Option: ")

        if choice == "1":
            learn_classifier()
        elif choice == "2":
            load_and_test()
        elif choice == "3":
            add_cases()
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
def add_cases():
    # 1) generate submenu with options to a) add new case or b) quit
    return

# driver function
def py_nb():
    menu()
