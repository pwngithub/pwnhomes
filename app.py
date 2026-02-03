import streamlit as st
import pandas as pd
import io

# App configuration
st.set_page_config(page_title="Homes Service Dashboard", layout="wide")
st.title("🏠 Broadband Connectivity Dashboard")

# The data you provided
raw_data = """052,FTTB,153,100,(65.3%),149,100,(65.3%)
053,FTTH-Baileyville,701,213,(30.4%),332,214,(30.5%)
054,FTTH-Airport Dr,19,11,(57.9%),18,11,(57.9%)
055,FTTH-Amity,43,26,(60.5%),41,26,(60.5%)
056,FTTH-Calais,1570,470,(29.9%),749,470,(29.9%)
057,FTTH-Big Lake,76,41,(53.9%),73,41,(53.9%)
058,FTTH-Chapman Rd,56,43,(76.8%),51,43,(76.8%)
059,FTTH-Crescent Park,47,32,(68.1%),43,32,(68.1%)
060,FTTH-Hodgdon,208,142,(68.3%),191,143,(68.8%)
061,FTTH-Hltn/Hodgdon Rt 1,37,21,(56.8%),32,21,(56.8%)
062,FTTH-Deerfield,98,68,(69.4%),82,68,(69.4%)
063,FTTH-Houlton County Rd,125,85,(68.0%),120,85,(68.0%)
064,FTTH-Alexander,258,162,(62.8%),203,162,(62.8%)
065,FTTH-Houlton NEQUAD,778,376,(48.3%),683,376,(48.3%)
066,FTTH-Indian Township,371,229,(61.7%),263,229,(61.7%)
067,FTTH-Houlton North,53,30,(56.6%),47,30,(56.6%)
068,FTTH-Oxbow,34,30,(88.2%),34,30,(88.2%)
069,FTTH-Linneus Bangor Rd,24,20,(83.3%),20,20,(83.3%)
070,FTTH-Maple Grove,90,59,(65.5%),85,59,(65.5%)
071,FTTH-Loring Fiber,4,1,(25.0%),4,1,(25.0%)
072,FTTH-McSheffery,75,59,(78.7%),72,59,(78.7%)
074,FTTH-Orient,158,74,(46.8%),152,75,(47.5%)
075,FTTH-Parsons Rd,71,42,(59.1%),70,42,(59.1%)
076,FTTH-Park and Green,132,74,(56.1%),119,74,(56.1%)
077,FTTH-PI,1386,208,(15.0%),320,208,(15.0%)
078,FTTH-Sherman,202,142,(70.3%),195,142,(70.3%)
079,FTTH-Stacyville,56,33,(58.9%),52,33,(58.9%)
080,FTTH-Plunkett Pond,144,83,(57.6%),101,85,(59.0%)
081,FTTH-West Street,271,29,(10.7%),31,29,(10.7%)
082,FTTH-Triquad,1387,794,(57.2%),1215,794,(57.2%)
084,FTTH-WS,19,15,(78.9%),16,15,(78.9%)
085,FTTH-WS Hodgdon,4,4,(100.0%),4,4,(100.0%)
086,FTTH-Westfield Shorey Rd,40,30,(75.0%),37,30,(75.0%)
087,FTTH-Walker Rd,74,56,(75.7%),66,56,(75.7%)
088,FTTH-Westford Hill,40,25,(62.5%),40,25,(62.5%)
300,FTTH-RDOF,1069,173,(16.2%),232,173,(16.2%)
302,FTTH,4,2,(50.0%),3,2,(50.0%)
303,FTTH-Ashland,45,9,(20.0%),9,9,(20.0%)
304,FTTH-Cameron's,86,76,(88.4%),80,76,(88.4%)
305,FTTH-Corner Rd Bridgewater,3,1,(33.3%),2,1,(33.3%)
306,FTTH-Crawford,32,3,(9.4%),5,3,(9.4%)
307,FTTH-Drew's Lake,82,73,(89.0%),81,73,(89.0%)
308,FTTH-Eagle Lake,1,1,(100.0%),1,1,(100.0%)
309,FTTH-E Plantation,5,5,(100.0%),5,5,(100.0%)
310,FTTH-Linneus 4 Corners,84,73,(86.9%),80,73,(86.9%)
312,FTTH-Masardis,29,21,(72.4%),22,21,(72.4%)
313,FTTH-McBurnie Rd PI,7,6,(85.7%),6,6,(85.7%)
314,FTTH-Monticello,7,3,(42.9%),6,3,(42.9%)
316,FTTH-Cooper,142,64,(45.1%),69,64,(45.1%)
318,FTTH-BEAD,2,0,(0.0%),0,0,(0.0%)
319,FTTH-Blaine-Robinson,4,4,(100.0%),4,4,(100.0%)
322,FTTH-Princeton,36,23,(63.9%),33,23,(63.9%)
323,FTTH-Cogan Rd,11,10,(90.9%),10,10,(90.9%)"""

# Load Data
df = pd.read_csv(io.StringIO(raw_data), names=["ID", "Name", "Total Homes", "Active Homes", "Perc1", "Col6", "Col7", "Perc2"])

# Clean numerical columns
df["Total Homes"] = pd.to_numeric(df["Total Homes"])
df["Active Homes"] = pd.to_numeric(df["Active Homes"])

# Calculate KPIs
df["Active Percentage"] = (df["Active Homes"] / df["Total Homes"] * 100).round(2)

# Global Totals
total_homes_passed = df["Total Homes"].sum()
total_active_homes = df["Active Homes"].sum()
overall_percentage = (total_active_homes / total_homes_passed * 100) if total_homes_passed > 0 else 0

# UI - Header KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Homes Passed", f"{total_homes_passed:,}")
col2.metric("Total Active Homes", f"{total_active_homes:,}")
col3.metric("Overall Penetration (%)", f"{overall_percentage:.2f}%")

st.divider()

# Display Data Table
st.subheader("Line-by-Line Service Detail")
st.dataframe(
    df[["Name", "Total Homes", "Active Homes", "Active Percentage"]],
    column_config={
        "Active Percentage": st.column_config.ProgressColumn(
            "Activation Rate",
            help="Percentage of homes active vs passed",
            format="%f%%",
            min_value=0,
            max_value=100,
        ),
    },
    use_container_width=True,
    hide_index=True
)
