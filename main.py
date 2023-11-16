import pandas as pd
import glob
import os

# finds most recent file in specified folder
list_of_files = glob.glob(os.path.join('C:/Users/Kevin/Desktop/FM_Data/input/', '*'))
latest_file = max(list_of_files, key=os.path.getctime)

# Read HTML file exported by FM - in this case an example of an output from the squad page
# This reads as a list, not a dataframe
squad_rawdata_list = pd.read_html(latest_file, header=0, encoding="utf-8", keep_default_na=False)
# turn the list into a dataframe
squad_rawdata = squad_rawdata_list[0]

# Calculate simple speed and workrate scores
squad_rawdata['Spd'] = ( squad_rawdata['Pac'] + squad_rawdata['Acc'] ) / 2
squad_rawdata['Work'] = ( squad_rawdata['Wor'] + squad_rawdata['Sta'] ) / 2
squad_rawdata['SetP'] = ( squad_rawdata['Jum'] + squad_rawdata['Bra'] ) / 2

# calculates Sweeper_keeper_Defend score
squad_rawdata['skd_key'] = ( squad_rawdata['Agi'] + squad_rawdata['Ref'] )
squad_rawdata['skd_green'] = ( squad_rawdata['Cmd'] + squad_rawdata['Kic'] + squad_rawdata['1v1'] + squad_rawdata['Ant'] + squad_rawdata['Cnt'] + squad_rawdata['Pos'] )
squad_rawdata['skd_blue'] = ( squad_rawdata['Aer'] + squad_rawdata['Fir'] + squad_rawdata['Han'] + squad_rawdata['Pas'] + squad_rawdata['TRO'] + squad_rawdata['Dec'] + squad_rawdata['Vis'] + squad_rawdata['Acc'] )
squad_rawdata['skd'] =( ( ( squad_rawdata['skd_key'] * 5) + (squad_rawdata['skd_green'] * 3) + (squad_rawdata['skd_blue'] * 1) ) / 36)
squad_rawdata.skd= squad_rawdata.skd.round(1)

# calculates Wing_back_Support score
squad_rawdata['wbs_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Sta'] + squad_rawdata['Wor'] )
squad_rawdata['wbs_green'] = ( squad_rawdata['Cro'] + squad_rawdata['Dri'] + squad_rawdata['Mar'] + squad_rawdata['Tck'] + squad_rawdata['OtB'] + squad_rawdata['Tea'] )
squad_rawdata['wbs_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Pas'] + squad_rawdata['Tec'] + squad_rawdata['Ant'] + squad_rawdata['Cnt'] + squad_rawdata['Dec'] + squad_rawdata['Pos'] + squad_rawdata['Agi'] + squad_rawdata['Bal'] )
squad_rawdata['wbs'] =( ( ( squad_rawdata['wbs_key'] * 5) + (squad_rawdata['wbs_green'] * 3) + (squad_rawdata['wbs_blue'] * 1) ) / 47)
squad_rawdata.wbs= squad_rawdata.wbs.round(1)

# calculates Ball_playing_defender_Defend score
squad_rawdata['bpdd_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Jum'] + squad_rawdata['Cmp'] )
squad_rawdata['bpdd_green'] = ( squad_rawdata['Hea'] + squad_rawdata['Mar'] + squad_rawdata['Pas'] + squad_rawdata['Tck'] + squad_rawdata['Pos'] + squad_rawdata['Str'] )
squad_rawdata['bpdd_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Tec'] + squad_rawdata['Agg'] + squad_rawdata['Ant'] + squad_rawdata['Bra'] + squad_rawdata['Cnt'] + squad_rawdata['Dec'] + squad_rawdata['Vis'] )
squad_rawdata['bpdd'] =( ( ( squad_rawdata['bpdd_key'] * 5) + (squad_rawdata['bpdd_green'] * 3) + (squad_rawdata['bpdd_blue'] * 1) ) / 46)
squad_rawdata.bpdd= squad_rawdata.bpdd.round(1)

# calculates Segundo_volante_Attack score
squad_rawdata['sva_key'] = ( squad_rawdata['Wor'] + squad_rawdata['Sta'] + squad_rawdata['Acc'] + squad_rawdata['Pac'] )
squad_rawdata['sva_green'] = ( squad_rawdata['Fin'] + squad_rawdata['Lon'] + squad_rawdata['Pas'] + squad_rawdata['Tck'] + squad_rawdata['Ant'] + squad_rawdata['OtB'] + squad_rawdata['Pos'] )
squad_rawdata['sva_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Mar'] + squad_rawdata['Cmp'] + squad_rawdata['Cnt'] + squad_rawdata['Dec'] + squad_rawdata['Bal'] )
squad_rawdata['sva'] =( ( ( squad_rawdata['sva_key'] * 5) + (squad_rawdata['sva_green'] * 3) + (squad_rawdata['sva_blue'] * 1) ) / 47)
squad_rawdata.sva= squad_rawdata.sva.round(1)

# calculates Advanced_forward_Attack score
squad_rawdata['afa_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Fin'] )
squad_rawdata['afa_green'] = ( squad_rawdata['Dri'] + squad_rawdata['Fir'] + squad_rawdata['Tec'] + squad_rawdata['Cmp'] + squad_rawdata['OtB'] )
squad_rawdata['afa_blue'] = ( squad_rawdata['Pas'] + squad_rawdata['Ant'] + squad_rawdata['Dec'] + squad_rawdata['Wor'] + squad_rawdata['Agi'] + squad_rawdata['Bal'] + squad_rawdata['Sta'] )
squad_rawdata['afa'] =( ( ( squad_rawdata['afa_key'] * 5) + (squad_rawdata['afa_green'] * 3) + (squad_rawdata['afa_blue'] * 1) ) / 37)
squad_rawdata.afa= squad_rawdata.afa.round(1)

squad_rawdata

# builds squad dataframe using only columns that will be exported to HTML
squad = squad_rawdata[['Name','Age','Club','Transfer Value','Wage','Nat','Position','Personality','Media Handling','Left Foot', 'Right Foot','Spd','Jum','Str','Work','Height','skd','bpdd','wbs','sva','afa']]

# taken from here: https://www.thepythoncode.com/article/convert-pandas-dataframe-to-html-table-python
# creates a function to make a sortable html export

def generate_html(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
    table_html = dataframe.to_html(table_id="table", index=False)
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <h1>Darren's Player Analyzer That He Made Himself And Did Not Copy :)</h1>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                paging: false,
                order: [[12, 'desc']],
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html

# generates random file name for write-out of html file
import uuid
file_name = str(uuid.uuid4()) + ".html"
print(file_name)
folder_name = "C:/Users/Kevin/Desktop/FM_Data/output/"
file_path = f"{folder_name}/{file_name}"
print(file_path)


# creates a sortable html export from the dataframe 'squad'

html = generate_html(squad)
open(file_path, "w", encoding="utf-8").write(html)

