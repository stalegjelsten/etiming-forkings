# %%
import pandas as pd
import random
import math
import time
import pyodbc
import sqlalchemy as sa

# path to the access .mdb database file. Should be an absolute path
mdb_path = r"C:\Users\stale\dev\etiming-gaflinger\etime.mdb"
connection_string = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + mdb_path + r";"
)

# create SQLalchemy connection
engine = sa.create_engine(
    sa.engine.URL.create("access+pyodbc", query={"odbc_connect": connection_string})
)

# create pyodbc connection
conn = pyodbc.connect(connection_string)

# create pandas dataframes from relevant tables
classdf = pd.read_sql_query("select * from class", engine)
namedf = pd.read_sql_query("select * from name", engine)
coursedf = pd.read_sql_query("select * from cource", engine)

# a pd series which contains the number of forkings entered for each class
no_of_forkings = pd.Series([0 for i in range(len(classdf))]).rename("forkings")


# %%
def distributeCourses(currentClass, low_limit, high_limit):
    names_in_class = namedf[namedf["class"] == str(currentClass)]
    n = len(names_in_class)

    # create an array with uniform distribution of integers from lower limit
    # to upper limit
    courses = [i for i in range(low_limit, high_limit + 1)] * math.ceil(
        n / (high_limit - low_limit + 1)
    )

    # shuffle the elements of courses and slice it down to correct length
    random.shuffle(courses)
    courses = courses[:n]

    # loop over all names and assign the random courses to the competitors
    idx = 0
    for index, row in namedf.iterrows():
        if row["class"] == str(currentClass):
            namedf.loc[index, "cource"] = courses[idx]
            print(idx, courses[idx])
            idx += 1

    print(namedf[["name", "ename", "cource"]][namedf["class"] == str(currentClass)])
    print(
        f"Successfully set random courses for "
        f"{classdf['class'][classdf['code'] == str(currentClass)].item()}"
    )
    no_of_forkings[classdf[classdf["code"] == str(currentClass)].index] = (
        high_limit - low_limit + 1
    )
    time.sleep(1)

    return chooseClass()


def listCourses():
    # lists all courses in the database with
    courses = coursedf[["code", "name", "length"]]
    print("------------------------")
    print("Courses in the eTiming database")
    print(courses.to_string(index=False))
    print("------------------------")


def chooseClass():
    number_participants = namedf["class"].value_counts()

    # prints the classes together with the number of forkings assigned
    # and the number of participants in the class
    print(
        classdf[["code", "class"]]
        .merge(no_of_forkings, left_index=True, right_index=True)
        .merge(
            number_participants.rename("participants").rename_axis("code"),
            how="outer",
            on="code",
        )
    )

    print("Which class would you like to assign courses to?")
    chosen_class = int(
        input(
            f"Enter a number from {0} to {len(classdf)-1}, "
            "OR write -1 to exit OR write -2 to write changes to the .mdb database file: "
        )
    )
    if chosen_class == -1:
        return
    elif chosen_class == -2:
        writeToDatabase()
    else:
        chosen_class_code = classdf.iloc[chosen_class]["code"]
        printRunners(int(chosen_class_code))


def writeToDatabase():
    # namedf.to_sql("name", engine, index=False, if_exists="replace")
    cursor = conn.cursor()

    for _, row in namedf.iterrows():
        cursor.execute(f"update name set cource = {row.cource} where id like {row.id};")

    conn.commit()
    cursor.close()


def printRunners(currentClass):
    print(currentClass)
    names_in_class = namedf[namedf["class"] == str(currentClass)]
    print(names_in_class[["name", "ename"]])
    print(
        f"{len(names_in_class)} runners in "
        f"{classdf['class'][classdf['code'] == str(currentClass)].item()}."
    )
    print("l: List all courses.")
    print("n: Abort and choose another class.")
    print("y: Input high and low limits for course numbers.")
    choice = input("What would you like to do? ")
    if (choice == "l") or choice == "L":
        listCourses()
    elif choice == "y" or "Y":
        low_limit = int(
            input(
                f"Enter the lowest course number for class "
                f"{classdf['class'][classdf['code'] == str(currentClass)].item()}: "
            )
        )
        high_limit = int(
            input(
                "Enter the highest course number for class "
                f"{classdf['class'][classdf['code'] == str(currentClass)].item()}: "
            )
        )
        distributeCourses(currentClass, low_limit, high_limit)
    else:
        return chooseClass()


def main():
    chooseClass()


if __name__ == "__main__":
    main()
