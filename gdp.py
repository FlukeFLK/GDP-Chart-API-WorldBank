import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Function to load GDP data from World Bank API for a specific country
def load_gdp_data(country_code):
    # API endpoint for World Bank GDP data for a specific country
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json'
    
    # Fetch data from the API
    response = requests.get(url)
    data = response.json()[1]
    
    # Extract GDP data
    gdp_values = [entry['value'] for entry in data]
    years = [entry['date'] for entry in data]

    # Create DataFrame
    df = pd.DataFrame({'Year': years, 'GDP': gdp_values})
    df['Year'] = pd.to_datetime(df['Year'])
    
    return df

# Predefined list of country names
country_names = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

# Title setup
st.title('GDP Analysis by Country')

# Dropdown for selecting a country
selected_country = st.selectbox('Select a country:', [''] + country_names)

# Input for typing the country name
typed_country = st.text_input('Or type a country name:', '')

if selected_country:
    country_name = selected_country
elif typed_country:
    country_name = typed_country
else:
    country_name = None

if country_name:
    # Try to fetch the country code for the entered country name
    try:
        country_code = requests.get(f'https://restcountries.com/v2/name/{country_name}').json()[0]['alpha2Code']
    except:
        st.error('Country not found. Please enter a valid country name.')
    else:
        # Load GDP data for the selected country
        gdp_data = load_gdp_data(country_code)

        # Display GDP data for the selected country
        if not gdp_data.empty:
            st.subheader(f'GDP Data for {country_name}')
            st.write(gdp_data)
            
            # Plot GDP over time for the selected country
            fig = px.line(gdp_data, x='Year', y='GDP', title=f'GDP Over Time for {country_name}')
            st.plotly_chart(fig)
        else:
            st.write(f'Error: No GDP data available for {country_name}.')
