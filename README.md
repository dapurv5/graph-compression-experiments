# graph-compression-experiments
simple graph compression heuristics


https://docs.google.com/spreadsheets/d/11fAXU5Vt3MTevokwXgP6R2DCmu3vuR9HObFzWPMlSZA/edit#gid=0




### Typical Dev. Cycle

- Write an algorithm by subclassing Compressor(Java code)

- mvn assembly:single (for creating the unified jar with dependencies)

- modify experiment.py to include this new algorithm in the experiment run

- python experiment.py (creates a results.tsv file and plots in the plots folder)

- import tsv files to google spreadsheet and compare results.

