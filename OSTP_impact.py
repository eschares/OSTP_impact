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


st.markdown('# Impact of the 2022 OSTP Memo')
#sst.header('A Bibliometric Analysis of U.S. Federally Funded Publications, 2017-2021')

#st.markdown("""---""")
st.header('As of November 4, 2022, this site has moved to dedicated web hosting at https://ostp.lib.iastate.edu/')

st.header('')

##### Footer in sidebar #####


html_string = "<p style=font-size:13px>Eric Schares, Iowa State University <br /> <b>eschares@iastate.edu</b></p>"
st.markdown(html_string, unsafe_allow_html=True)


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