etc = 5



print(" ")
print("# une liste peut se déclarer ainsi:")
print("liste = []")

liste = []
print(liste)


print(" ")
print("# .append(élément) permet d'ajouter un élément à la liste")
print("liste.append(45)")

liste.append(45)
print(liste)

# on peut mélanger les types d'élements avec python
print(" ")
print("# on peut mélanger les types d'élements avec python")

liste.append('a')
liste.append(42)
liste.append("blablabla")
print(liste)

# même des tuples 
print(" ")
print("# même des tuples ")
print("liste.append( (2,4) )")
print("liste.append( (4,5,4,'a')  )")

liste.append( (2,4) )
liste.append( (4,5,4,'a')  )
print(liste)

# même des listes
print(" ")
print("# même des listes")

liste.append([])
liste.append([[]])
print(liste)

#on accede à un element de la liste avec son index
print(" ")
print("# on accede à un element de la liste avec son index")

print(liste[0])
print(liste[1])
print(liste[etc])