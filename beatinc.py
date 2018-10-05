#! python3
# constants
ImpedOfFreeSpace = 377  # Ohms 
SpeedOfLight = 9.84e8   # Ft/sec 
pi = 3.1415927
ResistCopper = 6.79e-7  # Ohms inch 
ScreenDepth = 24
ScreenWidth = 80
BIG = 1.0e36
SMALL = 1.0e-36
MaxOpt = 15             # Maximum number of menu selections 
MaxUnits = 10           # Number of various units required for input 
StrLen = 50             # Length of string arrays 
Iseed = 123             # Dummy constant for random0  
IterationsMax = 100     # Max Num of iterations for stat analysis

# variables
OptArray = [None] * 15

# Define default parameter values
NumPoints = 5
NumHarmonics = 10
Time = [0.0] * (NumPoints + 2)
Magnitude = [0.0] * (NumPoints + 2)
base = [None] * 3
base[1] = 'Metric'
base[2] = 'Imperial'
    
Ende = False
DiConst = 4.7
EffDiConst = DiConst
LoadImp = 100
LineImp = 100
IntImped = 50
EffImped = 100
IntProp = 2.5
DistCap = 0
TraceThick = 0.0021
TraceWidth = 0.011
TraceHeight = 0.026
TraceSpacing = 0.089
TraceLength = 10
TraceThickSigma = 0.001  
TraceWidthSigma = 0.001
TraceHeightSigma = 0.001
DiConstSigma = 0.1
EmbedHeight = 0.004
EmbedHeightSigma = 0.001
Period = 20.0
SigPlaneSep = 0.004
SigPlaneSepSigma = 0.001
NumIterations = 10
SoldMask = 'n'
UnitSys = 1
Resist = 30
TRise = 1
DistCap = 2
EvenLineImp = 0
OddLineImp = 0
EvenIntProp = 0
OddIntProp = 0
