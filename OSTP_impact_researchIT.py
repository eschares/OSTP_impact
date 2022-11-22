"""
Created on Mon Oct 24 11:59:06 2022

@author: eschares
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
# import os
# import re
# from datetime import datetime

st.set_page_config(page_title='OSTP Impact', page_icon="", layout='wide') #, initial_sidebar_state="expanded")


st.markdown('# Impact of the 2022 OSTP Memo:')
st.header('A Bibliometric Analysis of U.S. Federally Funded Publications, 2017-2021')
#st.write('Research IT')


with st.expander("About:"):
    st.write("""
        On August 25, 2022, the White House Office of Science and Technology Policy (OSTP) released a [memo](https://www.whitehouse.gov/ostp/news-updates/2022/08/25/ostp-issues-guidance-to-make-federally-funded-research-freely-available-without-delay/) regarding public access to scientific research.
        This updated guidance eliminated the 12-month embargo on publications arising from U.S. federal funding that had been in effect from a previous 2013 OSTP memo.
        
        The OSTP released a companion report with the memo, but it only provided a broad estimate of total numbers affected per year.

        **Therefore, [this study](https://arxiv.org/abs/2210.14871) seeks to more deeply investigate the characteristics of U.S. federally funded research** over a 5-year period from 2017-2021 to better understand the impact of the updated guidance. It uses a manually created custom filter in the Dimensions database to return only publications that arise from U.S. federal funding.
        
        Results show that an average of 265,000 articles are published each year that acknowledge U.S. federal funding agencies. These research outputs are further examined to look at patterns by publisher, journal title, institutions, and Open Access status.
        
        Each static graph from the journal article is reproduced here as an interactive version. Users can zoom, pan, and hover over data points for more detail.
        
        Additionally, you may search for a particular publisher, journal title, or research institution and label it and color it red to make it easier to distinguish on the graphs.

        The dataset and code are available at the Github repo, [https://github.com/eschares/OSTP_impact](https://github.com/eschares/OSTP_impact).
    """)


st.markdown("""---""")
st.header('Number')
st.write('The number of U.S. federally funded publications per year, as defined in the database Dimensions, are:')

d = {'Year': [2021, 2020, 2019, 2018, 2017],
    'Number': ['275,825', '277,407', '262,682', '259,518', '251,040']
    }
summary_df = pd.DataFrame(data=d)
summary_df



# Initialize session_state versions of to_true list
if 'publishers_to_change' not in st.session_state:
    st.session_state.publishers_to_change = []
if 'jnls_to_change' not in st.session_state:
    st.session_state.jnls_to_change = []
if 'resorgs_to_change' not in st.session_state:
    st.session_state.resorgs_to_change = []


st.markdown("""---""")
st.header('Publishers')
publishers_df = pd.read_csv('Publishers.csv', header=1)
if st.checkbox('Show raw publisher data'):
    st.subheader('Raw data')
    st.write(publishers_df)


st.write('Label a Publisher and turn it red on the charts:')
selected_publishers = st.multiselect('Publisher Name:', pd.Series(publishers_df['Name'].reset_index(drop=True)), help='Displayed in order provided by the underlying datafile')

if st.button('Find that Publisher'):
    for publisher_name in selected_publishers:
        #st.write(f"changed name, {publisher_name}")
        #clear_name_from_list(publisher_name)

        st.session_state.publishers_to_change.append(publisher_name)
        
# Actually do the changes in df; this runs every time the script runs but session_state lets me save the previous changes
#st.write('changing', st.session_state.publishers_to_change)
for name in st.session_state.publishers_to_change:
    title_filter = (publishers_df['Name'] == name)
    publishers_df.loc[title_filter, 'color'] = 'red'


### Publishers ###
st.subheader('By absolute number')
fig = px.scatter(publishers_df, x='Worldwide',y='FF Pubs', color='color',
                color_discrete_sequence=['blue', 'red'],
                log_x='True', 
                hover_name='Name', 
                hover_data={'color':False},
                trendline='ols',
                trendline_scope='overall',
                trendline_color_override='blue',
                #text='Name'
                )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=800, width=1200,
    title_text='Publishers Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Total number of publications worldwide 2017-2021 [log]',
    yaxis_title = 'Number of U.S. Federally Funded publications 2017-2021',
    showlegend = False
)

publishers_df2 = publishers_df[ (publishers_df['FF Pubs'] > 29180) | (publishers_df['Worldwide']>427000) | publishers_df['Name'].isin(selected_publishers)]
num_rows = publishers_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(publishers_df2['Worldwide']).iloc[i],
                    y=publishers_df2["FF Pubs"].iloc[i],
                    text = publishers_df2["Name"].iloc[i],
                    showarrow = False,
                        ax = 0,
                        yshift = 10
                        #ay = -10
                    )

fig.add_annotation(x=4.593, y=23500,
            text="American Geophysical Union",
            showarrow=False,
            arrowhead=0)

fig.add_annotation(x=4.39, y=14000,
            text="American Astronomical Society",
            showarrow=True,
            arrowhead=0,
            ax = -30,
            ay = -30)


st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)




st.subheader('By percentage')
fig = px.scatter(publishers_df, x='Worldwide',y='percentage', color='color',
                color_discrete_sequence=['blue', 'red'],
                hover_name='Name', 
                hover_data={'color':False},
                #text='Name',
                log_x='True',
                )


fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Publishers Total Publications vs. Percentage U.S. Federally Funded',
    xaxis_title = 'Total number of Publications 2017-2021 [log]',
    yaxis_title = "Percentage of Publications that are FF, 2017-2021",
    showlegend = False
)

publishers_df2 = publishers_df[ (publishers_df['percentage'] > 51) | (publishers_df['Worldwide']>200000) | publishers_df['Name'].isin(selected_publishers)]
num_rows = publishers_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(publishers_df2['Worldwide']).iloc[i],
                    y=publishers_df2["percentage"].iloc[i],
                    text = publishers_df2["Name"].iloc[i],
                    showarrow = False,
                        ax = 0,
                        yshift = 10
                        #ay = -10
                    )

fig.add_annotation(x=3.576, y=52.5,
            text="Am. Assn of Immunologists",
            showarrow=False,
            arrowhead=0)


fig.add_annotation(x=3.785, y=50,
            text="Soc. for Neuroscience",
            showarrow=True,
            arrowhead=0,
                ax=30,
                ay=18)

fig.add_annotation(x=4.593, y=44.7,
            text="Am. Geophysical Union (AGU)",
            showarrow=False,
            arrowhead=0)

fig.add_annotation(x=4.096, y=44.8,
            text="Am. Physciological Soc.",
            showarrow=True,
            arrowhead=0,
                ax=30,ay=16)

fig.add_annotation(x=5.02, y=27.7,
            text="Am. Physical Soc.",
            showarrow=True,
            arrowhead=0,
                ax=30,ay=-16)


st.plotly_chart(fig, use_container_width=True)








st.markdown("""---""")
### Journals ###
st.header('Journal Titles')

jnl_df = pd.read_csv('Journal_titles.csv', header=1)
if st.checkbox('Show raw journal data'):
    st.subheader('Raw data')
    st.write(jnl_df)



st.write('Label a Journal and turn it red on the charts:')
selected_journals = st.multiselect('Journal Name:', pd.Series(jnl_df['Name'].reset_index(drop=True)), help='Displayed in order provided by the underlying datafile')

if st.button('Find that Journal'):
    for journal_name in selected_journals:
        #st.write(f"changed name, {journal_name}")
        #clear_name_from_list(publisher_name)

        st.session_state.jnls_to_change.append(journal_name)

# Actually do the changes in df; this runs every time the script runs but session_state lets me save the previous changes
#st.write('changing', st.session_state.jnls_to_change)
for name in st.session_state.jnls_to_change:
    title_filter = (jnl_df['Name'] == name)
    jnl_df.loc[title_filter, 'color'] = 'red'



st.subheader('Absolute Number')

fig = px.scatter(jnl_df, x='Worldwide',y='FF Pubs', color='color',
                 log_x='True', 
                 hover_name='Name', 
                 hover_data={'color':False},
                 trendline='ols',
                 trendline_scope='overall',
                 trendline_color_override='blue',
                )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Journal Titles: Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Total number of publications worldwide 2017-2021 [log]',
    yaxis_title = 'Number of U.S. Federally Funded publications 2017-2021',
    showlegend = False
)


jnl_df2 = jnl_df[ (jnl_df['FF Pubs'] > 8000) | (jnl_df['Worldwide']>52000) | (jnl_df['Name'].str.contains('Physical Review B|Chemical Society')) | jnl_df['Name'].isin(selected_journals) ]
num_rows = jnl_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(jnl_df2['Worldwide']).iloc[i],
                       y=jnl_df2["FF Pubs"].iloc[i],
                       text = jnl_df2["Name"].iloc[i],
                       showarrow = False,
                        ax = 0,
                        yshift = 12
                      )
    
fig.add_annotation(x=4.433, y=6940,
            text="The FASEB Journal",
            showarrow=True,
            arrowhead=0,
                  ay=18,
                  ax=10)


st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)


st.subheader('Percentage')

fig = px.scatter(jnl_df[jnl_df['Worldwide']!=0], x='Worldwide',y='Percentage', color='color',
                 log_x=False,
                 hover_name='Name', 
                 hover_data={'color':False},
                )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Journal Titles: Total vs. Percentage U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Number of total publications worldwide 2017-2021 [log]',
    yaxis_title = 'Percentage FF, 2017-2021',
    showlegend = False
)

jnl_df2 = jnl_df[ (jnl_df['Worldwide'] > 55000) | (jnl_df['Percentage']>53) | ((jnl_df['Percentage']>40) & (jnl_df['Percentage']<44)) | jnl_df['Name'].isin(selected_journals)]
num_rows = jnl_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=jnl_df2['Worldwide'].iloc[i],
                       y=jnl_df2["Percentage"].iloc[i],
                       text = jnl_df2["Name"].iloc[i],
                       showarrow = False,
                        ax = 5,
                        yshift = 12
                        #ay = -12
                      )

fig.add_annotation(x=20344, y=53.3,
            text="PNAS",
            showarrow=False,
            arrowhead=0,)

fig.add_annotation(x=8728, y=53,
            text="eLife",
            showarrow=True,
            arrowhead=0,
                  ax=30,
                  ay=5)

fig.add_annotation(x=6463, y=52.4,
            text="Cell Reports",
            showarrow=True,
            arrowhead=0,
                  ax=-50,
                  ay=5)

fig.add_annotation(x=4447, y=50.3,
            text="Jnl of Neuroscience",
            showarrow=True,
            arrowhead=0,
                  ax=-50,
                  ay=15)

fig.add_annotation(x=8384, y=48.5,
            text="Jnl of Biological Chemistry",
            showarrow=True,
            arrowhead=0,
                  ax=100,
                  ay=0)

fig.add_annotation(x=7077, y=47.63,
            text="Science Advances",
            showarrow=True,
            arrowhead=0,
                  ax=-35,
                  ay=12)


st.plotly_chart(fig, use_container_width=True)






st.markdown("""---""")
### Research Institutions ###
st.header('Research Institutions')

institution_df = pd.read_csv('ResOrgs.csv', header=1, encoding='latin1')
if st.checkbox('Show raw institution data'):
    st.subheader('Raw data')
    st.write(institution_df)


st.write('Label a Research Institution and turn it red on the charts:')
selected_resorgs = st.multiselect('Institution Name:', pd.Series(institution_df['Name'].reset_index(drop=True)), help='Displayed in order provided by the underlying datafile')

if st.button('Find that Institution'):
    for resorg_name in selected_resorgs:
        #st.write(f"changed name, {resorg_name}")
        #clear_name_from_list(publisher_name)

        st.session_state.resorgs_to_change.append(resorg_name)

# Actually do the changes in df; this runs every time the script runs but session_state lets me save the previous changes
#st.write('changing', st.session_state.resorgs_to_change)
for name in st.session_state.resorgs_to_change:
    title_filter = (institution_df['Name'] == name)
    institution_df.loc[title_filter, 'color'] = 'red'





st.subheader('Absolute Number')

fig = px.scatter(institution_df, x='AllUS',y='FF Pubs', color='color',
                 #symbol='Name',
                 log_x='True', 
                 hover_name='Name', 
                 hover_data={'color':False},
                 trendline='ols',
                 trendline_scope='overall',
                 trendline_color_override='blue',
                 #text='Name'
                )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Research Institutions: Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Total number of publications worldwide 2017-2021 [log]',
    yaxis_title = 'Number of U.S. Federally Funded publications 2017-2021',
    showlegend = False
)


inst_df2 = institution_df[ (institution_df['FF Pubs'] > 30000) | (institution_df['AllUS']>65000) | (institution_df['Name'].str.contains('Lawrence Berk|Ridge National|Argonne|Iowa State')) | institution_df['Name'].isin(selected_resorgs) ]
num_rows = inst_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(inst_df2['AllUS']).iloc[i],
                       y=inst_df2["FF Pubs"].iloc[i],
                       text = inst_df2["Name"].iloc[i],
                       # showarrow = True,
                        ax = -80,
                        ay = -12
                      )

st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)




st.subheader('Percentage')

fig = px.scatter(institution_df[institution_df['AllUS']!=0], x='AllUS',y='Percentage', color='color',
                 #symbol='Name', 
                 hover_name='Name', 
                 hover_data={'color':False},
                 log_x=False,
                 #text='Name'
                )

fig.update_traces(textposition='top right')

fig.update_layout(
    height=700, width=1200,
    title_text='Research Institutions: Total vs. Percentage U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Number of Total publications 2017-2021',
    yaxis_title = "Percentage FF, 2017-2021",
    showlegend = False
)

inst_df2 = institution_df[ (institution_df['AllUS'] > 80000) | (institution_df['Percentage']>99) | (institution_df['Name'].str.contains('Iowa State|Larence Berk|Ridge Natioal|Argone')) | institution_df['Name'].isin(selected_resorgs)]
num_rows = inst_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=inst_df2['AllUS'].iloc[i],
                       y=inst_df2["Percentage"].iloc[i],
                       text = inst_df2["Name"].iloc[i],
                       #showarrow = True,
                        ax = 55,
                        ay = -12
                      )

fig.add_shape(type="rect",
    x0=0, y0=76, x1=21500, y1=92,
    line=dict(color="RoyalBlue"),
    #layer="below",
)

fig.add_annotation(x=24500, y=87,
            text="National Laboratories",
            showarrow=False,
            arrowhead=0,)

st.plotly_chart(fig, use_container_width=True)





st.markdown("""---""")
### Open Access ###
st.header('Open Access Status')

st.subheader('Federally Funded Publications')

OA_df = pd.read_csv('OA_FF.csv', header=1, encoding='latin1')
if st.checkbox('Show raw OA data on Federally Funded pubs'):
    st.subheader('Raw data')
    st.write(OA_df)

fig = px.histogram(OA_df, x='Year', y='Count', color='Mode',
                  barnorm='percent', text_auto='.2f',
                  color_discrete_sequence=["gray", "green", "gold", "darkgoldenrod", "red"],
                   title='Open Access status of FF publications')

fig.update_layout(
    height=700, width=700,
    title_text='Open Access Status of U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Year',
    yaxis_title = 'Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=False)



st.subheader('Worldwide Publications')

OA_WW_df = pd.read_csv('OA_worldwide.csv', header=0, encoding='latin1')
if st.checkbox('Show raw OA data on Worldwide pubs'):
    st.subheader('Raw data')
    st.write(OA_WW_df)

fig = px.histogram(OA_WW_df, x='Year', y='Count', color='Mode',
                  barnorm='percent', text_auto='.2f',
                  color_discrete_sequence=["gray", "green", "gold", "darkgoldenrod", "red"],
                   title='Open Access status of FF publications')

fig.update_layout(
    height=700, width=700,
    title_text='Open Access Status of all Publications, 2017-2021',
    xaxis_title = 'Year',
    yaxis_title = 'Percentage All Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=False)


st.markdown("""---""")
### OA of publishers ###
st.subheader('OA Status of Federally Funded pubs by Publisher')
oa_by_pub_df = pd.read_csv('Publishers.csv', header=1)

if st.checkbox('Show raw publisher OA data'):
    st.subheader('Raw data')
    st.write(oa_by_pub_df)


sortby = st.radio(
    'The following charts will show the highest 32 publishers. How do you want to sort?', ('Total Number of Federally Funded pubs','% of Closed', '% of Green', '% of Gold', '% of Bronze', '% of Hybrid'))

if sortby == 'Total Number of Federally Funded pubs':
    oa_by_pub_df = oa_by_pub_df.sort_values(by='FF Pubs', ascending=False)
elif sortby == '% of Closed':
    oa_by_pub_df = oa_by_pub_df.sort_values(by='% OSTP closed', ascending=False)
elif sortby == '% of Green':
    oa_by_pub_df = oa_by_pub_df.sort_values(by='% OSTP Green', ascending=False)
elif sortby == '% of Gold':
    oa_by_pub_df = oa_by_pub_df.sort_values(by='% OSTP Gold', ascending=False)
elif sortby == '% of Bronze':
    oa_by_pub_df = oa_by_pub_df.sort_values(by='% OSTP Bronze', ascending=False)
elif sortby == '% of Hybrid':
    oa_by_pub_df = oa_by_pub_df.sort_values(by='% OSTP Hybrid', ascending=False)


fig = px.histogram(oa_by_pub_df.iloc[:16], x='Name', y=['% OSTP closed', '% OSTP Green', '% OSTP Gold', '% OSTP Bronze', '% OSTP Hybrid'], #color='Mode',
                  barnorm='percent', text_auto='.2f',
                  color_discrete_sequence=["gray", "green", "gold", "darkgoldenrod", "red"],
                  title='Open Access status of FF publications')#, facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='Open Access Status of U.S. Federally Funded Publications, by Publisher 2017-2021 <br> Numbers 1-16 based on condition selected',
    xaxis_title = 'Publisher',
    yaxis_title = 'Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=False)



fig = px.histogram(oa_by_pub_df.iloc[17:32], x='Name', y=['% OSTP closed', '% OSTP Green', '% OSTP Gold', '% OSTP Bronze', '% OSTP Hybrid'], #color='Mode',
                  barnorm='percent', text_auto='.2f',
                  color_discrete_sequence=["gray", "green", "gold", "darkgoldenrod", "red"],
                  title='Open Access status of FF publications')#, facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='Open Access Status of U.S. Federally Funded Publications, by Publisher 2017-2021 <br> Numbers 17-32 based on condition selected',
    xaxis_title = 'Publisher',
    yaxis_title = 'Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=False)



st.markdown("""---""")
### OA of Journals ###
st.subheader('OA Status of Federally Funded pubs by Journal title')
oa_by_jnl_df = pd.read_csv('Journal_titles.csv', header=1)

if st.checkbox('Show raw Journal title OA data'):
    st.subheader('Raw data')
    st.write(oa_by_jnl_df)


sortby = st.radio(
    'The following charts will show the highest 32 journal titles. How do you want to sort?', ('Total Number of Federally Funded pubs','% of Closed', '% of Green', '% of Gold', '% of Bronze', '% of Hybrid'))

if sortby == 'Total Number of Federally Funded pubs':
    oa_by_jnl_df = oa_by_jnl_df.sort_values(by='FF Pubs', ascending=False)
elif sortby == '% of Closed':
    oa_by_jnl_df = oa_by_jnl_df.sort_values(by='% OSTP closed', ascending=False)
elif sortby == '% of Green':
    oa_by_jnl_df = oa_by_jnl_df.sort_values(by='% OSTP Green', ascending=False)
elif sortby == '% of Gold':
    oa_by_jnl_df = oa_by_jnl_df.sort_values(by='% OSTP Gold', ascending=False)
elif sortby == '% of Bronze':
    oa_by_jnl_df = oa_by_jnl_df.sort_values(by='% OSTP Bronze', ascending=False)
elif sortby == '% of Hybrid':
    oa_by_jnl_df = oa_by_jnl_df.sort_values(by='% OSTP Hybrid', ascending=False)


fig = px.histogram(oa_by_jnl_df.iloc[:16], x='Name', y=['% OSTP closed', '% OSTP Green', '% OSTP Gold', '% OSTP Bronze', '% OSTP Hybrid'], #color='Mode',
                  barnorm='percent', text_auto='.2f',
                  color_discrete_sequence=["gray", "green", "gold", "darkgoldenrod", "red"],
                  title='Open Access status of FF publications')#, facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='Open Access Status of U.S. Federally Funded Publications, by Journal Title 2017-2021 <br> Numbers 1-16 based on condition selected',
    xaxis_title = 'Journal Title',
    yaxis_title = 'Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=False)



fig = px.histogram(oa_by_jnl_df.iloc[17:32], x='Name', y=['% OSTP closed', '% OSTP Green', '% OSTP Gold', '% OSTP Bronze', '% OSTP Hybrid'], #color='Mode',
                  barnorm='percent', text_auto='.2f',
                  color_discrete_sequence=["gray", "green", "gold", "darkgoldenrod", "red"],
                  title='Open Access status of FF publications')#, facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='Open Access Status of U.S. Federally Funded Publications, by Journal Title 2017-2021 <br> Numbers 17-32 based on condition selected',
    xaxis_title = 'Journal Title',
    yaxis_title = 'Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=False)



##### Footer in sidebar #####
#st.subheader("About")
github = "[![GitHub repo stars](https://img.shields.io/github/stars/eschares/ostp_impact?logo=github&style=social)](<https://github.com/eschares/ostp_impact>)"
twitter = "[![Twitter Follow](https://img.shields.io/twitter/url?label=Twitter%20%40eschares&style=social&url=https%3A%2F%2Ftwitter.com%2Feschares)](<https://twitter.com/eschares>)"
zenodo = "[![DOI](https://zenodo.org/badge/554219142.svg)](https://zenodo.org/badge/latestdoi/554219142)"

mastodon = "[![Mastodon Follow](https://img.shields.io/mastodon/follow/108216956438964080?domain=https://scholar.social&style=social)](<https://scholar.social/@eschares>)"


html_string = "<p style=font-size:13px>v1.0, last modified 11/23/22 <br />Created by Eric Schares, Iowa State University <br /> <b>eschares@iastate.edu</b></p>"
st.markdown(html_string, unsafe_allow_html=True)

st.write(zenodo + " " + github)
st.write(mastodon + " " + twitter)
#st.write(twitter)


html_string_statcounter = '''
<!-- Default Statcounter code for OSTP Impact, Streamlit
Cloud
https://eschares-ostp-impact-ostp-impact-zgsykn.streamlitapp.com/
-->
<script type="text/javascript">
var sc_project=12810611; 
var sc_invisible=1; 
var sc_security="c7ce9654"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/12810611/0/c7ce9654/1/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
'''

components.html(html_string_statcounter)  # JavaScript works