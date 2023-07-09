import operator
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the dataset into a pandas dataframe
df = pd.read_csv("pmc.csv")
wards = ["KarveNagar", "Ghole Road", "Kasaba", "Wanowrie Ramtekdi", "Dhankawadi", "Sinhgad Road",
         "Hadapsar", "Bhavani Peth", "Kondhwa", "Yerawada"]

cleanliness_probabilities = []
footpath_probabilities = []
road_probabilities = []
water_probabilities = []
cleanliness_benchmark = 0
footpath_benchmark = 0
road_benchmark = 0
water_benchmark = 0
dict_cleanliness = {}
dict_footpath = {}
dict_road = {}
dict_water = {}
menu = ["Singular", "Comparison_top3", "Comparison_All_Cleanliness", "Comparison_All_Footpath",
        "Comparison_All_Road", "Comparison_All_Water"]
choice = st.sidebar.selectbox("Select an option", menu)

# Iterate over wards
for ward in wards:
    location = ward
    df_ward = df.loc[df['location'] == ward]  # Filter dataframe for the specific ward

    # Calculate the negative counts for each complaint category
    cleanliness_count = (df_ward[df_ward['complaint'] == 'cleanliness']['level'] == 'negative').sum()
    footpath_count = (df_ward[df_ward['complaint'] == 'footpath']['level'] == 'negative').sum()
    water_count = (df_ward[df_ward['complaint'] == 'water']['level'] == 'negative').sum()
    road_count = (df_ward[df_ward['complaint'] == 'road']['level'] == 'negative').sum()

    total = len(df_ward['complaint'])  # Total number of complaints for the ward

    # Calculate the probabilities of negative complaints for each category
    prob_neg_cleanliness = cleanliness_count / total
    prob_neg_footpath = footpath_count / total
    prob_neg_water = water_count / total
    prob_neg_road = road_count / total

    cleanliness_probabilities.append(prob_neg_cleanliness)
    footpath_probabilities.append(prob_neg_footpath)
    water_probabilities.append(prob_neg_water)
    road_probabilities.append(prob_neg_road)

    dict_cleanliness[ward] = prob_neg_cleanliness
    dict_footpath[ward] = prob_neg_footpath
    dict_road[ward] = prob_neg_road
    dict_water[ward] = prob_neg_water

cleanliness_benchmark = np.mean(cleanliness_probabilities)
footpath_benchmark = np.mean(footpath_probabilities)
road_benchmark = np.mean(road_probabilities)
water_benchmark = np.mean(water_probabilities)

# Sort the dictionaries based on probabilities in ascending order
sorted_cleanliness_data = sorted(dict_cleanliness.items(), key=operator.itemgetter(1), reverse=False)
sorted_footpath_data = sorted(dict_footpath.items(), key=operator.itemgetter(1), reverse=False)
sorted_road_data = sorted(dict_road.items(), key=operator.itemgetter(1), reverse=False)
sorted_water_data = sorted(dict_water.items(), key=operator.itemgetter(1), reverse=False)

# Process user choice
if choice == "Singular":
    st.title('Wards')
    unique_locations = np.unique(df['location'])  # Get unique locations from the dataset
    ward_selected = st.selectbox("Select a ward", options=unique_locations)

    df_ward_selected = df.loc[df['location'] == ward_selected]  # Filter dataframe for the selected ward

    # Calculate the negative and positive counts for each complaint category
    cleanliness_count_negative = (df_ward_selected[df_ward_selected['complaint'] == 'cleanliness']['level'] == 'negative').sum()
    cleanliness_count_positive = (df_ward_selected[df_ward_selected['complaint'] == 'cleanliness']['level'] == 'positive').sum()

    footpath_count_negative = (df_ward_selected[df_ward_selected['complaint'] == 'footpath']['level'] == 'negative').sum()
    footpath_count_positive = (df_ward_selected[df_ward_selected['complaint'] == 'footpath']['level'] == 'positive').sum()

    water_count_negative = (df_ward_selected[df_ward_selected['complaint'] == 'water']['level'] == 'negative').sum()
    water_count_positive = (df_ward_selected[df_ward_selected['complaint'] == 'water']['level'] == 'positive').sum()

    road_count_negative = (df_ward_selected[df_ward_selected['complaint'] == 'road']['level'] == 'negative').sum()
    road_count_positive = (df_ward_selected[df_ward_selected['complaint'] == 'road']['level'] == 'positive').sum()

    total = len(df_ward_selected['complaint'])  # Total number of complaints for the selected ward

    # Calculate the probabilities of negative complaints for each category
    prob_neg_cleanliness = cleanliness_count_negative / total
    prob_neg_footpath = footpath_count_negative / total
    prob_neg_water = water_count_negative / total
    prob_neg_road = road_count_negative / total

    data = {'Cleanliness': prob_neg_cleanliness, 'Footpath': prob_neg_footpath, 'Water': prob_neg_water, 'Road': prob_neg_road}

    # Create a bar chart to visualize the probabilities
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(data.keys(), data.values(), width=0.4)

    # Add benchmark lines for each category
    ax.axhline(cleanliness_benchmark, color='red', linestyle=':', label='cleanliness_benchmark', xmin=0, xmax=1)
    ax.axhline(footpath_benchmark, color='orange', linestyle='--', label='footpath_benchmark', xmin=0, xmax=2)
    ax.axhline(road_benchmark, color='green', linestyle='dashed', label='road_benchmark', xmin=0, xmax=3)
    ax.axhline(water_benchmark, color='black', linestyle='dashdot', label='water_benchmark', xmin=0, xmax=4)

    ax.set_xlabel('Complaint Categories')
    ax.set_ylabel('Probability of Negative Complaints')
    plt.legend(loc='best')

    st.pyplot(fig)

    # Create a pie chart to visualize the negative and positive counts for each complaint category
    labels = ['cleanliness-', 'cleanliness+', 'footpath-', 'footpath+', 'water-', 'water+', 'road-', 'road+']
    values = [cleanliness_count_negative, cleanliness_count_positive, footpath_count_negative, footpath_count_positive,
              water_count_negative, water_count_positive, road_count_negative, road_count_positive]
    colors = ['tab:blue', 'orange', 'green', 'red', 'purple', 'black', 'pink', 'gray']

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, colors=colors, radius=2, autopct='%1.1f%%', startangle=60)
    ax1.axis('equal')

    st.pyplot(fig1)

if choice == "Comparison_top3":
    # Create data dictionaries for the top 3 wards in each category
    data_cleanliness = {sorted_cleanliness_data[0][0]: dict_cleanliness.get(sorted_cleanliness_data[0][0]),
                        sorted_cleanliness_data[1][0]: dict_cleanliness.get(sorted_cleanliness_data[1][0]),
                        sorted_cleanliness_data[2][0]: dict_cleanliness.get(sorted_cleanliness_data[2][0])}

    data_footpath = {sorted_footpath_data[0][0]: dict_footpath.get(sorted_footpath_data[0][0]),
                     sorted_footpath_data[1][0]: dict_footpath.get(sorted_footpath_data[1][0]),
                     sorted_footpath_data[2][0]: dict_footpath.get(sorted_footpath_data[2][0])}

    data_road = {sorted_road_data[0][0]: dict_road.get(sorted_road_data[0][0]),
                 sorted_road_data[1][0]: dict_road.get(sorted_road_data[1][0]),
                 sorted_road_data[2][0]: dict_road.get(sorted_road_data[2][0])}

    data_water = {sorted_water_data[0][0]: dict_water.get(sorted_water_data[0][0]),
                  sorted_water_data[1][0]: dict_water.get(sorted_water_data[1][0]),
                  sorted_water_data[2][0]: dict_water.get(sorted_water_data[2][0])}

    # Create bar charts for each category
    fig_cleanliness, ax_cleanliness = plt.subplots(figsize=(10, 5))
    ax_cleanliness.bar(data_cleanliness.keys(), data_cleanliness.values(), width=0.4)
    ax_cleanliness.axhline(cleanliness_benchmark, color='red', linestyle=':', label='cleanliness_benchmark', xmin=0, xmax=1)
    ax_cleanliness.set_xlabel('Wards')
    ax_cleanliness.set_ylabel('Mean')
    plt.title('Cleanliness')
    plt.legend(loc='best')
    st.pyplot(fig_cleanliness)

    fig_footpath, ax_footpath = plt.subplots(figsize=(10, 5))
    ax_footpath.bar(data_footpath.keys(), data_footpath.values(), width=0.4)
    ax_footpath.axhline(footpath_benchmark, color='orange', linestyle='--', label='footpath_benchmark', xmin=0, xmax=1)
    ax_footpath.set_xlabel('Wards')
    ax_footpath.set_ylabel('Mean')
    plt.title('Footpath')
    plt.legend(loc='best')
    st.pyplot(fig_footpath)

    fig_road, ax_road = plt.subplots(figsize=(10, 5))
    ax_road.bar(data_road.keys(), data_road.values(), width=0.4)
    ax_road.axhline(road_benchmark, color='green', linestyle='dashed', label='road_benchmark', xmin=0, xmax=1)
    ax_road.set_xlabel('Wards')
    ax_road.set_ylabel('Mean')
    plt.title('Road')
    plt.legend(loc='best')
    st.pyplot(fig_road)

    fig_water, ax_water = plt.subplots(figsize=(10, 5))
    ax_water.bar(data_water.keys(), data_water.values(), width=0.4)
    ax_water.axhline(water_benchmark, color='black', linestyle='dashdot', label='water_benchmark', xmin=0, xmax=1)
    ax_water.set_xlabel('Wards')
    ax_water.set_ylabel('Mean')
    plt.title('Water')
    plt.legend(loc='best')
    st.pyplot(fig_water)

if choice == "Comparison_All_Cleanliness":
    labels = wards
    cleanliness_values = [dict_cleanliness[ward] for ward in wards]

    fig_cleanliness_all, ax_cleanliness_all = plt.subplots()
    ax_cleanliness_all.pie(cleanliness_values, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax_cleanliness_all.axis('equal')
    plt.title('Cleanliness')
    st.pyplot(fig_cleanliness_all)

if choice == "Comparison_All_Footpath":
    labels = wards
    footpath_values = [dict_footpath[ward] for ward in wards]

    fig_footpath_all, ax_footpath_all = plt.subplots()
    ax_footpath_all.pie(footpath_values, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax_footpath_all.axis('equal')
    plt.title('Footpath')
    st.pyplot(fig_footpath_all)

if choice == "Comparison_All_Water":
    labels = wards
    water_values = [dict_water[ward] for ward in wards]

    fig_water_all, ax_water_all = plt.subplots()
    ax_water_all.pie(water_values, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax_water_all.axis('equal')
    plt.title('Water')
    st.pyplot(fig_water_all)

if choice == "Comparison_All_Road":
    labels = wards
    road_values = [dict_road[ward] for ward in wards]

    fig_road_all, ax_road_all = plt.subplots()
    ax_road_all.pie(road_values, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax_road_all.axis('equal')
    plt.title('Road')
    st.pyplot(fig_road_all)
