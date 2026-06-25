import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================

with st.spinner("Loading EduPro Analytics Dashboard..."):
    df = pd.read_csv("Merged_EduPro_Dataset.csv")
# =========================
# CREATE AGE GROUPS
# =========================

bins = [0, 18, 25, 35, 45, 100]

labels = [
    "<18",
    "18-25",
    "26-35",
    "36-45",
    "45+"
]

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=bins,
    labels=labels,
    right=False
)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

# Age Group Filter
age_group = st.sidebar.selectbox(
    "Age Group",
    ["All"] + list(df["AgeGroup"].dropna().unique()),
    key="age_filter"
)

# Gender Filter
gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + list(df["Gender"].unique()),
    key="gender_filter"
)

# Course Category Filter
category = st.sidebar.selectbox(
    "Course Category",
    ["All"] + list(df["CourseCategory"].unique()),
    key="category_filter"
)

# Course Level Filter
level = st.sidebar.selectbox(
    "Course Level",
    ["All"] + list(df["CourseLevel"].unique()),
    key="level_filter"
)

# =========================
# APPLY FILTERS
# =========================

filtered_df = df.copy()

if age_group != "All":
    filtered_df = filtered_df[
        filtered_df["AgeGroup"] == age_group
    ]

if gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == gender
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["CourseCategory"] == category
    ]

if level != "All":
    filtered_df = filtered_df[
        filtered_df["CourseLevel"] == level
    ]

if filtered_df.empty:
    st.warning(
        "No data available for selected filters."
    )
    st.stop()

if (
    age_group != "All"
    or gender != "All"
    or category != "All"
    or level != "All"
):
    message=st.toast("✅Filters applied successfully!")
    import time
    time.sleep(2)
    message.empty()

    
# =========================
# DASHBOARD TITLE
# =========================

st.title("🎓 EduPro Analytics Dashboard")

st.markdown("""
### Learner Demographics and Course Enrollment Behavior Analysis

This dashboard provides insights into:

- Learner demographics
- Enrollment patterns
- Course popularity
- Skill level preferences
- Educational planning trends
""")

# =========================
# KPI CALCULATIONS
# =========================

total_users = filtered_df["UserID"].nunique()

total_courses = filtered_df["CourseID"].nunique()

total_enrollments = len(filtered_df)

avg_courses = (
    filtered_df.groupby("UserID")["CourseID"]
    .count()
    .mean()
)

# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Users",
    total_users
)

col2.metric(
    "Total Courses",
    total_courses
)

col3.metric(
    "Total Enrollments",
    total_enrollments
)

col4.metric(
    "Avg Courses/User",
    round(avg_courses, 2)
)

# =========================
# TOP INSIGHT KPIs
# =========================

top_category = (
    filtered_df["CourseCategory"]
    .value_counts()
    .idxmax()
)

top_level = (
    filtered_df["CourseLevel"]
    .value_counts()
    .idxmax()
)

top_age = (
    filtered_df["AgeGroup"]
    .value_counts()
    .idxmax()
)

st.subheader("Top Insights")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Top Category",
    top_category
)

col2.metric(
    "Top Level",
    top_level
)

col3.metric(
    "Top Age Group",
    top_age
)

# =========================
# COURSE CATEGORY CHART
# =========================

st.subheader("Course Category Popularity")

category_counts = (
    filtered_df["CourseCategory"]
    .value_counts()
)

st.bar_chart(category_counts)

# =========================
# COURSE LEVEL CHART
# =========================

st.subheader("Course Level Popularity")

level_counts = (
    filtered_df["CourseLevel"]
    .value_counts()
)

st.bar_chart(level_counts)

# =========================
# AGE GROUP CHART
# =========================

st.subheader("Enrollments by Age Group")

age_counts = (
    filtered_df["AgeGroup"]
    .value_counts()
)

st.bar_chart(age_counts)
# =========================
# ENROLLMENT TREND
# =========================

st.subheader("Enrollment Trend Over Time")

filtered_df["TransactionDate"] = pd.to_datetime(
    filtered_df["TransactionDate"]
)

trend = (
    filtered_df.groupby("TransactionDate")
    .size()
)

st.line_chart(trend)

# =========================
# TOP 10 COURSES
# =========================

st.subheader("Top 10 Most Enrolled Courses")

top_courses = (
    filtered_df["CourseName"]
    .value_counts()
    .head(10)
)

st.bar_chart(top_courses)
# =========================
# TOP ACTIVE LEARNERS
# =========================

st.subheader("Top 10 Active Learners")

top_users = (
    filtered_df["UserName"]
    .value_counts()
    .head(10)
)

st.bar_chart(top_users)

# =========================
# GENDER DISTRIBUTION
# =========================

st.subheader("Gender Distribution")

gender_counts = (
    filtered_df["Gender"]
    .value_counts()
)

st.bar_chart(gender_counts)

# =========================
# GENDER VS COURSE LEVEL
# =========================

st.subheader("Gender vs Course Level")

gender_level = pd.crosstab(
    filtered_df["Gender"],
    filtered_df["CourseLevel"]
)

st.dataframe(gender_level)

st.bar_chart(gender_level)

# =========================
# HEATMAP CODE
# =========================

st.subheader("Age Group vs Course Category Heatmap")

heatmap_data = pd.crosstab(
    filtered_df["AgeGroup"],
    filtered_df["CourseCategory"]
)

fig, ax = plt.subplots(figsize=(10, 5))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    ax=ax
)

st.pyplot(fig)

# =========================
# FILTERED DATA TABLE
# =========================

st.subheader("Filtered Data")

st.dataframe(filtered_df)

# =========================
# DOWNLOAD BUTTON
# =========================

st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="Filtered_EduPro_Data.csv",
    mime="text/csv"
)

# =========================
# KEY INSIGHTS
# =========================

st.header("Key Insights")

top_category = (
    filtered_df["CourseCategory"]
    .value_counts()
    .idxmax()
)

top_level = (
    filtered_df["CourseLevel"]
    .value_counts()
    .idxmax()
)

top_age = (
    filtered_df["AgeGroup"]
    .value_counts()
    .idxmax()
)

st.write(
    f"✅ Most popular course category: {top_category}"
)

st.write(
    f"✅ Most preferred course level: {top_level}"
)

st.write(
    f"✅ Most active age group: {top_age}"
)

st.write(
    "✅ Dashboard supports data-driven educational planning."
)

# =========================
# EXECUTIVE SUMMARY
# =========================

st.header("Executive Summary")

st.success("""
EduPro serves a diverse learner base across multiple age groups.

The dashboard highlights learner demographics,
course preferences and enrollment patterns.

These insights can help improve course planning,
targeted outreach and learner engagement.
""")
# =========================
# PROJECT COMPLETION
# =========================

st.header("Project Status")

if st.button("Project Successfully Completed"):
    st.balloons()

    st.success(
        "EduPro Analytics Dashboard is working successfully!"
    )