import streamlit as st
import pandas as pd


# Title
st.title("🏫 School Result Management System")

# load or create data
try:
    df = pd.read_csv("student.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Roll No", "Name", "Maths", "Science", "English"])

menu = ["Add Student", "Enter Marks", "View All Result", "Search Student"] 
choice = st.sidebar.selectbox("menu", menu)

# Add Student
if choice == "Add Student":
    st.subheader("+ Add New Student")
    roll = st.text_input("Enter Roll No")
    name = st.text_input("Enter Student Name")

    if st.button("Add"):
        if roll in df["Roll No"].values:
            st.warning("Student with this roll number already exists!")
        else:
           new_row = pd.DataFrame([[roll, name, "", "", ""]], columns = df.columns)
           df = pd.concat([df, new_row], ignore_index = True)
           df.to_csv("student.csv", index=False)
           st.success(f"Student {name} added!")
        

# Enter Marks
elif choice == "Enter Marks":
    st.subheader("Enter Marks")
    roll = st.text_input("Enter Roll No")

    if roll in df["Roll No"].values:
        math = st.number_input("Math Marks", min_value=0, max_value=100)
        science= st.number_input("Science Marks", min_value=0, max_value=100)
        english = st.number_input("English Marks", min_value=0, max_value=100)

        if st.button("Save Marks"):
            df.loc[df["Roll No"] == roll, ["Maths", "Science", "English"]] = [math, science, english]
            df.to_csv("student.csv", index=False)
            st.success("Marks Updated Successfullly!")
    elif roll:
        st.error("Student not found!")

# View Result        
elif choice == "View All Result":
    st.subheader("View All Result")
    if not df.empty:
        result_df = df.copy()
        result_df[["Maths", "Science", "English"]] = result_df[["Maths", "Science", "English" ]].apply(pd.to_numeric, errors="coerce")
        result_df["Total"] = result_df[["Maths", "Science", "English"]].sum(axis=1)
        result_df["%"] = result_df["Total"]/ 3
        st.dataframe(result_df)
    else:
        st.info("No data available")

# Search Student
elif choice == "Search Student":
    st.subheader("🔍 Search Student")
    roll = st.text_input("Enter Roll Number to Search")
    if st.button("Search"):
        if roll in df["Roll No"].values:
            student = df[df["Roll No"] == roll]
            st.table(student)
        else:
            st.warning("Student not found!")


