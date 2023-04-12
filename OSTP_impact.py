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
st.markdown("""##### Companion website showing interactive versions of graphs from the study at [https://doi.org/10.1162/qss_a_00237](https://doi.org/10.1162/qss_a_00237).""")
st.markdown("""###### by Eric Schares, Iowa State University,  [eschares@iastate.edu](mailto:eschares@iastate.edu)""")
#st.write('Research IT')


with st.expander("About:"):
    st.write("""
        On August 25, 2022, the White House Office of Science and Technology Policy (OSTP) released a [memo](https://www.whitehouse.gov/ostp/news-updates/2022/08/25/ostp-issues-guidance-to-make-federally-funded-research-freely-available-without-delay/) regarding public access to scientific research.
        This updated guidance eliminated the 12-month embargo on publications arising from U.S. federal funding that had been in effect from a previous 2013 OSTP memo.
        
        The OSTP released a companion report with the memo, but it only provided a broad estimate of total numbers affected per year.

        **Therefore, [this study and website](https://doi.org/10.1162/qss_a_00237) seek to more deeply investigate the characteristics of U.S. federally funded research** over a 5-year period from 2017-2021 to better understand the impact of the updated guidance. It uses a manually created custom filter in the Dimensions database to return only publications that arise from U.S. federal funding.
        
        **Results** show that an average of 265,000 articles are published each year that acknowledge U.S. federal funding agencies. These research outputs are further examined to look at patterns by publisher, journal title, institutions, and Open Access status.
        
    """)

with st.expander("How to use:"):
    st.write("""
        Each static graph from the journal article at [https://doi.org/10.1162/qss_a_00237](https://doi.org/10.1162/qss_a_00237) is included here as an interactive version.
        
    Prefer an overview video? [This webinar](https://youtu.be/58FVVQaDtrA?t=991) walks through the various graphs and demonstrates how to interpret this site.
    
    Users can zoom, pan, and hover over data points for more detail. Double-clicking the graph will reset the axes and zoom back out. Choose to display the y-axis in linear or log scale.
        
    Additionally, you may search for a particular publisher, journal title, or research institution to label and color it red to make it easier to find on the graphs.

    **Publishers**
    - Absolute Numbers
    - Percentage of U.S. Federally Funded research

    **Journal titles**
    - Absolute Numbers
    - Percentage of U.S. Federally Funded research

    **Research Institutions**
    - Absolute Numbers
    - Percentage of U.S. Federally Funded research

    **Open Access Status**
    - U.S. Federally Funded
    - Overall publications
    - By Publisher
    - By Journal title
    
    The datasets and code are available at the Github repo, [https://github.com/eschares/OSTP_impact](https://github.com/eschares/OSTP_impact). 
    """)


st.markdown("""---""")
st.header('Number')
st.write('The number of U.S. federally funded publications per year, as defined in the database Dimensions, are:')

d = {'Year': [2021, 2020, 2019, 2018, 2017],
    'Number': ['275,825', '277,407', '262,682', '259,518', '251,040']
    }
summary_df = pd.DataFrame(data=d)
summary_df
st.write('The 5-year average is **265,294** publications, and the 5-year sum is 1.326M.')
st.write('This represents **33%** of all U.S. domestic research output over these 5 years (n=4.020M), and **4.5%** of total global research output over these 5 years (n=29.646M).')


# Initialize session_state versions of to_true list
if 'publishers_to_change' not in st.session_state:
    st.session_state.publishers_to_change = []
if 'jnls_to_change' not in st.session_state:
    st.session_state.jnls_to_change = []
if 'resorgs_to_change' not in st.session_state:
    st.session_state.resorgs_to_change = []


#### Start Publishers section ###

st.markdown("""---""")
st.header('Publishers')
publishers_df = pd.read_csv('Publishers.csv', header=1)
publishers_df = publishers_df[publishers_df['Worldwide']!=0]
if st.checkbox('Show raw publisher data'):
    st.subheader('Raw data')
    st.write(publishers_df)


#st.write('Label a Publisher and turn it red on the charts:')
selected_publishers = st.multiselect('Label a Publisher and turn it red on the charts:', pd.Series(
    publishers_df['Name'].reset_index(drop=True)), help='Displayed in order provided by the underlying datafile')

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


### Publisher graph ###
st.subheader('By absolute number')

publishers_logy = st.radio(
    'Display the y-axis as:', ('Publishers Log', 'Publishers Linear'))

if publishers_logy == 'Publishers Linear':
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

    publishers_df2 = publishers_df[ (publishers_df['FF Pubs'] > 88000) | 
                                    (publishers_df['Worldwide'] > 1000000) |
                                    (publishers_df['Name'].str.contains('American Chemical Society|Oxford|American Physical Society|De Gruyter|eLife')) |
                                    (publishers_df['Name'].isin(selected_publishers))
                                    ]
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
                arrowhead=0
                )

    fig.add_annotation(x=4.39, y=14000,
                text="American Astronomical Society",
                showarrow=True,
                arrowhead=0,
                ax = -30,
                ay = -30)

    fig.update_layout(yaxis_title='Number of U.S. Federally Funded publications 2017-2021')

else:   # log(y)
    fig = px.scatter(publishers_df, x='Worldwide', y='FF Pubs', color='color',
                 color_discrete_sequence=['blue', 'red'],
                 log_x='True',
                 log_y='True',
                 hover_name='Name',
                 hover_data={'color': False},
                 trendline='ols',
                 trendline_scope='overall',
                 trendline_color_override='blue',
                 #text='Name'
                 )

    publishers_df2 = publishers_df[ (publishers_df['FF Pubs'] > 88000) |
                                    (publishers_df['Worldwide'] > 1000000) |
                                    #(publishers_df['Name'].str.contains('American Chemical Society|Oxford|American Physical Society|De Gruyter|eLife')) |
                                    (publishers_df['Name'].isin(selected_publishers))
                                    ]
    num_rows = publishers_df2.shape[0]
    for i in range(num_rows):
            fig.add_annotation(x=np.log10(publishers_df2['Worldwide']).iloc[i],
                            y=np.log10(publishers_df2["FF Pubs"]).iloc[i],
                            text=publishers_df2["Name"].iloc[i],
                            ax=0,
                            ay = -10
                            )

    fig.add_annotation(x=4.593, y=4.22,
                    text="American Geophysical Union",
                    ay=-10,
                    arrowhead=0)

    fig.add_annotation(x=4.39, y=4.1455,
                    text="American Astronomical Society",
                    showarrow=True,
                    ax=-150,
                    ay=-10)

    fig.add_annotation(x=5.475, y=4.79,
                   text="ACS",
                   ay=-10)

    fig.add_annotation(x=5.769, y=4.7,
                   text="OUP",
                   ay=-10)

    fig.add_annotation(x=5.022, y=4.465,
                   text="APS",
                   ay=-10)

    fig.add_annotation(x=5.63, y=3.178,
                   text="De Gruyter",
                   ay=-10)

    fig.add_annotation(x=3.94, y=3.665,
                   text="eLife",
                   ay=-10)
                 
    fig.update_layout(yaxis_title='Number of U.S. Federally Funded publications 2017-2021 [log]')


fig.update_traces(textposition='top center')

fig.update_layout(
    height=800, width=1200,
    title_text='Publishers Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title='Total number of publications worldwide 2017-2021 [log]',
    #yaxis_title='Number of U.S. Federally Funded publications 2017-2021 [log]',
    showlegend=False,
    font_size=14
)

st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is', px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)




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
    showlegend = False,
    font_size = 14
)

publishers_df2 = publishers_df[ (publishers_df['percentage'] > 60) | 
                                (publishers_df['Worldwide']>588000) | 
                                publishers_df['Name'].isin(selected_publishers)
                                ]
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

fig.add_annotation(x=4.39, y=57,
                   text="Am. Astronomical Society",
                   showarrow=True,
                   arrowhead=0,
                   ax=-20,
                   ay=-18)

fig.add_annotation(x=4.593, y=42.7,
                   text="Am. Geophysical Union (AGU)",
                   showarrow=True,
                   ax=20,
                   arrowhead=0)

fig.add_annotation(x=4.096, y=44.8,
                   text="Am. Physciological Soc.",
                   showarrow=True,
                   arrowhead=0,
                   ax=-30, ay=16)

fig.add_annotation(x=5.02, y=27.7,
                   text="Am. Physical Soc.",
                   showarrow=True,
                   arrowhead=0,
                   ax=0, ay=-16)

fig.add_annotation(x=5.475, y=20.7,
                   text="ACS",
                   #showarrow=True,
                   #arrowhead=0,
                   ax=30, ay=-16)

fig.add_annotation(x=3.94, y=53,
                   text="eLife",
                   #showarrow=True,
                   #arrowhead=0,
                   ax=0, ay=-10)


st.plotly_chart(fig, use_container_width=True)





st.markdown("""---""")
### Journals section ###
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

journals_logy = st.radio(
    'Display the y-axis as:', ('Journals Log', 'Journals Linear'))

if journals_logy == 'Journals Linear':
    fig = px.scatter(jnl_df, x='Worldwide',y='FF Pubs', color='color',
                    log_x='True', 
                    hover_name='Name', 
                    hover_data={'color':False},
                    trendline='ols',
                    trendline_scope='overall',
                    trendline_color_override='blue',
                    )

    jnl_df2 = jnl_df[ (jnl_df['FF Pubs'] > 8000) | 
                      (jnl_df['Worldwide']>52000) | 
                      (jnl_df['Name'].str.contains('Physical Review B|Chemical Society')) | 
                      jnl_df['Name'].isin(selected_journals) ]
    num_rows = jnl_df2.shape[0]
    for i in range(num_rows):
        fig.add_annotation(x=np.log10(jnl_df2['Worldwide']).iloc[i],
                        y=jnl_df2["FF Pubs"].iloc[i],
                        text = jnl_df2["Name"].iloc[i],
                        showarrow = False,
                        ax = 0,
                        yshift = 12
                        )

        fig.add_annotation(x=3.941, y=4625,
                   text="eLife",
                   ay=-10)
        
    fig.update_layout(yaxis_title='Number of U.S. Federally Funded publications 2017-2021')

else: # log(y)
    fig = px.scatter(jnl_df, x='Worldwide', y='FF Pubs', color='color',
                     log_x='True',
                     log_y='True',
                     hover_name='Name',
                     hover_data={'color': False},
                     trendline='ols',
                     trendline_scope='overall',
                     trendline_color_override='blue',
                     )
    jnl_df2 = jnl_df[(jnl_df['FF Pubs'] > 8000) |
                     (jnl_df['Worldwide'] > 52000) |
                     (jnl_df['Name'].str.contains('XYZ')) |
                     jnl_df['Name'].isin(selected_journals)]
    num_rows = jnl_df2.shape[0]
    for i in range(num_rows):
        fig.add_annotation(x=np.log10(jnl_df2['Worldwide']).iloc[i],
                           y=np.log10(jnl_df2["FF Pubs"]).iloc[i],
                           text=jnl_df2["Name"].iloc[i],
                           showarrow=False,
                           ax=0,
                           yshift=12
                           )

    fig.add_annotation(x=4.415, y=3.847,
                       text="Physical Review B",
                       ay=-8)

    fig.add_annotation(x=4.11, y=3.747,
                   text="Jnl of Am. Chem. Soc.",
                   ay=-10)

    fig.add_annotation(x=3.941, y=3.665,
                   text="eLife",
                   ay=-10)

    fig.update_layout(
        yaxis_title='Number of U.S. Federally Funded publications 2017-2021 [log]')

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Journal Titles: Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title='Total number of publications worldwide 2017-2021 [log]',
    #yaxis_title='Number of U.S. Federally Funded publications 2017-2021',
    showlegend=False,
    font_size = 14
)

st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)




st.subheader('Percentage')

fig = px.scatter(jnl_df[jnl_df['Worldwide']!=0], x='Worldwide',y='Percentage', color='color',
                 log_x=True,
                 hover_name='Name', 
                 hover_data={'color':False},
                )

fig.update_traces(textposition='top right')

fig.update_layout(
    height=700, width=1200,
    title_text='Journal Titles: Total vs. Percentage U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Number of total publications worldwide 2017-2021 [log]',
    yaxis_title = 'Percentage FF, 2017-2021',
    showlegend = False,
    font_size = 14
)

jnl_df2 = jnl_df[ (jnl_df['Worldwide'] > 55000) |
                  (jnl_df['Percentage']>70) | 
                  jnl_df['Name'].isin(selected_journals)]
num_rows = jnl_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(jnl_df2['Worldwide']).iloc[i],
                       y=jnl_df2["Percentage"].iloc[i],
                       text = jnl_df2["Name"].iloc[i],
                       showarrow = False,
                       ax = 5,
                       yshift = 12
                       #ay = -12
                      )

fig.add_annotation(x=4.308, y=52.3,
                   text="PNAS",
                   ay=-18)
#showarrow=False,
#arrowhead=0,)

fig.add_annotation(x=3.94, y=53,
                   text="eLife",
                   #showarrow=True,
                   #arrowhead=0,
                   ax=30,
                   ay=-10)

fig.add_annotation(x=3.81, y=52.4,
                   text="Cell Reports",
                   #showarrow=True,
                   #arrowhead=0,
                   ax=-5,
                   ay=-25)

fig.add_annotation(x=3.648, y=50.3,
                   text="Jnl of Neuroscience",
                   showarrow=True,
                   arrowhead=0,
                   ax=0,
                   ay=-20)

fig.add_annotation(x=3.92, y=48.5,
                   text="Jnl of Biological Chemistry",
                   showarrow=True,
                   arrowhead=0,
                   ax=100,
                   ay=0)

fig.add_annotation(x=3.85, y=47.63,
                   text="Science Advances",
                   showarrow=True,
                   arrowhead=0,
                   ax=0,
                   ay=20)

fig.add_annotation(x=4.473, y=40.4,
                   text="Nature Communications",
                   showarrow=True,
                   arrowhead=0,
                   ax=0,
                   ay=-18)

fig.add_annotation(x=4.187, y=57.9,
                   text="The Astrophysical Journal",
                   showarrow=True,
                   arrowhead=0,
                   ax=0,
                   ay=-18)

fig.add_annotation(x=4.11, y=43.3,
                   text="Jnl ACS",
                   showarrow=True,
                   arrowhead=0,
                   ax=0,
                   ay=-10)

fig.add_annotation(x=4.42, y=27.06,
                   text="Physical Review B",
                   showarrow=True,
                   arrowhead=0,
                   ax=30,
                   ay=-10)


st.plotly_chart(fig, use_container_width=True)






st.markdown("""---""")
### Research Institutions ###
st.header('Research Institutions')

institution_df = pd.read_csv('ResOrgs.csv', header=1, encoding='latin1')
institution_df = institution_df[institution_df['AllUS']!=0]
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

institution_logy = st.radio(
    'Display the y-axis as:', ('Institution Log', 'Institution Linear')
)

if institution_logy == 'Institution Linear':
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

    inst_df2 = institution_df[ (institution_df['FF Pubs'] > 90000) | 
                               (institution_df['AllUS']>520000) | 
                               (institution_df['Name'].str.contains('Lawrence Berk|Oak Ridge Nat|Argonne|Iowa State|Harvard University|Ann Arbor|University of Washington')) | 
                               (institution_df['Name'].isin(selected_resorgs)) ]
    num_rows = inst_df2.shape[0]
    for i in range(num_rows):
        fig.add_annotation(x=np.log10(inst_df2['AllUS']).iloc[i],
                           y=inst_df2["FF Pubs"].iloc[i],
                           text = inst_df2["Name"].iloc[i],
                           # showarrow = True,
                            ax = -80,
                            ay = -12
                          )
    
    fig.update_layout(yaxis_title='Number of U.S. Federally Funded publications 2017-2021')

else: # log(y)
    fig = px.scatter(institution_df, x='AllUS', y='FF Pubs', color='color',
                     #symbol='Name',
                     log_x='True',
                     log_y='True',
                     hover_name='Name',
                     hover_data={'color': False},
                     trendline='ols',
                     trendline_scope='overall',
                     trendline_color_override='blue',
                     )

    inst_df2 = institution_df[(institution_df['FF Pubs'] > 90000) |
                              (institution_df['AllUS'] > 520000) |
                              (institution_df['Name'].str.contains('Lawrene Berk|Oak Ridge Nat|Argonne|Iowa State|Harvard University')) |
                              (institution_df['Name'].isin(selected_resorgs))]
    num_rows = inst_df2.shape[0]
    for i in range(num_rows):
        fig.add_annotation(x=np.log10(inst_df2['AllUS']).iloc[i],
                           y=np.log10(inst_df2["FF Pubs"]).iloc[i],
                           text=inst_df2["Name"].iloc[i],
                           # showarrow = True,
                           ax=-80,
                           ay=-12
                           )

        fig.add_annotation(x=4.905, y=4.579,
                           text="University of Michigan - Ann Arbor",
                           ax=-20,
                           ay=-20)
        fig.add_annotation(x=4.86, y=4.54,
                        text="University of Washington",
                        ax=-120,
                        ay=-10)
        fig.add_annotation(x=4.236, y=4.13,
                        text="Lawrence Berkeley Nat Lab",
                        ax=-120,
                        ay=-30)      

    fig.update_layout(yaxis_title='Number of U.S. Federally Funded publications 2017-2021 [log]',)


fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Research Institutions: Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title='Total number of publications worldwide 2017-2021 [log]',
    #yaxis_title='Number of U.S. Federally Funded publications 2017-2021',
    showlegend=False,
    font_size = 14
)

st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)






st.subheader('Percentage')

fig = px.scatter(institution_df, x='AllUS',y='Percentage', color='color',
                 #symbol='Name', 
                 hover_name='Name', 
                 hover_data={'color':False},
                 log_x=True,
                 #text='Name'
                )

fig.update_traces(textposition='top right')

fig.update_layout(
    height=700, width=1200,
    title_text='Research Institutions: Total vs. Percentage U.S. Federally Funded Publications, 2017-2021',
    xaxis_title = 'Number of Total publications 2017-2021 [log]',
    yaxis_title = "Percentage FF, 2017-2021",
    showlegend = False,
    font_size = 14
)

inst_df2 = institution_df[ (institution_df['AllUS'] > 80000) | 
                           (institution_df['Percentage']>99) | 
                           (institution_df['Name'].str.contains('Iowa State|Larence Berk|Ridge Natioal|Argone')) | 
                           institution_df['Name'].isin(selected_resorgs)]
num_rows = inst_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(inst_df2['AllUS']).iloc[i],
                       y=inst_df2["Percentage"].iloc[i],
                       text = inst_df2["Name"].iloc[i],
                       #showarrow = True,
                        ax = 55,
                        ay = -12
                      )

fig.add_shape(type="rect",
    x0=1300, y0=73.5, x1=19500, y1=90,
    line=dict(color="RoyalBlue"),
    #layer="below",
)

fig.add_annotation(x=4.3, y=87,
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
    legend_title_text='OA Type',
    font_size = 14
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
    legend_title_text='OA Type',
    font_size = 14
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
    legend_title_text='OA Type',
    font_size = 14
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
    legend_title_text='OA Type',
    font_size = 14
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
    legend_title_text='OA Type',
    font_size=14
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
    legend_title_text='OA Type',
    font_size=14
)

st.plotly_chart(fig, use_container_width=False)



##### Footer in sidebar #####
#st.subheader("About")
github = "[![GitHub repo stars](https://img.shields.io/github/stars/eschares/ostp_impact?logo=github&style=social)](<https://github.com/eschares/ostp_impact>)"
twitter = "[![Twitter Follow](https://img.shields.io/twitter/url?label=Twitter%20%40eschares&style=social&url=https%3A%2F%2Ftwitter.com%2Feschares)](<https://twitter.com/eschares>)"
zenodo = "[![DOI](https://zenodo.org/badge/554219142.svg)](https://zenodo.org/badge/latestdoi/554219142)"

mastodon = "[![Mastodon Follow](https://img.shields.io/mastodon/follow/108216956438964080?domain=https://scholar.social&style=social)](<https://scholar.social/@eschares>)"


html_string = "<p style=font-size:13px>v1.1, last modified 4/12/23 <br />Created by Eric Schares, Iowa State University <br /> <b>eschares@iastate.edu</b></p>"
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