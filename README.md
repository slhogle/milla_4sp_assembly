# Introduction

This protocol mixes 8 HAMBI species/strains in different proportions and combinations into a 96-well master plate.
The master plate can be used to inuclate serial transfer experiments. `01_distribute_pairs.py` is used to mix the 48 different 
pairwise combinations/proportions and `02_distribute_trios.py` is used to mix the 96 different trio combinations/proportions. The
ipython notebook is just for performing some simple scratch calculations if needed. 

# Reagents
- R2A, sterile
- 8 bacteria species/strains with normalized optical density
  - ANC HAMBI_0403 
  - ANC HAMBI_1287
  - ANC HAMBI_1896
  - ANC HAMBI_1977
  - EVO HAMBI_0403 
  - EVO HAMBI_1287
  - EVO HAMBI_1896
  - EVO HAMBI_1977

# Equipment
- 96 well plates (sterile)
- 9x 50 ml Falcon tubes (sterile)
- 2x Opentrons 10 Tube Rack with Falcon 4x50 mL, 6x15 mL Conical
- Opentrons P20 single channel pipette
- Opentrons P1000 single channel pipette
- Opentrons P1000 1000 ul pipette tips (sterile)
- Opentrons P20 20 ul pipette tips (sterile)

# IMPORTANT: Editing scripts
If you need to change defaults in these scripts you will need to edit the scripts directly before importing them into
the Opentrons app.

1. You should verify/check whether the p20 or p1000 are on the left or right side of the robot. This can be
   changed in the variables `p1000_single` and `p20_single`
2. The deck locations of the Opentrons 10 Tube Racks are set in the variables `tuberackA` 
   and `tuberackB.` 
3. If some columns of tipsrack have already been used then you can specify the tip
   position you want the robot to start from in your tip box . The default position is 'A1.' 
   This can be changed by setting the variables `p1000_single.starting_tip` and `p20_single.starting_tip`
4. The master plate wells and their corresponding species mixtures are mapped in the variable `pairs_csv_raw` or `trios_csv_raw.`
   This variable hold the csv as a raw string. It can be modified by copying and pasting from a spreadsheet editor. 

# Procedure

1. Grow overnight cultures of each species/strain.
2. Normalize the overnight cultures to the lowest optical density strain/species so that all cultures have the
   same optical density. For example, if the lowest optical density of all species is 0.4 then dilute all the other species with sterile M9
   to have an optical density of 0.4. 
3. Wipe down the inside of the OT2 using isopropyl alcohol to try and keep the robot workspace as sterile as possible.

## For setting up pairs: 
4. Gather the master 96-well plate, one 1000 ul tip box, one 20 ul tip box, the Falcon tube racks, and the 
Falcon tubes with bacteria. Add ~10 ml of sterile R2A to one empty 50 ml Falcon tube. Arrange the Falcon tubes as specified in variables `tuberackA` and `tuberackB.` The default arrangement is 
  - `tuberackA['A3']` ANC HAMBI_0403 
  - `tuberackA['A4']` ANC HAMBI_1287
  - `tuberackA['B3']` ANC HAMBI_1896
  - `tuberackA['B4']` ANC HAMBI_1977
  - `tuberackB['A3']` EVO HAMBI_0403 
  - `tuberackB['A4']` EVO HAMBI_1287
  - `tuberackB['B3']` EVO HAMBI_1896
  - `tuberackB['B4']` EVO HAMBI_1977
5. [Import](https://support.opentrons.com/s/article/Get-started-Import-a-protocol) and
   [run](https://support.opentrons.com/s/article/Get-started-Run-your-protocol) the protocol
   `01_distribute_pairs.py`. Here it is important to perform the ["Labware Position
   Check"](https://support.opentrons.com/s/article/How-positional-calibration-works-on-the-OT-2#LPC)
   which will allow you to [set
   offsets](https://support.opentrons.com/s/article/How-Labware-Offsets-work-on-the-OT-2)
   for the Falcon tubes. **MOST IMPORTANT** is to set the "z" offset for the Falcon tubes to be 10 mm above the tube edge. 
   This ensures that the OT-2 doesn't lower tips too deeply into the Falcon tubes. 
6. Right before starting the pairs protocol, place the sterile R2A Falcon tube in A3 of tuberackA in place of ANC HAMBI_0403.
7. Let the protocol add sterile R2A to 48 wells. When it finishes the last well, pause the protocol on the computer and swap
in ANC HAMBI_0403 into A3 of tuberackA.
8. Allow the protocol finish. The total time should be approximately 30 minutes.

## For setting up trios:
8. Gather the master 96-well plate, one 1000 ul tip box, **two** 20 ul tip boxes, the Falcon tube racks, and the 
Falcon tubes with bacteria. Arrange the Falcon tubes as specified in variables `tuberackA` and `tuberackB` and as describe in step 4 
above. Again, the default arrangement is 
  - `tuberackA['A3']` ANC HAMBI_0403 
  - `tuberackA['A4']` ANC HAMBI_1287
  - `tuberackA['B3']` ANC HAMBI_1896
  - `tuberackA['B4']` ANC HAMBI_1977
  - `tuberackB['A3']` EVO HAMBI_0403 
  - `tuberackB['A4']` EVO HAMBI_1287
  - `tuberackB['B3']` EVO HAMBI_1896
  - `tuberackB['B4']` EVO HAMBI_1977
9. Setup the labware following the deck layout on the opentrons app. 
10. Run the protocol (see step 5 above). The total time should be a little longer than 60 minutes.
