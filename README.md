# CharlieParkerImprovProgram
  A program which models musical improvisation by creating a markov model based upon the improvised solos of the famous saxophonist Charlie Parker.
This program uses a collection of midi files of the songs featured in the Charlie Parker Omnibook and transforms the note transitions featured in 
these files into markov transition matrices based on the chord transition a given note transition is performed over. The program is then able to 
generate a composition given an input of chord changes by walking along the markov transition matrices for the duration of each chord.

Complete:

  - Data structures
  - Data structure test suite
   
In Progress:
  
   - Midi reader
   - Midi reader test suite
 
 Not Yet Started:
 
   - Composition generator
   - Composition generator test suite
