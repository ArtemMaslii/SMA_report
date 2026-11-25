"""build_dataset.py — builds the node and edge tables for the project
"Does Development Cross Borders? A network analysis of human development across the land borders of Europe and Asia".

Node attributes (2023 values): UNDP Human Development Report 2025, Statistical Annex, Table 1
  https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Statistical_Annex_HDI_Table.pdf
  hdi, life_expectancy (years), expected_schooling (years), mean_schooling (years), gni_pc_ppp (2021 PPP $)
Subregions: UN M49 geoscheme. Edges: shared land border, or one of four permanent fixed links.
plot_lat / plot_lon are approximate drawing positions only (not used in any computation).
Output: nodes_eurasia_hdi.csv, edges_eurasia_borders.csv
"""
import pandas as pd
# name, iso3, subregion, landlocked, EU, exUSSR, plot_lat, plot_lon, HDI, LE, EYS, MYS, GNI
rows = [
("Albania","ALB","Southern Europe",0,0,0,41.33,19.82,0.810,79.6,14.5,10.2,17627),
("Austria","AUT","Western Europe",1,1,0,48.21,16.37,0.930,82.0,16.3,12.4,63479),
("Belarus","BLR","Eastern Europe",1,0,1,53.90,27.57,0.824,74.4,13.7,12.3,26725),
("Belgium","BEL","Western Europe",0,1,0,50.85,4.35,0.951,82.1,19.0,12.7,63582),
("Bosnia and Herzegovina","BIH","Southern Europe",0,0,0,43.86,18.41,0.804,77.9,13.2,11.0,19827),
("Bulgaria","BGR","Eastern Europe",0,1,0,42.70,23.32,0.845,75.6,15.3,11.5,32175),
("Croatia","HRV","Southern Europe",0,1,0,45.81,15.98,0.889,78.6,16.3,12.1,41380),
("Czechia","CZE","Eastern Europe",1,1,0,50.08,14.44,0.915,79.8,16.8,13.0,45889),
("Denmark","DNK","Northern Europe",0,1,0,55.68,12.57,0.962,81.9,18.7,13.0,76008),
("Estonia","EST","Northern Europe",0,1,1,59.44,24.75,0.905,79.2,16.0,13.6,40881),
("Finland","FIN","Northern Europe",0,1,0,60.17,24.94,0.948,81.9,19.5,13.0,57068),
("France","FRA","Western Europe",0,1,0,48.86,2.35,0.920,83.3,16.1,11.8,55060),
("Germany","DEU","Western Europe",0,1,0,52.52,13.40,0.959,81.4,17.3,14.3,64053),
("Greece","GRC","Southern Europe",0,1,0,37.98,23.73,0.908,81.9,20.8,11.6,35761),
("Hungary","HUN","Eastern Europe",1,1,0,47.50,19.04,0.870,77.0,15.5,12.3,37236),
("Ireland","IRL","Northern Europe",0,1,0,53.35,-6.26,0.949,82.4,19.2,11.7,90885),
("Italy","ITA","Southern Europe",0,1,0,41.90,12.50,0.915,83.7,16.7,10.8,52389),
("Latvia","LVA","Northern Europe",0,1,1,56.95,24.11,0.889,76.2,16.5,13.4,37998),
("Lithuania","LTU","Northern Europe",0,1,1,54.69,25.28,0.895,76.0,16.5,13.6,41916),
("Luxembourg","LUX","Western Europe",1,1,0,49.61,6.13,0.922,82.2,14.4,12.6,85461),
("Moldova","MDA","Eastern Europe",1,0,1,47.01,28.86,0.785,71.2,14.6,11.8,15867),
("Montenegro","MNE","Southern Europe",0,0,0,42.44,19.26,0.862,77.1,15.5,12.8,28026),
("Netherlands","NLD","Western Europe",0,1,0,52.37,4.90,0.955,82.2,18.6,12.7,68344),
("North Macedonia","MKD","Southern Europe",1,0,0,42.00,21.43,0.815,77.4,14.8,10.2,22128),
("Norway","NOR","Northern Europe",0,0,0,59.91,10.75,0.970,83.3,18.8,13.1,112710),
("Poland","POL","Eastern Europe",0,1,0,52.23,21.01,0.906,78.6,16.7,13.2,42218),
("Portugal","PRT","Southern Europe",0,1,0,38.72,-9.14,0.890,82.4,17.5,9.7,41064),
("Romania","ROU","Eastern Europe",0,1,0,44.43,26.10,0.845,75.9,14.1,11.6,39374),
("Russia","RUS","Eastern Europe",0,0,1,55.76,37.62,0.832,73.2,13.2,12.4,39222),
("Serbia","SRB","Southern Europe",1,0,0,44.79,20.45,0.833,76.8,15.0,11.6,23115),
("Slovakia","SVK","Eastern Europe",1,1,0,48.15,17.11,0.880,78.3,14.9,13.1,36793),
("Slovenia","SVN","Southern Europe",0,1,0,46.06,14.51,0.931,81.6,17.5,13.0,46361),
("Spain","ESP","Southern Europe",0,1,0,40.42,-3.70,0.918,83.7,17.8,10.8,46008),
("Sweden","SWE","Northern Europe",0,1,0,59.33,18.07,0.959,83.3,19.0,12.7,66102),
("Switzerland","CHE","Western Europe",1,0,0,46.95,7.45,0.970,84.0,16.7,13.9,81949),
("Ukraine","UKR","Eastern Europe",0,0,1,50.45,30.52,0.779,73.4,13.3,11.1,16933),
("United Kingdom","GBR","Northern Europe",0,0,0,51.51,-0.13,0.946,81.3,17.8,13.5,54372),
("Türkiye","TUR","Western Asia",0,0,0,39.93,32.86,0.853,77.2,19.8,9.0,34507),
("Georgia","GEO","Western Asia",0,0,1,41.72,44.79,0.844,74.5,16.8,12.7,20753),
("Armenia","ARM","Western Asia",1,0,1,40.18,44.51,0.811,75.7,14.4,11.3,20221),
("Azerbaijan","AZE","Western Asia",1,0,1,40.41,49.87,0.789,74.4,12.9,11.1,20668),
("Iran","IRN","Southern Asia",0,0,0,35.69,51.39,0.799,77.7,14.0,10.8,16096),
("Iraq","IRQ","Western Asia",0,0,0,33.31,44.36,0.695,72.3,12.4,6.8,12654),
("Syria","SYR","Western Asia",0,0,0,33.51,36.28,0.564,72.1,7.4,5.9,3918),
("Lebanon","LBN","Western Asia",0,0,0,33.89,35.50,0.752,77.8,11.7,10.4,11299),
("Israel","ISR","Western Asia",0,0,0,32.08,34.78,0.919,82.4,14.9,13.5,48050),
("Palestine","PSE","Western Asia",0,0,0,31.90,35.20,0.674,65.2,13.0,10.1,6547),
("Jordan","JOR","Western Asia",0,0,0,31.95,35.93,0.754,77.8,13.1,10.2,9222),
("Saudi Arabia","SAU","Western Asia",0,0,0,24.71,46.68,0.900,78.7,16.9,11.6,50299),
("Kuwait","KWT","Western Asia",0,0,0,29.38,47.99,0.852,80.4,15.9,7.6,56612),
("Qatar","QAT","Western Asia",0,0,0,25.29,51.53,0.886,82.4,13.1,10.8,105353),
("United Arab Emirates","ARE","Western Asia",0,0,0,24.45,54.38,0.940,82.9,15.6,13.0,71142),
("Oman","OMN","Western Asia",0,0,0,23.59,58.41,0.858,80.0,13.4,11.9,36096),
("Yemen","YEM","Western Asia",0,0,0,15.37,44.19,0.470,69.3,7.5,5.5,1018),
("Bahrain","BHR","Western Asia",0,0,0,26.23,50.59,0.899,81.3,15.9,11.1,52819),
("Kazakhstan","KAZ","Central Asia",1,0,1,51.17,71.45,0.837,74.4,14.0,12.5,30989),
("Uzbekistan","UZB","Central Asia",1,0,1,41.30,69.24,0.740,72.4,12.5,11.9,8826),
("Turkmenistan","TKM","Central Asia",1,0,1,37.96,58.33,0.764,70.1,13.2,11.2,17716),
("Kyrgyzstan","KGZ","Central Asia",1,0,1,42.87,74.59,0.720,71.7,12.7,12.1,6078),
("Tajikistan","TJK","Central Asia",1,0,1,38.56,68.79,0.691,71.8,10.8,11.3,5747),
("Afghanistan","AFG","Southern Asia",1,0,0,34.53,69.17,0.496,66.0,10.8,2.5,1972),
("Pakistan","PAK","Southern Asia",0,0,0,33.68,73.05,0.544,67.6,7.9,4.3,5501),
("India","IND","Southern Asia",0,0,0,28.61,77.21,0.685,72.0,13.0,6.9,9047),
("Nepal","NPL","Southern Asia",1,0,0,27.72,85.32,0.622,70.4,13.8,4.5,4726),
("Bhutan","BTN","Southern Asia",1,0,0,27.47,89.64,0.698,73.0,13.2,5.8,13843),
("Bangladesh","BGD","Southern Asia",0,0,0,23.81,90.41,0.685,74.7,12.3,6.8,8498),
("China","CHN","Eastern Asia",0,0,0,39.90,116.40,0.797,78.0,15.5,8.0,22029),
("Mongolia","MNG","Eastern Asia",1,0,0,47.89,106.91,0.747,71.7,13.6,9.4,14787),
("Myanmar","MMR","South-eastern Asia",0,0,0,19.76,96.08,0.609,66.9,11.5,6.4,4919),
("Thailand","THA","South-eastern Asia",0,0,0,13.76,100.50,0.798,76.4,15.4,9.0,20570),
("Laos","LAO","South-eastern Asia",1,0,0,17.98,102.63,0.617,69.0,9.6,6.1,8106),
("Cambodia","KHM","South-eastern Asia",0,0,0,11.56,104.92,0.606,70.7,11.2,5.2,4931),
("Viet Nam","VNM","South-eastern Asia",0,0,0,21.03,105.85,0.766,74.6,15.5,9.0,13033),
("Malaysia","MYS","South-eastern Asia",0,0,0,3.14,101.69,0.819,76.7,12.7,11.1,32553),
("Singapore","SGP","South-eastern Asia",0,0,0,1.35,103.82,0.946,83.7,16.7,12.0,111239),
("Brunei","BRN","South-eastern Asia",0,0,0,4.90,114.94,0.837,75.3,13.7,9.3,75827),
("Indonesia","IDN","South-eastern Asia",0,0,0,-6.21,106.85,0.728,71.1,13.3,8.7,13700),
("Timor-Leste","TLS","South-eastern Asia",0,0,0,-8.56,125.57,0.634,67.7,13.3,6.2,5435),
]
cols=["country","iso3","subregion","landlocked","eu_member","former_ussr","plot_lat","plot_lon",
      "hdi","life_expectancy","expected_schooling","mean_schooling","gni_pc_ppp"]
nodes=pd.DataFrame(rows,columns=cols)
# Plot-only positions: capitals by default; geographic centres where capitals overlap or sit at a country's edge.
OVR={"AUT":(47.6,14.6),"SVK":(48.7,19.6),"HRV":(45.3,16.3),"BIH":(44.2,17.8),"SRB":(44.0,20.9),
     "MNE":(42.7,19.3),"MKD":(41.6,21.7),"ALB":(41.0,20.0),"SVN":(46.1,14.6),"CZE":(49.8,15.3),
     "DEU":(51.1,10.4),"NLD":(52.3,5.6),"LUX":(49.6,6.1),"LBN":(33.9,35.8),"SYR":(35.0,38.4),
     "ISR":(31.0,34.8),"PSE":(31.95,35.3),"JOR":(30.9,36.8),"KWT":(29.3,47.6),"BHR":(26.0,50.55),
     "QAT":(25.3,51.2),"ARE":(23.9,54.3),"SAU":(24.0,45.0),"OMN":(21.0,57.0),"TUR":(39.0,35.0),
     "IRN":(32.5,54.0),"KAZ":(48.0,67.0),"CHN":(35.0,103.0),"MNG":(47.0,103.0),"IND":(22.0,79.0),
     "IDN":(-2.5,113.0),"MYS":(4.0,102.0),"SGP":(1.3,103.8)}
for k,(la,lo) in OVR.items():
    nodes.loc[nodes.iso3==k,["plot_lat","plot_lon"]]=[la,lo]
nodes.insert(3,"continent",nodes.subregion.str.contains("Europe").map({True:"Europe",False:"Asia"}))
def grp(h):
    return "Very high" if h>=0.8 else "High" if h>=0.7 else "Medium" if h>=0.55 else "Low"
nodes["hdi_group"]=nodes.hdi.map(grp)

B = {
"ALB":"MNE MKD GRC","AUT":"DEU CZE SVK HUN SVN ITA CHE","BLR":"RUS UKR POL LTU LVA",
"BEL":"FRA LUX DEU NLD","BIH":"HRV SRB MNE","BGR":"ROU SRB MKD GRC TUR",
"HRV":"SVN HUN SRB BIH MNE","CZE":"DEU POL SVK AUT","DNK":"DEU","EST":"LVA RUS",
"FIN":"SWE NOR RUS","FRA":"BEL LUX DEU CHE ITA ESP","DEU":"DNK POL CZE AUT CHE FRA LUX BEL NLD",
"GRC":"ALB MKD BGR TUR","HUN":"AUT SVK UKR ROU SRB HRV SVN","IRL":"GBR","ITA":"FRA CHE AUT SVN",
"LVA":"EST LTU BLR RUS","LTU":"LVA BLR POL RUS","LUX":"BEL FRA DEU","MDA":"ROU UKR",
"MNE":"HRV BIH SRB ALB","NLD":"BEL DEU","MKD":"SRB BGR GRC ALB","NOR":"SWE FIN RUS",
"POL":"DEU CZE SVK UKR BLR LTU RUS","PRT":"ESP","ROU":"HUN UKR MDA BGR SRB",
"RUS":"NOR FIN EST LVA LTU POL BLR UKR GEO AZE KAZ CHN MNG","SRB":"HUN ROU BGR MKD MNE BIH HRV",
"SVK":"CZE POL UKR HUN AUT","SVN":"ITA AUT HUN HRV","ESP":"PRT FRA","SWE":"NOR FIN",
"CHE":"FRA DEU AUT ITA","UKR":"RUS BLR POL SVK HUN ROU MDA","GBR":"IRL",
"TUR":"GRC BGR GEO ARM AZE IRN IRQ SYR","GEO":"RUS TUR ARM AZE","ARM":"GEO AZE IRN TUR",
"AZE":"RUS GEO ARM IRN TUR","IRN":"TUR ARM AZE TKM AFG PAK IRQ","IRQ":"TUR IRN KWT SAU JOR SYR",
"SYR":"TUR IRQ JOR ISR LBN","LBN":"SYR ISR","ISR":"LBN SYR JOR PSE","PSE":"ISR JOR",
"JOR":"SYR IRQ SAU ISR PSE","SAU":"JOR IRQ KWT QAT ARE OMN YEM","KWT":"IRQ SAU","QAT":"SAU",
"ARE":"SAU OMN","OMN":"ARE SAU YEM","YEM":"SAU OMN","BHR":"",
"KAZ":"RUS CHN KGZ UZB TKM","UZB":"KAZ KGZ TJK AFG TKM","TKM":"KAZ UZB AFG IRN",
"KGZ":"KAZ UZB TJK CHN","TJK":"KGZ UZB AFG CHN","AFG":"IRN TKM UZB TJK CHN PAK",
"PAK":"IRN AFG CHN IND","IND":"PAK CHN NPL BTN BGD MMR","NPL":"IND CHN","BTN":"IND CHN",
"BGD":"IND MMR","CHN":"RUS MNG KAZ KGZ TJK AFG PAK IND NPL BTN MMR LAO VNM","MNG":"RUS CHN",
"MMR":"BGD IND CHN LAO THA","THA":"MMR LAO KHM MYS","LAO":"CHN MMR THA KHM VNM",
"KHM":"THA LAO VNM","VNM":"CHN LAO KHM","MYS":"THA IDN BRN","SGP":"","BRN":"MYS","IDN":"MYS TLS","TLS":"IDN",
}
FIXED = [("GBR","FRA","Channel Tunnel"),("DNK","SWE","Øresund Bridge"),
         ("BHR","SAU","King Fahd Causeway"),("SGP","MYS","Johor–Singapore Causeway")]
# symmetry check
iso=set(nodes.iso3)
for a,s in B.items():
    for b in s.split():
        assert b in iso,(a,b)
        assert a in B[b].split(),("asym",a,b)
edges=set()
for a,s in B.items():
    for b in s.split():
        edges.add(tuple(sorted((a,b))))
E=[(a,b,"land border","") for a,b in sorted(edges)]
E+= [(*sorted((a,b)),"fixed link",n) for a,b,n in FIXED]
name=dict(zip(nodes.iso3,nodes.country))
edf=pd.DataFrame(E,columns=["source","target","edge_type","note"])
edf.insert(2,"source_name",edf.source.map(name)); edf.insert(3,"target_name",edf.target.map(name))
nodes.to_csv("nodes_eurasia_hdi.csv",index=False); edf.to_csv("edges_eurasia_borders.csv",index=False)
print(len(nodes),"nodes",len(edf),"edges"); print(nodes.subregion.value_counts())
