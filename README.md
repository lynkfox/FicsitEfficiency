# FicsitEfficiency

A set of scripts and graphs for comparing any possible permutiation of recipes (standard and alternates) for any component in the game Satisfactory by Coffee Stain Studios

All data about in game assets is Copywrite CSS;


## xml-json.py
Parses the xml that was scraped from game pak files by @SillyBits on the Modding Discord into a json with what data this project needs.

## main.py

Currently just generates all possible paths of the directed graph tree of potential recipie combinations

## ./unit_tests

Unit tests. Some of them anyways

## ./ficsit

main module

## ficsit/effeciency.py

contains the class for creating recipe paths

TODO: Update to a proper weighted directed graph (utilizing the recipe.json objects)

## ficsit/components.py

constants

## ficsit/effeciency_calcualtions.py

Math and other functions.

## ficsit/utils.py

Helper/common functions

## fisit/possible_paths

Output jsons of all possible paths for any given recipe.
