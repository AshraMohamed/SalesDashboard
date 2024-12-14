
# import some libraries
import streamlit as st
import numpy as np 
import pandas as pd 
import plotly.express as px 
import matplotlib.pyplot as plt 
import seaborn as sns 
import calendar

# Set page config with an icon
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",  # Add your icon here (emoji or local file path)
    layout='wide',
    initial_sidebar_state="collapsed"
)

# Apply custom styling for fonts and center alignment
st.markdown(
    """
    <style>
    /* Set a gradient background for the entire page */
    body {
        background: linear-gradient(to right, #ece9e6, #ffffff); /* Replace with desired colors */
        font-family: 'Arial', sans-serif;
    }
    /* Center the title and apply a custom font */
    .main-title {
        font-family: 'Arial', sans-serif; /* Change font if needed */
        font-size: 50px;
        color: #333333;  /* Customize text color */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the title with custom style
st.markdown('<h1 class="main-title">📊 Sales Dashboard</h1>', unsafe_allow_html=True)

# Read file
df_All = pd.read_csv('Company_Performance_Cleaned.csv')
# Define the color mapping for each country
color_discrete_map = {
    "Algeria": "#1f77b4",     # Blue
    "Iran": "#ff7f0e",        # Orange
    "Iraq": "#2ca02c",        # Green
    "Jordan": "#d62728",      # Red
    "Lebanon": "#9467bd",     # Purple
    "Libya": "#8c564b",       # Brown
    "Morocco": "#e377c2",     # Pink
    "Palestine": "#7f7f7f",   # Gray
    "Sudan": "#bcbd22",       # Yellow-green
    "Syria": "#17becf",       # Teal
    "Tunisia": "#ffbb78",     # Light Orange
    "Yemen": "#98df8a"        # Light Green
}
# -------------------------------------------------------------------------- Procedures
def Map(df,unit):
    df_grouped = df.groupby('Country', as_index=False)[f'{unit}'].sum()
    fig = px.choropleth( df_grouped, locations='Country', locationmode='country names', color=f'{unit}', color_continuous_scale='reds', 
                        title=f'Sales {unit} by Country', labels={f'{unit}': f'Sales {unit}'})
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, scope='world', projection_type='natural earth', center={"lat": 10, "lon": 30}, 
                 lataxis={"range": [-35, 40]}, lonaxis={"range": [-20, 65]}, ), title_font_size=24 )
    return fig

def Countries(df,unit):
    fig = px.histogram(data_frame=df, y='Country', x=f'{unit}', text_auto=True, color='Country', title=f'Distribution of {unit} by Country', 
                       labels={'Country': 'Country', f'{unit}': f'Sales {unit}'}, template='plotly_white', histfunc='sum',
                       color_discrete_map=color_discrete_map,)
    fig.update_layout(xaxis_title=f'{unit}', yaxis_title='Country', showlegend=False, font=dict(size=12),)
    fig.update_yaxes(categoryorder = 'total ascending')
    fig.update_traces( texttemplate='%{x:,.1f}', textposition='outside', textfont_size=10,)
    return fig

def CountryGrowth(df,unit):
    df_grouped = df.groupby(['Country', 'year'], as_index=False).agg({f'{unit}': 'sum', f'LastYear{unit}': 'sum' })
    df_grouped[f'{unit} Growth (%)'] = df_grouped.apply( lambda row: ((row[f'{unit}'] - row[f'LastYear{unit}']) / row[f'LastYear{unit}']) * 100 
                                                      if row[f'LastYear{unit}'] != 0 else None, axis=1)
    df_grouped = df_grouped.dropna(subset=[f'{unit} Growth (%)'])
    fig = px.bar(df_grouped, 
                 x='year', y=f'{unit} Growth (%)',  color='Country', barmode='group',title=f'{unit} Growth per Country by Year', 
                 labels={f'{unit} Growth (%)': f'{unit} Growth (%)'},color_discrete_map=color_discrete_map, height=600)
    fig.update_layout( title=f'{unit} Growth per Country by Year', title_x=0.5, title_font_size=20, title_font_family='Arial', 
                      xaxis_title='Year', yaxis_title=f'{unit} Growth (%)', xaxis_tickangle=-45,  plot_bgcolor='white', paper_bgcolor='white', 
                      showlegend=True, legend_title='Country', legend=dict(x=0.8, y=0.95), margin=dict(l=40, r=40, t=40, b=100))
    return fig

def CountryAtchivment(df,unit):
    df_grouped = df.groupby(['Country', 'year'], as_index=False).agg({f'{unit}': 'sum',f'Target{unit}': 'sum'})
    df_grouped[f'{unit} Achievement (%)'] = df_grouped.apply(lambda row: round((row[f'{unit}'] / row[f'Target{unit}']) * 100, 1) 
                                                           if row[f'Target{unit}'] != 0 else None, axis=1)
    df_grouped = df_grouped.dropna(subset=[f'{unit} Achievement (%)'])
    fig = px.bar(df_grouped, x='year', y=f'{unit} Achievement (%)', color='Country', barmode='group', 
                 title=f'{unit} Achievement per Country by Year', labels={f'{unit} Achievement (%)': f'{unit} Achievement (%)'},
                 color_discrete_map=color_discrete_map, height=600, text_auto='true')
    fig.update_layout(title=f'{unit} Achievement per Country by Year',title_x=0.5, title_font_size=20, title_font_family='Arial', 
                      xaxis_title='Year', yaxis_title=f'{unit} Achievement (%)',  xaxis_tickangle=-45, yaxis=dict(tickformat='.1f'), 
                      plot_bgcolor='white',paper_bgcolor='white',  showlegend=True, legend_title='Country', margin=dict(l=40, r=40, t=40, b=100))
    return fig

def Lines(df,unit):
    df_ordered = df.groupby('Line', as_index=False)[f'{unit}'].sum().sort_values(by=f'{unit}', ascending=False)
    fig = px.pie(data_frame=df_ordered,names='Line',values=f'{unit}', title='Distribution of Sales by Line', 
                 template='plotly_white',color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(font=dict(size=12), title_font=dict(size=16))
    fig.update_traces(textinfo='percent+label', textfont_size=12, pull=[0.1 if i == 0 else 0 for i in range(len(df_ordered))])
    return fig

def MainTypes(df,unit):
    df_ordered = df.groupby('MainType', as_index=False)[f'{unit}'].sum().sort_values(by=f'{unit}', ascending=False)
    fig = px.pie(data_frame=df_ordered,names='MainType',values=f'{unit}', title='Distribution of Sales by Main Type', 
                 template='plotly_white',color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(font=dict(size=12), title_font=dict(size=16))
    fig.update_traces(textinfo='percent+label', textfont_size=12, pull=[0.1 if i == 0 else 0 for i in range(len(df_ordered))])
    return fig

def Bricks(df,unit):
    brick_performance_country = df.groupby(['Country', 'Brick'])[f'{unit}'].sum().reset_index()
    brick_performance_country = brick_performance_country.sort_values(by=f'{unit}', ascending=False)
    top_10_bricks = brick_performance_country.head(10)
    top_10_bricks['Country_Brick'] = top_10_bricks['Country'] + ' - ' + top_10_bricks['Brick']
    fig = px.bar(top_10_bricks, x=f'{unit}', y='Country_Brick', title=f'Top 10 Bricks Performance by {unit} with Country and Brick',
                 labels={f'{unit}': f'Total {unit}', 'Country_Brick': 'Country - Brick'},color='Country_Brick', 
                 color_discrete_map=color_discrete_map, height=600)
    fig.update_layout(title=f'Top 10 Bricks Performance by {unit} with Country and Brick',title_x=0.5, title_font_size=20, 
                      title_font_family='Arial', xaxis_title=f'Total {unit}', yaxis_title='Country - Brick',  yaxis_tickangle=0, 
                      plot_bgcolor='white', paper_bgcolor='white', showlegend=False, margin=dict(l=250, r=40, t=40, b=100), 
                      xaxis=dict(showgrid=True),)
    return fig

def Trend(df,unit):
    df_grouped = df.groupby('Year-Month', as_index=False)[[f'{unit}', f'Target{unit}', f'LastYear{unit}']].sum()
    fig = px.line( data_frame=df_grouped, x='Year-Month', y=[f'{unit}', f'Target{unit}', f'LastYear{unit}'], title=f'Sales {unit} by Year and Month', 
                  labels={'Year-Month': 'Year-Month', f'{unit}': f'Sales {unit}', f'Target{unit}': 'Target Sales', f'LastYear{unit}' : f"Last Year {unit}" }, 
                  template='plotly_white', )
    fig.update_layout(xaxis_title='Time (Year-Month)', yaxis_title=f'Sales {unit}', font=dict(size=12), xaxis=dict(tickformat='%b %Y', dtick="M1",),)
    fig.update_traces(line=dict(width=2), marker=dict(size=4, symbol='circle'), )
    return fig

def Monthly(df,unit):
    pivot_table = pd.pivot_table(data=df, values=f'{unit}', columns='year', index='month', aggfunc='sum', fill_value=0)
    fig = px.imshow( pivot_table,labels=dict(x="Year", y="Month", color=f"Sales {unit}"), title=f"Monthly Sales {unit} by Year", 
                    color_continuous_scale=['rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(255, 0, 0)'], aspect="auto", text_auto=True,)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(pivot_table.columns), ticktext=[str(year) for year in pivot_table.columns]), 
                      yaxis=dict(tickmode='array', tickvals=list(pivot_table.index), ticktext=[calendar.month_name[i] for i in pivot_table.index]),
                      font=dict(size=12), coloraxis_colorbar=dict(title=f"Sales {unit}", tickvals=[pivot_table.min().min(), pivot_table.max().max()]), )
    return fig



def BusinessLines(df,unit):
    pivot_table = pd.pivot_table( data=df, values=f'{unit}', columns='Country', index='Line', aggfunc='sum', fill_value=0)
    fig = px.imshow( pivot_table, labels=dict(x="Country", y="Line", color=f"{unit}"), title=f"Line Performance Across Countries - {unit} ",  color_continuous_scale='reds', 
                    aspect="auto", text_auto=True, )
    fig.update_layout(font=dict(size=12), coloraxis_colorbar=dict(title=f"Sales {unit}", tickvals=[pivot_table.min().min(), pivot_table.max().max()]),)
    return fig

def Employees(df,unit):
    employee_columns = ['Emp1Name', 'Emp2Name', 'Emp3Name', 'Emp4Name']
    df_long = df.melt(id_vars=[f'{unit}'], value_vars=employee_columns, var_name='Employee', value_name='EmployeeName')
    employee_performance = df_long.groupby('EmployeeName')[f'{unit}'].sum().reset_index()
    employee_performance = employee_performance.sort_values(by=f'{unit}', ascending=False)
    top_10_employees = employee_performance.head(10)
    fig = px.bar( top_10_employees, x='EmployeeName', y=f'{unit}', title=f'Top 10 Employees Performance by {unit}',
                 labels={f'{unit}': f'Total {unit}', 'EmployeeName': 'Employee'}, color='EmployeeName',  
                 color_discrete_sequence=px.colors.qualitative.Set2, height=600)
    fig.update_layout( title=f'Top 10 Employees Performance by {unit}', title_x=0.5, title_font_size=20, title_font_family='Arial', 
                      xaxis_title='Employee', yaxis_title=f'Total {unit}', xaxis_tickangle=-45, plot_bgcolor='white', paper_bgcolor='white', 
                      showlegend=False, margin=dict(l=40, r=40, t=40, b=100))
    return fig

# --------------------------------------------------------------------------

def page1():
# --------------------------------------------------------
    # Overall Values
    total_value = df['Value'].sum()
    total_TargetValue = df['TargetValue'].sum()
    total_LastYearValue = df['LastYearValue'].sum()
    growth = ((total_value - total_LastYearValue) / total_LastYearValue) * 100
    achievement = (total_value / total_TargetValue) * 100
    
    # Create 5 columns for metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Total Value", value=f"£{total_value:,.0f}")
    with col2:
        st.metric(label="Total Target Value", value=f"£{total_TargetValue:,.0f}")
    with col3:
        st.metric(label="Total Last Year Value", value=f"£{total_LastYearValue:,.0f}")
    with col4:
        st.metric(label="Growth", value=f"{growth:.1f}%")
    with col5:
        st.metric(label="Achievement", value=f"{achievement:.1f}%", delta=f"{achievement - 100:.1f}%")
# --------------------------------------------------------
    st.plotly_chart(Map(df,'Value'))
    st.plotly_chart(Countries(df,'Value'))
    st.plotly_chart(CountryGrowth(df,'Value'))
    st.plotly_chart(CountryAtchivment(df,'Value'))
    st.plotly_chart(Bricks(df,'Value'))
    st.plotly_chart(Trend(df,'Value'))
    st.plotly_chart(Monthly(df,'Value'))
    col1 , col2  = st.columns(2)
    with col1 :
        st.plotly_chart(Lines(df,'Value'))
    with col2 :
        st.plotly_chart(MainTypes(df,'Value'))
    st.plotly_chart(BusinessLines(df,'Value'))
    st.plotly_chart(Employees(df,'Value'))
        
# --------------------------------------------------------
    
def page2():
    # Overall Quantitys
    total_Quantity = df['Quantity'].sum()
    total_TargetQuantity = df['TargetQuantity'].sum()
    total_LastYearQuantity = df['LastYearQuantity'].sum()
    growth = ((total_Quantity - total_LastYearQuantity) / total_LastYearQuantity) * 100
    achievement = (total_Quantity / total_TargetQuantity) * 100
    
    # Create 5 columns for metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Total Quantity", value=f"{total_Quantity:,.0f}")
    with col2:
        st.metric(label="Total Target Quantity", value=f"{total_TargetQuantity:,.0f}")
    with col3:
        st.metric(label="Total Last Year Quantity", value=f"{total_LastYearQuantity:,.0f}")
    with col4:
        st.metric(label="Growth", value=f"{growth:.1f}%")
    with col5:
        st.metric(label="Achievement", value=f"{achievement:.1f}%", delta=f"{achievement - 100:.1f}%")
# --------------------------------------------------------
    st.plotly_chart(Map(df,'Quantity'))
    st.plotly_chart(Countries(df,'Quantity'))
    st.plotly_chart(CountryGrowth(df,'Quantity'))
    st.plotly_chart(CountryAtchivment(df,'Quantity'))
    st.plotly_chart(Bricks(df,'Quantity'))
    st.plotly_chart(Trend(df,'Quantity'))
    st.plotly_chart(Monthly(df,'Quantity'))
    col1 , col2  = st.columns(2)
    with col1 :
        st.plotly_chart(Lines(df,'Quantity'))
    with col2 :
        st.plotly_chart(MainTypes(df,'Quantity'))
    st.plotly_chart(BusinessLines(df,'Quantity'))
    st.plotly_chart(Employees(df,'Quantity'))
    
# --------------------------------------------------------


pgs = {
    'Value' : page1,
    'Quantity' : page2
}
pg = st.sidebar.radio('Navigate Units ' ,options= pgs.keys())
Country = st.sidebar.multiselect('select Countries' , options=df_All['Country'].unique())
Year = st.sidebar.multiselect('Select Years', options=sorted(df_All['year'].unique()))
MainType = st.sidebar.multiselect('select Main Types' , options=df_All['MainType'].unique())
Brand = st.sidebar.multiselect('select Brands' , options=df_All['Brand'].unique())
Item = st.sidebar.multiselect('select Items' , options=df_All['Item'].unique())
Apply = st.sidebar.button('Apply')

if Apply:
    msk = (
        (df_All['Country'].isin(Country) | (len(Country) == 0))
        & (df_All['year'].isin(Year) | (len(Year) == 0))
        & (df_All['MainType'].isin(MainType) | (len(MainType) == 0))
        & (df_All['Brand'].isin(Brand) | (len(Brand) == 0))
        & (df_All['Item'].isin(Item) | (len(Item) == 0))
    )
    df = df_All[msk]
    pgs[pg]()



