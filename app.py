import streamlit as st
import pandas as pd
import plotly.express as px

# Title for your Streamlit app
st.title("Top Countries for Financial Independence")

# Load the embedded Excel file automatically
@st.cache_data
def load_data():
    file_path = "Col_Sal.xlsx"  # Ensure this file is in the same directory as app.py
    data = pd.read_excel(file_path, sheet_name="Country")
    return data

data = load_data()

# Clean the Country column
data['Country'] = data['Country'].str.strip()  # Remove leading/trailing spaces
data['Country'] = data['Country'].str.title()  # Title case for uniformity

# Add title and instructions
st.write("### Instructions for Using the Tool")

instructions = """
- This tool aims to help users find the most suitable countries for pursuing FI during the accumulation phase.
- Select your **current country** from the dropdown menu above the graph.
- The graph maps **percentage differences** in salaries and cost of living (COL) relative to your selected country.
- The **red dashed line** serves as a benchmark:
   - Countries **above the red line** may provide better opportunities for pursuing financial independence during the accumulation phase (on average).
   - Countries **on the red line** have equivalent percentage differences in both salaries and COL (e.g., perhaps a 10% higher salary, but also a 10% higher COL).
   - Countries **below the red line** may provide worse opportunities for pursuing financial independence during the accumulation phase (on average).
- Hover over the top right of the figure and use the zoom tool (draw a square on the figure), zoom in/out, pan, and other functions to better visualize your countries of interest
- Example: With Italy as the reference (appearing at the intersection of the x and y axes in dashed white), Spain has an 11% higher average salary and a 7.4% lower cost of living. Pursuing FI in Spain is likely to be easier, on average, than in Italy. There are about 30 countries where achieving FI would likely be easier compared to Italy.
- Click on the legend's continents to remove groups of countries.
- Data on salaries and cost of living is from Numbeo (2025).
"""
st.write(instructions)  # Add instructions above the dropdown menu

# Dropdown menu for selecting the reference country
# Dropdown menu for selecting the reference country
reference_country = st.selectbox(
    "Select Reference Country:",
    options=sorted(data['Country'].unique()),  # Sort countries alphabetically
    index=sorted(data['Country'].unique()).index("Italy")  # Default index set to "Italy"
)



# Country-to-continent mapping
country_to_continent = {
    # America
    'United States': 'America', 'Puerto Rico': 'America', 'Canada': 'America', 'Uruguay': 'America',
    'Costa Rica': 'America', 'Chile': 'America', 'Panama': 'America', 'Trinidad And Tobago': 'America',
    'Mexico': 'America', 'Argentina': 'America', 'Brazil': 'America', 'Ecuador': 'America',
    'Dominican Republic': 'America', 'Colombia': 'America', 'Paraguay': 'America', 'Venezuela': 'America',
    'Peru': 'America',

    # Africa
    'South Africa': 'Africa', 'Mauritius': 'Africa', 'Libya': 'Africa', 'Tunisia': 'Africa',
    'Kenya': 'Africa', 'Algeria': 'Africa', 'Ghana': 'Africa', 'Nigeria': 'Africa',
    'Egypt': 'Africa', 'Zimbabwe': 'Africa', 'Morocco': 'Africa', 'Uganda': 'Africa',

    # Asia
    'Singapore': 'Asia', 'Hong Kong (China)': 'Asia', 'United Arab Emirates': 'Asia', 'Qatar': 'Asia',
    'Israel': 'Asia', 'South Korea': 'Asia', 'Japan': 'Asia', 'Oman': 'Asia', 'Bahrain': 'Asia',
    'Saudi Arabia': 'Asia', 'Taiwan': 'Asia', 'China': 'Asia', 'Malaysia': 'Asia', 'Thailand': 'Asia',
    'Jordan': 'Asia', 'Kazakhstan': 'Asia', 'Lebanon': 'Asia', 'Armenia': 'Asia', 'Iraq': 'Asia',
    'Uzbekistan': 'Asia', 'Vietnam': 'Asia', 'Philippines': 'Asia', 'Kyrgyzstan': 'Asia',
    'Bangladesh': 'Asia', 'Iran': 'Asia', 'Nepal': 'Asia', 'Sri Lanka': 'Asia', 'Pakistan': 'Asia',
    'Kuwait': 'Asia', 'India': 'Asia', 'Turkey': 'Asia', 'Indonesia': 'Asia',

    # Europe
    'Switzerland': 'Europe', 'Luxembourg': 'Europe', 'Iceland': 'Europe', 'Denmark': 'Europe',
    'Netherlands': 'Europe', 'Norway': 'Europe', 'United Kingdom': 'Europe', 'Ireland': 'Europe',
    'Germany': 'Europe', 'Sweden': 'Europe', 'Finland': 'Europe', 'Belgium': 'Europe',
    'Austria': 'Europe', 'France': 'Europe', 'Italy': 'Europe', 'Spain': 'Europe', 'Cyprus': 'Europe',
    'Czech Republic': 'Europe', 'Slovenia': 'Europe', 'Estonia': 'Europe', 'Poland': 'Europe',
    'Malta': 'Europe', 'Croatia': 'Europe', 'Lithuania': 'Europe', 'Slovakia': 'Europe',
    'Latvia': 'Europe', 'Portugal': 'Europe', 'Bulgaria': 'Europe', 'Hungary': 'Europe',
    'Romania': 'Europe', 'Greece': 'Europe', 'Montenegro': 'Europe', 'Serbia': 'Europe',
    'Bosnia And Herzegovina': 'Europe', 'North Macedonia': 'Europe', 'Albania': 'Europe',
    'Moldova': 'Europe', 'Belarus': 'Europe', 'Georgia': 'Europe', 'Ukraine': 'Europe', 'Russia': 'Europe',

    # Oceania
    'Australia': 'Oceania', 'New Zealand': 'Oceania'
}

# Calculate differences
def calculate_differences(data, reference_country):
    ref_data = data[data['Country'] == reference_country].iloc[0]
    data['Sal_Diff_%'] = ((data['Sal'] - ref_data['Sal']) / ref_data['Sal']) * 100
    data['Col_Diff_%'] = ((data['Col'] - ref_data['Col']) / ref_data['Col']) * 100
    data['Continent'] = data['Country'].map(country_to_continent)
    return data

data = calculate_differences(data, reference_country)

# Create scatter plot with red dashed benchmark line
def create_scatter_plot(data, reference_country):
    # Add the reference country to the plot at (0,0)
    ref_data = data[data['Country'] == reference_country]
    x_min, x_max = data['Col_Diff_%'].min(), data['Col_Diff_%'].max()
    y_min, y_max = data['Sal_Diff_%'].min(), data['Sal_Diff_%'].max()
    x_margin = (x_max - x_min) * 0.1
    y_margin = (y_max - y_min) * 0.1

    # Create the scatter plot
    fig = px.scatter(
        data,
        x='Col_Diff_%',
        y='Sal_Diff_%',
        color='Continent',
        text='Country',
        hover_data={'Col_Diff_%': ':.1f', 'Sal_Diff_%': ':.1f', 'Country': True},
        labels={
            'Col_Diff_%': 'Cost of Living Difference (%)',
            'Sal_Diff_%': 'Salary Difference (%)',
        },
        title=f"Cost of Living vs Salary Comparison (Reference: {reference_country})",
        template="plotly_dark",
    )

    # Add red benchmark line
    fig.add_shape(
        type="line",
        x0=-1000, x1=1000,
        y0=-1000, y1=1000,
        line=dict(color="red", dash="dash", width=2),
    )

    # Add dashed lines for x=0 and y=0
    fig.add_shape(
        type="line",
        x0=0, x1=0,
        y0=y_min - y_margin, y1=y_max + y_margin,
        line=dict(color="white", dash="dash", width=2),
    )
    fig.add_shape(
        type="line",
        x0=x_min - x_margin, x1=x_max + x_margin,
        y0=0, y1=0,
        line=dict(color="white", dash="dash", width=2),
    )

    # Customize gridlines
    fig.update_xaxes(
        range=[x_min - x_margin, x_max + x_margin],
        gridcolor="rgba(255, 255, 255, 0.2)",  # Ensure vertical gridlines
        showgrid=True,
        zeroline=False,  # Disable the default white x=0 line
        tickmode="linear",
        dtick=(x_max - x_min) / 5,
    )
    fig.update_yaxes(
        range=[y_min - y_margin, y_max + y_margin],
        gridcolor="rgba(255, 255, 255, 0.2)",  # Ensure horizontal gridlines
        showgrid=True,
        zeroline=False,  # Disable the default white y=0 line
        tickmode="linear",
        dtick=(y_max - y_min) / 5,
    )

    # Customize bubble size and legend
    fig.update_traces(
        marker=dict(size=13, line=dict(width=2, color='DarkSlateGrey')),  # Slightly larger bubbles
        textposition='top center'
    )
    fig.update_layout(
    height=500,  # Reduce height slightly
    width=1200,  # Increase width for a more horizontal shape

        legend=dict(
            title=dict(font=dict(color="white")),
            font=dict(color="white"),
            bgcolor="rgba(0, 0, 0, 0)",  # Transparent legend background
        ),
        title=dict(
            text=f"Cost of Living vs Salary Comparison (Reference: {reference_country})",
            font=dict(size=20, color="white"),  # Fully visible title
        ),
        margin=dict(l=40, r=40, t=50, b=5),
        paper_bgcolor='black',
        plot_bgcolor='black',
    )

    return fig


# Display the plot
scatter_plot = create_scatter_plot(data, reference_country)
st.plotly_chart(scatter_plot, use_container_width=True)
st.empty() 

