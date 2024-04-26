from opentrons import protocol_api
from io import StringIO
import pandas as pd

# note: run source .venv/bin/activate in /home/shane/Documents/projects/method_dev/opentrons for
# development

metadata = {
    "protocolName": "Make pair mixes",
    "description": """This protocol mixes 8 HAMBI species/evo histories into all possible pairs with
                   each species either at 0.95 or 0.05 fraction""",
    "author": "Shane Hogle"
}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

# Functions ####################################################################

# Data #########################################################################

# this is annoying but you need to hard code the well/plate layout as a csv string. See here:
# https://support.opentrons.com/s/article/Using-CSV-input-data-in-Python-protocols

pairs_csv_raw = '''
Mixture_name,sp_A,sp_B,f_A,f_B,well
B49,blank,blank,0,0,A1
P17,ANC_0403,ANC_1977,0.05,0.95,A2
B50,blank,blank,0,0,A3
P13,ANC_1287,EVO_1896,0.05,0.95,A4
B51,blank,blank,0,0,A5
P47,EVO_0403,EVO_1287,0.05,0.95,A6
B52,blank,blank,0,0,A7
P36,EVO_1896,ANC_1977,0.95,0.05,A8
B53,blank,blank,0,0,A9
P16,EVO_1287,EVO_1896,0.95,0.05,A10
B54,blank,blank,0,0,A11
P28,EVO_1287,ANC_1977,0.95,0.05,A12
P26,ANC_1287,ANC_1977,0.95,0.05,B1
B55,blank,blank,0,0,B2
P38,ANC_1896,EVO_1977,0.95,0.05,B3
B56,blank,blank,0,0,B4
P32,EVO_1287,EVO_1977,0.95,0.05,B5
B57,blank,blank,0,0,B6
P03,EVO_0403,ANC_1896,0.05,0.95,B7
B58,blank,blank,0,0,B8
P02,ANC_0403,ANC_1896,0.95,0.05,B9
B59,blank,blank,0,0,B10
P39,EVO_1896,EVO_1977,0.05,0.95,B11
B60,blank,blank,0,0,B12
B61,blank,blank,0,0,C1
P44,EVO_0403,ANC_1287,0.95,0.05,C2
B62,blank,blank,0,0,C3
P11,EVO_1287,ANC_1896,0.05,0.95,C4
B63,blank,blank,0,0,C5
P34,ANC_1896,ANC_1977,0.95,0.05,C6
B64,blank,blank,0,0,C7
P45,ANC_0403,EVO_1287,0.05,0.95,C8
B65,blank,blank,0,0,C9
P27,EVO_1287,ANC_1977,0.05,0.95,C10
B66,blank,blank,0,0,C11
P05,ANC_0403,EVO_1896,0.05,0.95,C12
P25,ANC_1287,ANC_1977,0.05,0.95,D1
B67,blank,blank,0,0,D2
P10,ANC_1287,ANC_1896,0.95,0.05,D3
B68,blank,blank,0,0,D4
P46,ANC_0403,EVO_1287,0.95,0.05,D5
B69,blank,blank,0,0,D6
P09,ANC_1287,ANC_1896,0.05,0.95,D7
B70,blank,blank,0,0,D8
P14,ANC_1287,EVO_1896,0.95,0.05,D9
B71,blank,blank,0,0,D10
P48,EVO_0403,EVO_1287,0.95,0.05,D11
B72,blank,blank,0,0,D12
B73,blank,blank,0,0,E1
P12,EVO_1287,ANC_1896,0.95,0.05,E2
B74,blank,blank,0,0,E3
P21,ANC_0403,EVO_1977,0.05,0.95,E4
B75,blank,blank,0,0,E5
P41,ANC_0403,ANC_1287,0.05,0.95,E6
B76,blank,blank,0,0,E7
P35,EVO_1896,ANC_1977,0.05,0.95,E8
B77,blank,blank,0,0,E9
P18,ANC_0403,ANC_1977,0.95,0.05,E10
B78,blank,blank,0,0,E11
P08,EVO_0403,EVO_1896,0.95,0.05,E12
P24,EVO_0403,EVO_1977,0.95,0.05,F1
B79,blank,blank,0,0,F2
P04,EVO_0403,ANC_1896,0.95,0.05,F3
B80,blank,blank,0,0,F4
P30,ANC_1287,EVO_1977,0.95,0.05,F5
B81,blank,blank,0,0,F6
P40,EVO_1896,EVO_1977,0.95,0.05,F7
B82,blank,blank,0,0,F8
P33,ANC_1896,ANC_1977,0.05,0.95,F9
B83,blank,blank,0,0,F10
P20,EVO_0403,ANC_1977,0.95,0.05,F11
B84,blank,blank,0,0,F12
B85,blank,blank,0,0,G1
P31,EVO_1287,EVO_1977,0.05,0.95,G2
B86,blank,blank,0,0,G3
P43,EVO_0403,ANC_1287,0.05,0.95,G4
B87,blank,blank,0,0,G5
P23,EVO_0403,EVO_1977,0.05,0.95,G6
B88,blank,blank,0,0,G7
P37,ANC_1896,EVO_1977,0.05,0.95,G8
B89,blank,blank,0,0,G9
P19,EVO_0403,ANC_1977,0.05,0.95,G10
B90,blank,blank,0,0,G11
P15,EVO_1287,EVO_1896,0.05,0.95,G12
P22,ANC_0403,EVO_1977,0.95,0.05,H1
B91,blank,blank,0,0,H2
P42,ANC_0403,ANC_1287,0.95,0.05,H3
B92,blank,blank,0,0,H4
P07,EVO_0403,EVO_1896,0.05,0.95,H5
B93,blank,blank,0,0,H6
P29,ANC_1287,EVO_1977,0.05,0.95,H7
B94,blank,blank,0,0,H8
P01,ANC_0403,ANC_1896,0.05,0.95,H9
B95,blank,blank,0,0,H10
P06,ANC_0403,EVO_1896,0.95,0.05,H11
B96,blank,blank,0,0,H12
'''

pairs_csv = pd.read_csv(StringIO(pairs_csv_raw))
pairs_dict = pairs_csv.set_index('well').to_dict(orient='index')

# the order of the bacteria in the reservoir is very important! Here I have then in numerical
# order with the ancestral species first.
# A1 = ANC_0403, A2 = ANC_1287, A3 = ANC_1896, A4 = ANC_1977
# A5 = EVO_0403, A6 = EVO_1287, A7 = EVO_1896, A8 = EVO_1977
# It is also important that blank media is in A9

strain_dict = {'ANC_0403': 'A1', 'ANC_1287': 'A2', 'ANC_1896': 'A3', 'ANC_1977': 'A4',
               'EVO_0403': 'A5', 'EVO_1287': 'A6', 'EVO_1896': 'A7', 'EVO_1977': 'A8'}

# Main body ####################################################################


def run(protocol: protocol_api.ProtocolContext):

    # Loading labware ##########################################################

    tips300 = [protocol.load_labware("opentrons_96_tiprack_300ul", rack, label="300ul tips")
               for rack in [9]]
    tips20 = [protocol.load_labware("opentrons_96_tiprack_20ul", rack, label="20ul tips")
              for rack in [6]]

    # IMPORTANT!!! CHANGE the position of the pipette (left/right) if necessary
    p300_single = protocol.load_instrument(
        "p300_single_gen2", "left", tip_racks=tips300)
    p20_single = protocol.load_instrument(
        "p20_single_gen2", "right", tip_racks=tips20)

    # IMPORTANT!!! CHANGE ME to the column of the first available tip. This is necessary if you are
    # using a tip box where some of the tips have already been used. By default it is set to the
    # first column/position (A1) in the tip box.
    p300_single.starting_tip = tips300[0]['A1']
    p20_single.starting_tip = tips20[0]['A1']

    # IMPORTANT!!! CHANGE this if using different number of plates.
    master_plates = [protocol.load_labware("corning_96_wellplate_360ul_flat",
                                           slot, label="Master Mix Plates")
                     for slot in [11]]

    # Load the the bacteria reservoir at deck 1. This is the not the exact same model as in the
    # opentrons labware library but it should work. This should have at least 5 ml in each well

    reservoir = protocol.load_labware("usascientific_12_reservoir_22ml", 8)

    # this loop pipettes the blank R2A
    p300_single.pick_up_tip()
    for P, V in pairs_dict.items():
        if V['sp_A'] == 'blank':
            p300_single.transfer(volume=200,
                                 source=reservoir['A9'],
                                 dest=master_plates[0][P],
                                 touch_tip=False,
                                 new_tip="never")
    p300_single.drop_tip()  # drop tips

    # this loop pipettes the 95% strain of each mixture. It reuses 1 pipette tip for each species
    for sp, reswell in strain_dict.items():
        p300_single.pick_up_tip()
        for P, V in pairs_dict.items():
            if (V['sp_A'] == sp and V['f_A'] == 0.95) or (V['sp_B'] == sp and V['f_B'] == 0.95):
                p300_single.transfer(volume=190,
                                     source=reservoir[reswell],
                                     dest=master_plates[0][P],
                                     touch_tip=True,
                                     new_tip="never")
        p300_single.drop_tip()  # drop tips

    # this loop pipettes the 5% strain of each mixture. It uses a new pipette tip for each transfer
    for sp, reswell in strain_dict.items():
        for P, V in pairs_dict.items():
            if (V['sp_A'] == sp and V['f_A'] == 0.05) or (V['sp_B'] == sp and V['f_B'] == 0.05):
                p20_single.transfer(volume=10,
                                    source=reservoir[reswell],
                                    dest=master_plates[0][P],
                                    touch_tip=True,
                                    new_tip="once")
