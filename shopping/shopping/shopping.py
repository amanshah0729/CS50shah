import csv
import sys
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.05


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    length1, length2, evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    print(length1)
    print(length2)


def load_data(filename):
    with open(filename, 'r') as f:
        next(f)
        a = csv.reader(f)
        evidence = []
        labels = []
        for row in a:
            if row[10] == "June":
                row[10] = "Jun"
            row[10] = datetime.strptime(row[10], '%b').month - 1
            if row[15] == "Returning_Visitor":
                row[15] = 1
            else: 
                row[15] = 0
            if row[16] == "TRUE":
                row[16] = 1
            else: 
                row[16] = 0
            
            labels.append(row.pop())
            evidence.append(row)

    for i in range(len(labels)):
        if labels[i] == "TRUE":
            labels[i] = int(1)
        else: 
            labels[i] = int(0)
    evidence = [list(map(float, sublist)) for sublist in evidence]


    #print(evidence)
    #print(type(evidence[9][2]))
    list1 = [i for i in labels if i == 0]
    len1 = len(list1)
    list2 = [i for i in labels if i == 1]
    len2 = len(list2)
    return (len1, len2, evidence, labels)



    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence, labels)
    return model
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """


def evaluate(labels, predictions):
    for item in predictions:
        print(item)
    total = 0
    correct = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            total += 1
            if predictions[i] == 1:
                correct += 1
    sensitivity = correct/total

    total1 = 0
    correct1 = 0
    for i in range(len(labels)):
        if labels[i] == 0:
            total1 += 1
            if predictions[i] == 0:
                correct1 += 1
    specificity = correct1/total1
    return (sensitivity, specificity)
    """
    
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    raise NotImplementedError


if __name__ == "__main__":
    main()
