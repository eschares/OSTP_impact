## OSTP impact, v2

Eric Schares, August 29, 2023

eschares@iastate.edu

---

This is a revised and expanded version of data that supports the research study at https://doi.org/10.1162/qss_a_00237.

Data were collected August 28 - September 1, 2023 from the paid version of Digital Science’s Dimensions platform, available at https://app.dimensions.ai. Both the web interface and the API were used.

Basic search query was:
- Year: 2016-2022
- Publication Type: NOT preprint
- Funder group: US Federal Funders
- Custom filter applied to remove "front matter": editorials, cover photo, cover picture, titelbild, etc.

Note: a known issue is the inclusion of "Supplementary" material. This was not separated out due to technical issues. The inclusion of this material adds 0.3% to the total US Federally Funded (FF) publication counts from 2016-2022.

Website at https://ostp-v2.streamlit.app/

### Updates:

#### 9/1/23:
Research Organizations:
  - Top 10 journal titles where different groups (R1, R2, etc.) publish. 2016-2022 combined.
  - How much concentration is there in each group's top 10 titles, or what percentage of a group's overall output is in just the top 10 journals? NASNTI most concentrated, 11% of output in 10 journals. HSI, HBCU, AANAPISI all over 8%. R1 and R2 around 7%.
  - Look for any differences in where each group publishes, but hard to quantify. Brought in Journal Impact Factor (JIF) as a way to describe each journal, but don't feel good about it. JIF has many well-known problems and biases. Summary number for a journal is `% of each group's output in that journal * journal's JIF`. If a group publishes a lot in a title, should get more of that journal's JIF in the summary number.



#### 8/31/23:

Research Organizations file, `ResOrgs_v2.xlsx`.
  - Main sheet is `summary_pastevalues`. Flat file that contains information on 1150 research organizations, including R1s, R2s, HBCUs, HSIs, NASNTIs, AANAPISIs as defined in Dimensions.
  - ResOrg group definitions (R1, R2, HBCUs, HSIs, NASNTIs, AANAPISIs) from Dimensions shown in sheet `ResOrg-group_definitions`
  - File started with an export of top 500 orgs by number of FF pubs, 2016-2022.
  - In some cases, a ResOrg belonging to a group was in the initial pull of top 500. That org was not looked up using the API. Other (smaller) orgs were specifically searched for in the API and added to the bottom of the sheet.
  - Did not break it out into individual files for a single year. Could do that if there's interest, will take quite a bit of time to run.
  - Added new set of files {group}_publish_here, showing top journals that different ResOrg groups publish FF research in, 2016-2022
  - Scatter plot US FF vs. % FF Gold. Not quite what I wanted to see, hard to summarize how ResOrgs differ in their behavior.

By Discipline, years 2016-2022 combined
  - OA colors by discipline, for both sub- (4-digit) and top-level (2-digit) codes. Stacked bar charts sorted by highest % Closed. Education has highest % FF Closed
  - Interactive versions of stacked bar graphs on v2 website
  - Looked deeper into biggest FF code **32 - Biological Sciences**. Biggest sub-code is **3202 - Clinical Sciences**, provided OA breakdown and top journals within it.

#### 8/30/23:

By OA Color
  - Stacked bar charts show OA mode by research org groups and comparison funder groups

By journal, 2016-2022 combined and single years

By publisher, 2016-222 combined and single years


## Overall Numbers:
- The sum of US FF papers over the years 2016-2022 is **1,950,355**, and the average number of US FF papers per year is **278,622**.
- The number of US FF papers increased each year from 2016-2021, but decreased in 2022. This matches the trend seen from all US publications and output from two European funding groups. The number of worldwide publications continued to increase in 2022.
- The US FF rate of change ranged from a 5.4% increase (2019-2020) to an 8% decrease (2021 to 2022). The average rate of increase over all six years studied here was 0.5%. Excluding the 2022 decrease, the average rate of increase was 2.3% YoY.
- The so-called "Covid spike" of publications in 2020 is seen as increases in all groups here, ranging from 11.3-5.4%.

- US FF publications make up around 36% of all US output, ranging from 35.6% to 37.4% in an individual year.
- All US output makes up around 13.5% of all worldwide output over 2016-2022, ranging from 11.8-15.8% in an individual year.
- Therefore, US FF publications make up nearly 5% of all worldwide output over the 7 years studied here, ranging from 4.2-5.9% in an individual year.
