# %%
import pandas as pd
import random
import math
import time

classdf = pd.read_excel("class.xlsx")
namedf = pd.read_excel("name.xlsx")
coursedf = pd.read_excel("cource.xlsx")
finished = pd.Series([0 for i in range(len(classdf))]).rename("forkings")


# %%
def distributeCourses(currentClass, low_limit, high_limit):
    names_in_class = namedf[namedf["class"] == currentClass] 
    n = len(names_in_class)
    courses = [i for i in range(low_limit, high_limit+1)] * math.ceil(n/(high_limit-low_limit+1))
    random.shuffle(courses) # shuffle the sequence x in place
    courses = courses[:n]
    print(courses)
    # x = pd.Series(x[:n])
    idx = 0
    for index, row in namedf.iterrows():
        if row["class"] == currentClass:
            namedf.loc[index, "cource"] = courses[idx]
            print(idx, courses[idx])
            idx += 1
    print(namedf[["name", "ename", "cource"]][namedf["class"] == currentClass])
    print(f"Successfully set random courses for {classdf['class'][classdf["code"] == str(currentClass)].item()}")
    finished[classdf[classdf["code"] == str(currentClass)].index] = high_limit-low_limit+1
    time.sleep(1)

    return chooseClass()


def chooseClass():
    print(classdf[["class", "code"]].merge(finished, left_index=True, right_index=True))
    chosen_class = int(
        input(
            f"What class would you like to assign courses to? Enter a number from {0} to {len(classdf)-1}, or -1 to exit: "
        )
    )
    if chooseClass == -1:
        return
    chosen_class_code = classdf.iloc[chosen_class]["code"]
    printRunners(int(chosen_class_code))


def printRunners(currentClass):
    print(currentClass)
    names_in_class = namedf[namedf["class"] == currentClass]
    print(names_in_class[["name", "ename"]])
    print(f"{len(names_in_class)} runners in {classdf["class"][classdf["code"] == str(currentClass)].item()}.")
    print("l: List all courses.")
    print("n: Abort and choose another class.")
    print("y: Input high and low limits for course numbers.")
    choice = input(f"What would you like to do? ")
    if (choice == "l") or choice == "L":
        listCourses()
    elif choice == "y" or "Y":
        low_limit = int(input(f"Enter the lowest course number for class {classdf["class"][classdf["code"] == str(currentClass)].item()}: "))
        high_limit = int(input(f"Enter the highest course number for class {classdf["class"][classdf["code"] == str(currentClass)].item()}: "))
        distributeCourses(currentClass, low_limit, high_limit)
    else:
        return chooseClass()
    


def main():
    chooseClass()

if __name__ == "__main__":
    main()

# %%
