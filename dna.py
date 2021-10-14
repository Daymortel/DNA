from sys import argv, exit
import itertools
import csv
import re
# vérifiez s'il y a la quantité requise d'arguments de ligne de commande.
if len(argv) != 3:
    print(f"Error there should be 2 argv, you have {argv}")
    exit(1)
# Ouvrez CSV et lisez une liste.
with open(argv[1], "r") as inputfile:
    reader = list(csv.reader(inputfile))
    reader[0].remove("name")
    i = reader[0]
# Ouvrir la séquence TXT
with open(argv[2], "r") as sequence:
    data = sequence.read()
# i est un segment d'ADN qui contient les données du CSV que nous recherchons.
# pour chaque séquence
valuelist = []
for q in range(len(i)):  # par exemple. pour le petit CSV i3. donc itérer pour chaque nucléotide.
    maxcounter = 0
    counter = 0
    position = 0
    previouspos = 0
    # alors que la séquence d'ADN n'a pas été entièrement analysée, procédez comme suit.
    while position < len(data):
        # cela donne la position à laquelle la séquence est trouvée
        position = data.find(i[q], position)
        if position == -1:  # c'est-à-dire introuvable, réinitialiser le compteur, arrêter la boucle.
            counter = 0
            break
        # sinon -1 alors la séquence recherchée a été trouvée et si (position - la longueur de la séquence) est également égale à 0, c'est une valeur consécutive
        # si la séquence est au début de la séquence
        elif (position != -1) and previouspos == 0:
            counter += 1
            maxcounter = counter
            previouspos = position
        # occurrences séquentielles
        elif (position != -1) and ((position - len(i[q])) == previouspos):
            counter += 1
            previouspos = position
            if maxcounter < counter:
                maxcounter = counter
        # trouvé en premier et non au début de la séquence.
        elif (position != -1) and ((position - len(i[q])) != previouspos):
            counter = 1
            previouspos = position
            if maxcounter < counter:
                maxcounter = counter
        position += 1
    # enregistrer le plus grand nombre d'occurrences séquentielles.
    valuelist.append(maxcounter)

# ce qui suit compare les occurrences de chaque nucléotide aux bases de données
# mettre à jour la liste pour qu'elle soit une liste de chaînes pour permettre la comparaison.
valuelist = list(map(str, valuelist))
# faire une nouvelle liste pour préserver le lecteur
cleaned = list(reader)
cleaned.pop(0)
# comparez la liste de valeurs au lecteur et si trouvé, imprimez le nom de la personne dont l'ADN a toutes les occurrences sur la console/le terminal.
for person in cleaned:
    if person[1:] == valuelist:
        print(f"{person[0]}")
        break
    elif person == cleaned[-1]:
        print("No match")
