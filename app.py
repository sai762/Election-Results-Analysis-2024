import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data for parliament and state elections
parliament_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\Parliament_election_results.csv")
andhra_pradesh_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\AndhraPradesh_election_results.csv")
odisha_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\Odisha_election_results.csv")
arunachal_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\ArunachalPradesh_election_results.csv")
sikkim_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\Sikkim_election_results.csv")
andhra_pradesh_parliament_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\AndhraPradesh_Parliament_election_results.csv")
odisha_parliament_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\Odisha_Parliament_election_results.csv")
arunachal_parliament_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\ArunachalPradesh_Parliament_election_results.csv")
sikkim_parliament_results = pd.read_csv(r"C:\Users\SAI KEERTHAN\Downloads\Sikkim_Parliament_election_results.csv")

def create_parliament_pie_chart():
    total_seats_parliament = parliament_results['Total'].sum()
    parliament_results['Seat Share (%)'] = (parliament_results['Total'] / total_seats_parliament) * 100

    # Identify the top 12 parties by seats
    top_12_parties = parliament_results.nlargest(12, 'Total')
    remaining_parties = parliament_results[~parliament_results['Party'].isin(top_12_parties['Party'])]

    # Combine remaining parties into a single 'Other' category
    other_seat_share = remaining_parties['Seat Share (%)'].sum()
    other_total_seats = remaining_parties['Total'].sum()
    other_row = pd.DataFrame([['Other', other_total_seats, 0, other_total_seats, other_seat_share]], columns=parliament_results.columns)

    # Create a new DataFrame with the top 12 parties and the 'Other' category
    top_12_with_other = pd.concat([top_12_parties, other_row], ignore_index=True)

    # Plotting with Plotly Express
    fig = px.pie(top_12_with_other, values='Seat Share (%)', names='Party', title='Parliament Election Results - Party Seat Shares',
                 hover_name='Party', hover_data=['Total'], labels={'Party': 'Parties'})

    return fig

def create_state_pie_chart(state_results, state_name):
    total_seats_state = state_results['Total'].sum()
    state_results['Seat Share (%)'] = (state_results['Total'] / total_seats_state) * 100

    # Plotting with Plotly Express
    fig = px.pie(state_results, values='Seat Share (%)', names='Party', title=f'{state_name} Election Results - Party Seat Shares',
                 hover_name='Party', hover_data=['Total'], labels={'Party': 'Parties'})

    return fig

def create_state_contribution_chart(state_parliament_results, state_name):
    total_seats_parliament = parliament_results['Total'].sum()
    state_total_seats_parliament = state_parliament_results['Total'].sum()

    # Calculate the seat share of the state's parties in Parliament
    state_seat_share_parliament = (state_total_seats_parliament / total_seats_parliament) * 100
    other_states_seat_share_parliament = 100 - state_seat_share_parliament

    # Data for plotting
    data = [state_seat_share_parliament, other_states_seat_share_parliament]
    labels = [f'{state_name} Parties', 'Other States']

    # Plotting with Plotly Express
    fig = px.pie(values=data, names=labels, title=f'Contribution of {state_name} Parties to Overall Parliament Results',
                 labels={'label': 'Regions', 'value': 'Seat Share (%)'})

    return fig

# Define Streamlit app layout
st.title("Election Results Visualization")

st.header("Parliament Election Results")
# Plot and display the pie chart for parliament results
parliament_pie_chart = create_parliament_pie_chart()
st.plotly_chart(parliament_pie_chart)

st.header("Statewise Election Results & Statewise Parliament Election Results Contribution")

# Create three columns for side-by-side layout with a spacer in the middle
col1, spacer, col2 = st.columns([1, 0.4, 1])

with col1:
    st.subheader("Andhra Pradesh")
    andhra_pradesh_pie_chart = create_state_pie_chart(andhra_pradesh_results, "Andhra Pradesh")
    st.plotly_chart(andhra_pradesh_pie_chart)

    st.subheader("Odisha")
    odisha_pie_chart = create_state_pie_chart(odisha_results, "Odisha")
    st.plotly_chart(odisha_pie_chart)

    st.subheader("Arunachal Pradesh")
    arunachal_pie_chart = create_state_pie_chart(arunachal_results, "Arunachal Pradesh")
    st.plotly_chart(arunachal_pie_chart)

    st.subheader("Sikkim")
    sikkim_pie_chart = create_state_pie_chart(sikkim_results, "Sikkim")
    st.plotly_chart(sikkim_pie_chart)

with col2:
    st.subheader("Andhra Pradesh")
    andhra_pradesh_parliament_contribution_chart = create_state_contribution_chart(andhra_pradesh_parliament_results, "Andhra Pradesh")
    st.plotly_chart(andhra_pradesh_parliament_contribution_chart)

    st.subheader("Odisha")
    odisha_parliament_contribution_chart = create_state_contribution_chart(odisha_parliament_results, "Odisha")
    st.plotly_chart(odisha_parliament_contribution_chart)

    st.subheader("Arunachal Pradesh")
    arunachal_parliament_contribution_chart = create_state_contribution_chart(arunachal_parliament_results, "Arunachal Pradesh")
    st.plotly_chart(arunachal_parliament_contribution_chart)

    st.subheader("Sikkim")
    sikkim_parliament_contribution_chart = create_state_contribution_chart(sikkim_parliament_results, "Sikkim")
    st.plotly_chart(sikkim_parliament_contribution_chart)



# Dictionary of file paths for each state's parliament election results
state_files = {
    'Andhra Pradesh': r"C:\Users\SAI KEERTHAN\Downloads\AndhraPradesh_Parliament_election_results.csv",
    'Odisha': r"C:\Users\SAI KEERTHAN\Downloads\Odisha_Parliament_election_results.csv",
    'Arunachal Pradesh': r"C:\Users\SAI KEERTHAN\Downloads\ArunachalPradesh_Parliament_election_results.csv",
    'Sikkim': r"C:\Users\SAI KEERTHAN\Downloads\Sikkim_Parliament_election_results.csv"
    # Add paths for other states as needed
}

# Initialize lists to store the data
states = []
seat_shares = []

# Total seats in the parliament
total_seats_parliament = parliament_results['Total'].sum()

# Calculate seat shares for each state
for state, file_path in state_files.items():
    state_results = pd.read_csv(file_path)
    state_total_seats = state_results['Total'].sum()
    state_seat_share = (state_total_seats / total_seats_parliament) * 100
    states.append(state)
    seat_shares.append(state_seat_share)

# Calculate the seat share of Other States in Parliament
other_states_seat_share = 100 - sum(seat_shares)
states.append('Other States')
seat_shares.append(other_states_seat_share)

# Data for plotting
data = pd.DataFrame({
    'State': states,
    'Seat Share (%)': seat_shares
})

# Create the pie chart using Plotly Express
fig = px.pie(data, values='Seat Share (%)', names='State', title="Contribution of Each State to Overall Parliament Results")

# Display the chart
st.plotly_chart(fig)
