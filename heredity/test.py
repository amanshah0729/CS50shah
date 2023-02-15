import csv
import itertools
import sys
from turtle import delay
import time

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    print("test")
    print(joint_probability1(people, {"Ginny"}, {}, {})) #
    print(joint_probability(people, {"Ginny"}, {}, {})) #
    print("end test")
    time.sleep(35)
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]



def joint_probability(people, one_gene, two_genes, have_trait):
    
    if len(one_gene) == 0:
        one_gene = set()
    if len(two_genes) == 0:
        two_genes = set()
    if len(have_trait) == 0:
        have_trait = set()


    """
    ret
   
   
   
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    onecounter = 1
    
    
    for name in one_gene:
        #print(name)
        #print(people[name]["mother"])
        if not people[name]["mother"]:
            onecounter = onecounter * PROBS["gene"][1]
            #print("Balls")
        else:
            if people[name]["mother"] in one_gene:
                if people[name]["father"] in one_gene:
                    onecounter = onecounter * 0.5
                elif people[name]["father"] in two_genes:
                    onecounter = onecounter * ((0.99 * 0.5) + (0.01 * .5 ))
                else:
                    onecounter = onecounter * ((0.01 * 0.5) + (0.5 * 0.99))

            elif people[name]["mother"] in two_genes:
                if people[name]["father"] in one_gene:
                    onecounter = onecounter * ((0.99 * 0.5) +( 0.01 * .5))
                elif people[name]["father"] in two_genes:
                    onecounter = onecounter * ((0.99 * 0.01) + (0.99 * 0.01))
                else:
                    onecounter = onecounter * ((0.99 * 0.99) + (0.01* 0.01))
            else:
                if people[name]["father"] in one_gene:
                    onecounter = onecounter * ((0.99 * 0.5) +( 0.01 * .5))
                elif people[name]["father"] in two_genes:
                    onecounter = onecounter * ((0.99 * 0.99) + (0.01* 0.01))
                    #print(onecounter)
                else:
                    print("Ginny was here")
                    onecounter = onecounter * ((0.01 * 0.99) + (0.01 * 0.99))


    twocounter = 1
    for name in two_genes:
        if people[name]["mother"] is None:
            twocounter = twocounter * PROBS["gene"][2]
            #print(twocounter)
        else:
            if people[name]["mother"] in one_gene:
                if people[name]["father"] in one_gene:
                    twocounter = twocounter * .25
                elif people[name]["father"] in two_genes:
                    twocounter = twocounter * (0.99 * 0.5)
                else:
                    twocounter = twocounter * (0.01 * 0.5)

            elif people[name]["mother"] in two_genes:
                if people[name]["father"] in one_gene:
                    twocounter = twocounter * (0.99 * 0.5)
                elif people[name]["father"] in two_genes:
                    twocounter = twocounter * (0.99 * 0.99)
                else:
                    twocounter = twocounter * (0.99 * 0.01)
            else:
                if people[name]["father"] in one_gene:
                    twocounter = twocounter * 0.5 * 0.01
                elif people[name]["father"] in two_genes:
                    twocounter = twocounter * 0.99 * 0.01
                else:
                    twocounter = twocounter * (0.01 * 0.01)
    
    zerocounter = 1
    
    
    empty = set()
    for name in people.keys():
        empty.add(name)
    temp = one_gene
    sloop = empty.difference(one_gene.union(two_genes))
    one_gene = temp

    #print("Text")
    print(sloop)

    for name in sloop: #use .isDifference() and union(). keys() may help read just keys. keys() i think creates an object which is not what i want
        if people[name]["mother"] is None:
            zerocounter = zerocounter * PROBS["gene"][0]
            print(name)
        else:
            print(name)
            if people[name]["mother"] in one_gene:
                if people[name]["father"] in one_gene:
                    zerocounter = zerocounter * .25
                elif people[name]["father"] in two_genes:
                    zerocounter = zerocounter * (0.01 * 0.5)
                else:
                    zerocounter = zerocounter * (0.99 * 0.5)
                    
            elif people[name]["mother"] in two_genes:
                if people[name]["father"] in one_gene:
                    zerocounter = zerocounter * 0.5 * 0.01
                elif people[name]["father"] in two_genes:
                    zerocounter = zerocounter * (0.01 * 0.01)
                else:
                    zerocounter = zerocounter * (0.99 * 0.01)
            else:
                if people[name]["father"] in one_gene:
                    zerocounter = zerocounter * (0.99 * 0.5)
                elif people[name]["father"] in two_genes:
                    zerocounter = zerocounter * 0.99 * 0.01
                else:
                    print("got here!")
                    zerocounter = zerocounter * (0.99 * 0.99)
    """

    traitcounter = 1
    for name in have_trait:
        #print("got here")
        if people[name]["trait"] == True:
            continue
        elif people[name]["trait"] == False: #comment this out if u want it to work. this is standard chance, use this (.01 * .65) + (.03 * .56) + (.96 * .01)
            traitcounter = 0
        else:
            if people[name]["mother"] is None:
                traitcounter = traitcounter * (.01 * .65) + (.03 * .56) + (.96 * .01)
            else:
                #bong
                
                if people[name]["mother"] in one_gene:
                    if people[name]["father"] in one_gene:
                        traitcounter = traitcounter * (.01 * .25 +  .56 * .5 + .65 * .25)
                    elif people[name]["father"] in two_genes:
                        traitcounter = traitcounter *(.01 * (0.01 * 0.5) + .56 * (0.99 * 0.5 + 0.01 * .5 ) + .65 * (0.99 * 0.5))
                    else:
                        traitcounter = traitcounter * (.01 * (0.99 * 0.5) + .56 * ((0.01 * 0.5) + (0.5 * 0.99)) + .65 * (0.01 * 0.5))
                    
                if people[name]["mother"] in two_genes:
                    if people[name]["father"] in one_gene:
                        traitcounter = traitcounter *(.01 * (0.5 * 0.01) + .56 * (0.99 * 0.5 + 0.01 * .5 ) + .65 * (0.99 * 0.5))
                    elif people[name]["father"] in two_genes:
                        traitcounter = traitcounter * (.01 * (0.01 * 0.01) + .56 * ((0.99 * 0.01) + (0.99 * 0.01)) + .65 * (0.99 * 0.99))
                    else:
                        traitcounter = traitcounter * (.01 * (0.99 * 0.01) + .56 *((0.99 * 0.99) + (0.01* 0.01)) + .65 * (0.99 * 0.01))
                else:
                    if people[name]["father"] in one_gene:
                        traitcounter = traitcounter * (.01 * (0.99 * 0.5) + .56 * ((0.01 * 0.5) + (0.5 * 0.99)) + .65 * (0.01 * 0.5))
                    elif people[name]["father"] in two_genes:
                        traitcounter = traitcounter * (.01 * (0.99 * 0.01) + .56 *((0.99 * 0.99) + (0.01 * 0.01)) + .65 * (0.99 * 0.01))
                        #print("traitcounter")
                    else:
                        traitcounter = traitcounter * (.01 * (0.99 * 0.99) + .56 *((0.01 * 0.99) + (0.01 * 0.99)) + .65 * (0.01 * 0.01))
    
    
    empty = set()
    for name in people.keys():
        empty.add(name)
    sloop1 = empty.difference(have_trait)
    #print(sloop1)
    for name in sloop1:
        if people[name]["trait"] == True:
            traitcounter = 0
        if people[name]["trait"] == False: #comment this out if u want it to work. this is standard chance, use this (.01 * .65) + (.03 * .56) + (.96 * .01)
            continue
        else:
            if people[name]["mother"] is None:
                traitcounter = traitcounter * (1 - ((.01 * .65) + (.03 * .56) + (.96 * .01)))
            else:
                #bong

                if people[name]["mother"] in one_gene:
                    if people[name]["father"] in one_gene:
                        traitcounter = traitcounter * (1-(.01 * .25 + .56 * .5 + .65 * .25))
                    elif people[name]["father"] in two_genes:
                        traitcounter = traitcounter *(1- (.01 * (0.01 * 0.5) + .56 * (0.99 * 0.5 + 0.01 * .5 ) + .65 * (0.99 * 0.5)))
                    else:
                        traitcounter = traitcounter * (1 -(.01 * (0.99 * 0.5) + .56 * ((0.01 * 0.5) + (0.5 * 0.99)) + .65 * (0.01 * 0.5)))
                    
                if people[name]["mother"] in two_genes:
                    if people[name]["father"] in one_gene:
                        traitcounter = traitcounter *(1 - (.01 * (0.5 * 0.01) + .56 * (0.99 * 0.5 + 0.01 * .5 ) + .65 * (0.99 * 0.5)))
                    elif people[name]["father"] in two_genes:
                        traitcounter = traitcounter * (1 -(.01 * (0.01 * 0.01) + .56 * ((0.99 * 0.01) + (0.99 * 0.01)) + .65 * (0.99 * 0.99)))
                    else:
                        traitcounter = traitcounter * (1 - (.01 * (0.99 * 0.01) + .56 *((0.99 * 0.99) + (0.01* 0.01)) + .65 * (0.99 * 0.01)))
                else:
                    if people[name]["father"] in one_gene:
                        traitcounter = traitcounter * (1- (.01 * (0.99 * 0.5) + .56 * ((0.01 * 0.5) + (0.5 * 0.99)) + .65 * (0.01 * 0.5)))
                    elif people[name]["father"] in two_genes:
                        traitcounter = traitcounter * (1 - (.01 * (0.99 * 0.01) + .56 *((0.99 * 0.99) + (0.01 * 0.01)) + .65 * (0.99 * 0.01)))
                    else:
                        traitcounter = traitcounter * (1 - (.01 * (0.99 * 0.99) + .56 *((0.01 * 0.99) + (0.01 * 0.99)) + .65 * (0.01 * 0.01)))
    """

    traitcounter = 1
    for name in have_trait:
        """if people[name]["trait"] == True:
            continue
        elif people[name]["trait"] == False: #comment this out if u want it to work. this is standard chance, use this (.01 * .65) + (.03 * .56) + (.96 * .01)
            traitcounter = 0"""
        if True:
        #print("got here")
            if name in one_gene:
                traitcounter = traitcounter * .56
            if name in two_genes:
                traitcounter = traitcounter * .65
            else:
                traitcounter = traitcounter * .01

    for name in people.keys():
        empty.add(name)
    sloop1 = empty.difference(have_trait)
    #print(sloop1)
    for name in sloop1:
        """if people[name]["trait"] == True:
            traitcounter = 0
        elif people[name]["trait"] == False: #comment this out if u want it to work. this is standard chance, use this (.01 * .65) + (.03 * .56) + (.96 * .01)
            monkeyballs = 0"""
        if True:
        #print("got here")
            if name in one_gene:
                traitcounter = traitcounter * (1 - .56)
            if name in two_genes:
                traitcounter = traitcounter * (1 - .65)
            else:
                traitcounter = traitcounter * (1 - .01)

    jointprob = zerocounter * twocounter * onecounter * traitcounter
    #print(jointprob)

    #print(zerocounter, twocounter, onecounter, traitcounter)
    return jointprob


def joint_probability1(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1

    for person in people:
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False

        gene_numb_prop = PROBS['gene'][gene_number]
        trait_prop = PROBS['trait'][gene_number][trait]

        if people[person]['mother'] is None:
            # no parents, use probability distribution
            probability *= gene_numb_prop * trait_prop
        else:
            # info about parents is available
            mother = people[person]['mother']
            father = people[person]['father']
            percentages = {}

            for ppl in [mother, father]:
                number = 1 if ppl in one_gene else 2 if ppl in two_genes else 0
                perc = 0 + PROBS['mutation'] if number == 0 else 0.5 if number == 1 else 1 - PROBS['mutation']
                percentages[ppl] = perc

            if gene_number == 0:
                # 0, none of parents gave gene
                probability *= (1 - percentages[mother]) * (1 - percentages[father])
            elif gene_number == 1:
                # 1, one of parents gave gene
                probability *= (1 - percentages[mother]) * percentages[father] + percentages[mother] * (1 - percentages[father])
            else:
                # 2, both of parents gave gene
                probability *= percentages[mother] * percentages[father]

            probability *= trait_prop

    return probability


def update1(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        probabilities[person]["gene"][gene_number] += p
        probabilities[person]["trait"][person in have_trait] += p

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    """for person in probabilities:
        number = 1 if person else 2 if person in two_genes else 0
        probabilities[person]["gene"][number] += p
        probabilities[person]["trait"][person in have_trait] += p
"""
    for person in one_gene:
        probabilities[person]["gene"][1] += p
    for person in two_genes:
        probabilities[person]["gene"][2] += p
    for person in have_trait:
        probabilities[person]["trait"][True] += p
    empty = set()
    for person in probabilities:
        empty.add(person)
        for person in one_gene.union(two_genes):
            if person in empty:
                empty.remove(person)
    for person in empty:
        probabilities[person]["gene"][0] += p


    for person in probabilities:
        empty.add(person)
        for person in have_trait:
            if person in empty:
                empty.remove(person)

    for person in empty:
        probabilities[person]["trait"][False] += p



def normalize1(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    normalized = probabilities.copy()
    for person in probabilities:
        for typ in ['gene', 'trait']:
            summed = sum(probabilities[person][typ].values())
            for category in probabilities[person][typ]:
                val = probabilities[person][typ][category]
                normalized_val = val / summed
                normalized[person][typ][category] = normalized_val
    return normalized

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        multiplier = 1/total
        for thing in probabilities[person]["gene"]:
            #print(probabilities[person]["gene"][thing])
            probabilities[person]["gene"][thing] *= multiplier
    for person in probabilities:
        total = probabilities[person]["trait"][False] + probabilities[person]["trait"][True]
        multiplier = 1/total
        for thing in probabilities[person]["trait"]:
            probabilities[person]["trait"][thing] *= multiplier



if __name__ == "__main__":
    main()