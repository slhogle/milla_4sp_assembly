from opentrons import protocol_api
from io import StringIO
import pandas as pd

# note: run source .venv/bin/activate in /home/shane/Documents/projects/method_dev/opentrons for
# development

# REMEMBER! to set offset for tube rack at 10 mm above the edge of the tube

metadata = {
    "protocolName": "Make Trios",
    "description": """This protocol mixes 8 HAMBI species/evo histories into all possible trios with
                   each species either starting at 0.90 and 0.05 fraction once""",
    "author": "Shane Hogle"
}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

# Functions ####################################################################

# Data #########################################################################

# this is annoying but you need to hard code the well/plate layout as a csv string. See here:
# https://support.opentrons.com/s/article/Using-CSV-input-data-in-Python-protocols

trios_csv_raw = '''
Mixture_name,sp_A,sp_B,sp_C,f_A,f_B,f_C,well
T55,ANC_0403,EVO_1896,ANC_1977,0.9,0.05,0.05,A1
T52,EVO_0403,ANC_1896,ANC_1977,0.9,0.05,0.05,A2
T41,EVO_0403,ANC_1287,EVO_1977,0.05,0.9,0.05,A3
T60,EVO_0403,EVO_1896,ANC_1977,0.05,0.05,0.9,A4
T62,ANC_0403,ANC_1896,EVO_1977,0.05,0.9,0.05,A5
T12,EVO_0403,EVO_1287,ANC_1896,0.05,0.05,0.9,A6
T46,EVO_0403,EVO_1287,EVO_1977,0.9,0.05,0.05,A7
T38,ANC_0403,ANC_1287,EVO_1977,0.05,0.9,0.05,A8
T45,ANC_0403,EVO_1287,EVO_1977,0.05,0.05,0.9,A9
T50,ANC_0403,ANC_1896,ANC_1977,0.05,0.9,0.05,A10
T47,EVO_0403,EVO_1287,EVO_1977,0.05,0.9,0.05,A11
T91,ANC_1287,EVO_1896,EVO_1977,0.9,0.05,0.05,A12
T89,EVO_1287,ANC_1896,EVO_1977,0.05,0.9,0.05,B1
T21,ANC_0403,EVO_1287,EVO_1896,0.05,0.05,0.9,B2
T05,EVO_0403,ANC_1287,ANC_1896,0.05,0.9,0.05,B3
T76,EVO_1287,ANC_1896,ANC_1977,0.9,0.05,0.05,B4
T23,EVO_0403,EVO_1287,EVO_1896,0.05,0.9,0.05,B5
T27,ANC_0403,ANC_1287,ANC_1977,0.05,0.05,0.9,B6
T08,ANC_0403,EVO_1287,ANC_1896,0.05,0.9,0.05,B7
T78,EVO_1287,ANC_1896,ANC_1977,0.05,0.05,0.9,B8
T70,EVO_0403,EVO_1896,EVO_1977,0.9,0.05,0.05,B9
T24,EVO_0403,EVO_1287,EVO_1896,0.05,0.05,0.9,B10
T43,ANC_0403,EVO_1287,EVO_1977,0.9,0.05,0.05,B11
T22,EVO_0403,EVO_1287,EVO_1896,0.9,0.05,0.05,B12
T02,ANC_0403,ANC_1287,ANC_1896,0.05,0.9,0.05,C1
T79,ANC_1287,EVO_1896,ANC_1977,0.9,0.05,0.05,C2
T35,EVO_0403,EVO_1287,ANC_1977,0.05,0.9,0.05,C3
T20,ANC_0403,EVO_1287,EVO_1896,0.05,0.9,0.05,C4
T83,EVO_1287,EVO_1896,ANC_1977,0.05,0.9,0.05,C5
T09,ANC_0403,EVO_1287,ANC_1896,0.05,0.05,0.9,C6
T31,ANC_0403,EVO_1287,ANC_1977,0.9,0.05,0.05,C7
T28,EVO_0403,ANC_1287,ANC_1977,0.9,0.05,0.05,C8
T11,EVO_0403,EVO_1287,ANC_1896,0.05,0.9,0.05,C9
T58,EVO_0403,EVO_1896,ANC_1977,0.9,0.05,0.05,C10
T71,EVO_0403,EVO_1896,EVO_1977,0.05,0.9,0.05,C11
T86,ANC_1287,ANC_1896,EVO_1977,0.05,0.9,0.05,C12
T90,EVO_1287,ANC_1896,EVO_1977,0.05,0.05,0.9,D1
T68,ANC_0403,EVO_1896,EVO_1977,0.05,0.9,0.05,D2
T15,ANC_0403,ANC_1287,EVO_1896,0.05,0.05,0.9,D3
T03,ANC_0403,ANC_1287,ANC_1896,0.05,0.05,0.9,D4
T07,ANC_0403,EVO_1287,ANC_1896,0.9,0.05,0.05,D5
T32,ANC_0403,EVO_1287,ANC_1977,0.05,0.9,0.05,D6
T73,ANC_1287,ANC_1896,ANC_1977,0.9,0.05,0.05,D7
T48,EVO_0403,EVO_1287,EVO_1977,0.05,0.05,0.9,D8
T59,EVO_0403,EVO_1896,ANC_1977,0.05,0.9,0.05,D9
T61,ANC_0403,ANC_1896,EVO_1977,0.9,0.05,0.05,D10
T13,ANC_0403,ANC_1287,EVO_1896,0.9,0.05,0.05,D11
T87,ANC_1287,ANC_1896,EVO_1977,0.05,0.05,0.9,D12
T40,EVO_0403,ANC_1287,EVO_1977,0.9,0.05,0.05,E1
T94,EVO_1287,EVO_1896,EVO_1977,0.9,0.05,0.05,E2
T04,EVO_0403,ANC_1287,ANC_1896,0.9,0.05,0.05,E3
T96,EVO_1287,EVO_1896,EVO_1977,0.05,0.05,0.9,E4
T33,ANC_0403,EVO_1287,ANC_1977,0.05,0.05,0.9,E5
T77,EVO_1287,ANC_1896,ANC_1977,0.05,0.9,0.05,E6
T26,ANC_0403,ANC_1287,ANC_1977,0.05,0.9,0.05,E7
T93,ANC_1287,EVO_1896,EVO_1977,0.05,0.05,0.9,E8
T67,ANC_0403,EVO_1896,EVO_1977,0.9,0.05,0.05,E9
T01,ANC_0403,ANC_1287,ANC_1896,0.9,0.05,0.05,E10
T66,EVO_0403,ANC_1896,EVO_1977,0.05,0.05,0.9,E11
T88,EVO_1287,ANC_1896,EVO_1977,0.9,0.05,0.05,E12
T18,EVO_0403,ANC_1287,EVO_1896,0.05,0.05,0.9,F1
T06,EVO_0403,ANC_1287,ANC_1896,0.05,0.05,0.9,F2
T42,EVO_0403,ANC_1287,EVO_1977,0.05,0.05,0.9,F3
T81,ANC_1287,EVO_1896,ANC_1977,0.05,0.05,0.9,F4
T57,ANC_0403,EVO_1896,ANC_1977,0.05,0.05,0.9,F5
T69,ANC_0403,EVO_1896,EVO_1977,0.05,0.05,0.9,F6
T17,EVO_0403,ANC_1287,EVO_1896,0.05,0.9,0.05,F7
T16,EVO_0403,ANC_1287,EVO_1896,0.9,0.05,0.05,F8
T74,ANC_1287,ANC_1896,ANC_1977,0.05,0.9,0.05,F9
T85,ANC_1287,ANC_1896,EVO_1977,0.9,0.05,0.05,F10
T10,EVO_0403,EVO_1287,ANC_1896,0.9,0.05,0.05,F11
T30,EVO_0403,ANC_1287,ANC_1977,0.05,0.05,0.9,F12
T65,EVO_0403,ANC_1896,EVO_1977,0.05,0.9,0.05,G1
T63,ANC_0403,ANC_1896,EVO_1977,0.05,0.05,0.9,G2
T19,ANC_0403,EVO_1287,EVO_1896,0.9,0.05,0.05,G3
T49,ANC_0403,ANC_1896,ANC_1977,0.9,0.05,0.05,G4
T64,EVO_0403,ANC_1896,EVO_1977,0.9,0.05,0.05,G5
T29,EVO_0403,ANC_1287,ANC_1977,0.05,0.9,0.05,G6
T39,ANC_0403,ANC_1287,EVO_1977,0.05,0.05,0.9,G7
T75,ANC_1287,ANC_1896,ANC_1977,0.05,0.05,0.9,G8
T34,EVO_0403,EVO_1287,ANC_1977,0.9,0.05,0.05,G9
T44,ANC_0403,EVO_1287,EVO_1977,0.05,0.9,0.05,G10
T92,ANC_1287,EVO_1896,EVO_1977,0.05,0.9,0.05,G11
T25,ANC_0403,ANC_1287,ANC_1977,0.9,0.05,0.05,G12
T95,EVO_1287,EVO_1896,EVO_1977,0.05,0.9,0.05,H1
T37,ANC_0403,ANC_1287,EVO_1977,0.9,0.05,0.05,H2
T84,EVO_1287,EVO_1896,ANC_1977,0.05,0.05,0.9,H3
T36,EVO_0403,EVO_1287,ANC_1977,0.05,0.05,0.9,H4
T51,ANC_0403,ANC_1896,ANC_1977,0.05,0.05,0.9,H5
T82,EVO_1287,EVO_1896,ANC_1977,0.9,0.05,0.05,H6
T53,EVO_0403,ANC_1896,ANC_1977,0.05,0.9,0.05,H7
T14,ANC_0403,ANC_1287,EVO_1896,0.05,0.9,0.05,H8
T80,ANC_1287,EVO_1896,ANC_1977,0.05,0.9,0.05,H9
T72,EVO_0403,EVO_1896,EVO_1977,0.05,0.05,0.9,H10
T56,ANC_0403,EVO_1896,ANC_1977,0.05,0.9,0.05,H11
T54,EVO_0403,ANC_1896,ANC_1977,0.05,0.05,0.9,H12
'''

trios_csv = pd.read_csv(StringIO(trios_csv_raw))
trios_dict = trios_csv.set_index('well').to_dict(orient='index')

# Main body ####################################################################


def run(protocol: protocol_api.ProtocolContext):

    # Loading labware ##########################################################

    tips1000 = [protocol.load_labware("opentrons_96_tiprack_1000ul", rack, label="1000ul tips")
                for rack in [9]]
    tips20 = [protocol.load_labware("opentrons_96_tiprack_20ul", rack, label="20ul tips")
              for rack in [3, 6]]

    # IMPORTANT!!! CHANGE the position of the pipette (left/right) if necessary
    p1000_single = protocol.load_instrument(
        "p1000_single_gen2", "left", tip_racks=tips1000)
    p20_single = protocol.load_instrument(
        "p20_single_gen2", "right", tip_racks=tips20)

    # IMPORTANT!!! CHANGE ME to the column of the first available tip. This is necessary if you are
    # using a tip box where some of the tips have already been used. By default it is set to the
    # first column/position (A1) in the tip box.
    p1000_single.starting_tip = tips1000[0]['A1']
    p20_single.starting_tip = tips20[0]['A1']

    # IMPORTANT!!! CHANGE this if using different number of plates.
    master_plates = [protocol.load_labware("corning_96_wellplate_360ul_flat",
                                           slot, label="Master Mix Plates")
                     for slot in [11]]

    # Load the the bacteria tubes at deck 10 (tuberackA) and deck 8 (tuberackB). Should have at least 10 ml in each tube

    tuberackA = protocol.load_labware("opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", 10)
    tuberackB = protocol.load_labware("opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", 8)

    strain_dict = {'ANC_0403': tuberackA['A3'], 'ANC_1287': tuberackA['A4'], 'ANC_1896': tuberackA['B3'], 'ANC_1977': tuberackA['B4'],
                   'EVO_0403': tuberackB['A3'], 'EVO_1287': tuberackB['A4'], 'EVO_1896': tuberackB['B3'], 'EVO_1977': tuberackB['B4']}

    #### this loop distribtues the 90% strain of each mixture. ####
    #### It uses one pipette tip to keep it fast               ####

    for sp, tube in strain_dict.items():
        sp90wells = [] # get list of wells with 0.90 fractions
        for P, V in trios_dict.items():
            if (V['sp_A'] == sp and V['f_A'] == 0.90) or (V['sp_B'] == sp and V['f_B'] == 0.90) or (V['sp_C'] == sp and V['f_C'] == 0.90):
                sp90wells.append(master_plates[0].wells_by_name()[P])
        p1000_single.distribute(volume=180,
                                source=tube,
                                dest=sp90wells,
                                mix_before=(1, 500),
                                touch_tip=False,
                                blow_out=False,
                                blowout_location="source well",
                                disposal_volume=0,
                                air_gap=50,
                                new_tip="once")

    #### this loop distribtues the 5% strain of each mixture. ####
    #### It uses a new pipette tip for each transfer because  ####
    #### it is dispensing into a bacterial culture            ####

    for sp, tube in strain_dict.items():
        sp05wells = []  # get list of wells with 0.05 fractions
        for P, V in trios_dict.items():
            if (V['sp_A'] == sp and V['f_A'] == 0.05) or (V['sp_B'] == sp and V['f_B'] == 0.05) or (V['sp_C'] == sp and V['f_C'] == 0.05):
                sp05wells.append(master_plates[0].wells_by_name()[P])
        p20_single.transfer(volume=10,
                            source=tube,
                            dest=sp05wells,
                            touch_tip=False,
                            blow_out=False,
                            blowout_location="trash",
                            disposal_volume=0,
                            air_gap=1,
                            new_tip="always")
