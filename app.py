import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Title for your Streamlit app
st.title("Cost of Living vs Salary Comparison")

# Sidebar: File upload
st.sidebar.header("Upload File")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file here:", type=["xlsx"])

# Load the file if provided
if uploaded_file is not None:
    # Load the Excel file
    try:
        data = pd.read_excel(uploaded_file, sheet_name="Country")
        st.sidebar.success("File loaded successfully!")

        # Display a preview of the data
        if st.sidebar.checkbox("Show raw data"):
            st.write("### Raw Data Preview")
            st.dataframe(data)
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        st.stop()
else:
    st.sidebar.info("Awaiting file upload...")
    st.stop()

# Clean the Country column
data['Country'] = data['Country'].str.strip()  # Remove leading/trailing spaces
data['Country'] = data['Country'].str.title()  # Title case for uniformity

# Sidebar: Select reference country
st.sidebar.header("Settings")
reference_country = st.sidebar.selectbox(
    "Select Reference Country:",
    options=sorted(data['Country'].unique()),  # Sort countries alphabetically
    index=0
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
    data['Sal_Diff_%'] = ((data['Sal'] - ref_data['Sal'].values[0]) / ref_data['Sal'].values[0]) * 100
    data['Col_Diff_%'] = ((data['Col'] - ref_data['Col'].values[0]) / ref_data['Col'].values[0]) * 100
    data['Continent'] = data['Country'].map(country_to_continent)

    # Calculate dynamic axis limits based on the data
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

    # Add dashed lines for x=0 and y=0
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=y_min - y_margin,
        y1=y_max + y_margin,
        line=dict(color="white", dash="dash", width=2),
    )
    fig.add_shape(
        type="line",
        x0=x_min - x_margin,
        x1=x_max + x_margin,
        y0=0,
        y1=0,
        line=dict(color="white", dash="dash", width=2),
    )

    # Enforce vertical and horizontal grid lines
    fig.update_xaxes(
        range=[x_min - x_margin, x_max + x_margin],
        showline=False,  # Remove default axis line
        zeroline=False,  # Disable the default white x=0 line
        gridcolor="rgba(255, 255, 255, 0.1)",  # Light vertical grid lines
        showgrid=True,  # Force vertical grid lines to show
        griddash="dot",  # Dashed grid lines
        tickmode="linear",
        dtick=(x_max - x_min) / 5,  # Dynamic ticks for granularity
    )
    fig.update_yaxes(
        range=[y_min - y_margin, y_max + y_margin],
        showline=False,  # Remove default axis line
        zeroline=False,  # Disable the default white y=0 line
        gridcolor="rgba(255, 255, 255, 0.1)",  # Light horizontal grid lines
        showgrid=True,  # Force horizontal grid lines to show
        griddash="dot",  # Dashed grid lines
        tickmode="linear",
        dtick=(y_max - y_min) / 5,
    )

    # Highlight the reference country at (0,0)
    fig.add_trace(
        px.scatter(
            ref_data,
            x=[0],
            y=[0],
            text='Country',
            template="plotly_dark",
        ).data[0]
    )

    # Customize layout and remove "Scatter Plot" title
    fig.update_traces(
        marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')),
        textposition='top center'
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(
            title=dict(font=dict(color="white")),
            font=dict(color="white"),
            itemsizing="constant",
        ),
        legend_title="Continent",
        height=700,
        width=900,
        title=dict(text=f"Cost of Living vs Salary Comparison (Reference: {reference_country})", font=dict(size=20, color="orange")),
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='black',
        plot_bgcolor='black',
    )

    return fig



# Display the plot
scatter_plot = create_scatter_plot(data, reference_country)
st.plotly_chart(scatter_plot, use_container_width=True)


