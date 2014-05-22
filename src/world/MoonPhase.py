'''
Created on May 22, 2014

@author: dstuart
'''

#############################################
#
# Just some notes about the moon phase feature for now
#
# Phases in order:
# New
# Waxing crescent
# First quarter
# Waxing gibbous
# Full
# Waning gibbous
# Third quarter
# Waning crescent
# New
# 
# Cycle is ~29.5 days
# Each phase is 3.6875 days long
# 
# The approximate age of the moon, and hence the approximate phase, 
# can be calculated for any date by calculating the number of days 
# since a known new moon (such as January 1, 1900 or August 11, 1999) 
# and reducing this modulo 29.530588853 (the length of a synodic month).
#
# Time between blue moons is 2.7145 years
#
# Full moon names:
# January: "Wolf Moon" "Old Moon"
# February: "Snow Moon", also "Hunger Moon"
# March: "Worm Moon", "Crow Moon", "Sap Moon", "Lenten Moon"
# April: "Seed Moon", "Pink Moon", "Sprouting Grass Moon", "Egg Moon" (c.f. "Goose-Egg" in Beard 1918), "Fish Moon"
# May: "Milk Moon", "Flower Moon", "Corn Planting Moon"
# June: "Mead Moon", "Strawberry Moon" (c.f. Beard 1918), "Rose Moon", "Thunder Moon"
# July: "Hay Moon", "Buck Moon", "Thunder Moon"
# August: "Corn Moon", "Sturgeon Moon", "Red Moon", "Green Corn Moon", "Grain Moon"
# September: "Harvest Moon", "Full Corn Moon",
# October: "Hunter's Moon", "Blood Moon"/"Sanguine Moon"
# November: "Beaver Moon", "Frosty Moon"
# December: "Oak Moon", "Cold Moon", "Long Nights Moon"
# 
# Eclipse cycle: http://en.wikipedia.org/wiki/Saros_(astronomy)
#
#
#############################################
