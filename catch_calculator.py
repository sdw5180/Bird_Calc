"""
Calculates the catch rate for several legendaries in the game Pokemon Go.

The catch rate fomula is:

    P   = 1- ( 1 - ( BASE_RATE / 2 * CPM))^modi

        BASE_RATE:  The base catch rate of a pokemon; this varies by species.
        CPM:        A float number that varries based on a pokemon's level:
                    [0.094 - 0.0.7317] for levels 1-30.
                    * This calculator uses the CPM range for WILD encounters.
        modi:       Catch modifier that takes into account a variety of 
                    variables (see below).
Where:
    modi = BALL * BERRY * THROW * CURVE * MEDAL * ENCOUNTER

        BALL:       [1 - 2] depending on pokeball used
        BERRY:      [1 - 2.5] depending on berry ysed
        THROW:      [1 - 2] depending on throw acheived
        CURVE:      1 for non-curve, 1.7 for curveball throw
        MEDAL:      [1 - 1.4] depending on player's type medals
        ENCOUNTER:  1 for wild, 2 for research, 10 for GoFest raid battles
    
    Note:   this calculator assumes that every throw uses a Golden Raspberry
            Curveball Throw, and platinum medal

@Author     Cedar Wood
@Date       09/20/24         (mm/dd/yy)
@Update     09/23/24

"""
import math



# GLOBALS
BASE_RATE   = 0.003                     # 0.3% for the galarian legendary trio

BERRY       = 2.5                           # Razzberry
CURVE       = 1.7                           # Curveball
ENCOUNTER   = 1                             # Wild Encounter
MEDAL       = 1.4                           # Platinum Medal(s)
BALL        = 2                             # Ultra Ball

SUCCESS_PERC = 0.99                     # Desired success chance after N throws
P_MIN_SUCCESS_PERC = 1 - SUCCESS_PERC       # 1 - p(catch after n throws)



# maps the CPM number to each pokemon level:
CPM = {
        '1'     : 0.094,
        '10'    : 0.4225,
        '20'    : 0.5974,
        '30'    : 0.7317
}



# maps the throw multiplier to each throw level note that each throw type gives a 
# range of multipliers, so an average for each type of throw is used:
THROW = {
        'NONE'  : 1,
        'NICE'  : 1.2,
        'GREAT' : 1.5,
        'EXCELENT' : 1.9
}



def calc_modi():
    """
    Calculates the modifier for the catch:
        modi = BALL * BERRY * THROW * CURVE * MEDAL * ENCOUNTER

    NOTE: this currently always returns the same result, but is designed to be
    future-proof for more variability in the future
    """
    modifier = BALL * BERRY * CURVE * MEDAL * ENCOUNTER

    modifier_none =     modifier * THROW['NONE']
    modifier_nice =     modifier * THROW['NICE']
    modifier_great =    modifier * THROW['GREAT']
    modifier_excelent = modifier * THROW['EXCELENT']

    # return all four modifiers by catch type:
    return modifier_none, modifier_nice, modifier_great, modifier_excelent



def calc_catch(CPM):
    """
    Calculates the probability of a successful catch:
            P   = 1 - ( 1 - ( BASE_RATE / 2 * CPM))^modi
            p   = 1 - catch_p^modi
    """
    modifier_none, modifier_nice, modifier_great, modifier_excelent = calc_modi()   # returns FOUR floats
    catch_p = ( 1 - BASE_RATE / ( 2 * CPM))

    catch_none =     1 - (pow(catch_p, modifier_none))
    catch_nice =     1 - (pow(catch_p, modifier_nice))
    catch_great =    1 - (pow(catch_p, modifier_great))
    catch_excelent = 1 - (pow(catch_p, modifier_excelent))

    return catch_none, catch_nice, catch_great, catch_excelent



def calc_avg(p_none, p_nice, p_great, p_excelent):
    """
    Calculates the average number of throws needed to for each throw tier: 
        NORMAL, NICE, GREAT, EXCELEMT

        # successes = p(success) * # attempts
        1 = p * n
        n = 1/p
    """
    return 1/p_none, 1/p_nice, 1/p_great, 1/p_excelent



def calc_throws(catch_rate):
    """
    Caculctes the number of pokeballs needed to acheive a set persentage chance of 
    catching a bird:
    p(catch after n throws) = 1 - ( 1 - p(catch) )^n
    ...
    n = log a / log b
        a = p(catch after n throws)                 <- desired
        b = 1 - p(catch)
        n = number of attempts (pokeballs needed)
    """

    if (catch_rate == 0):                   # If no rate is provided, use base catch rate
        catch_rate = BASE_RATE

    throws = 0                              # n
    break_out_rate = 1 - catch_rate         # b
    #P_MIN_SUCCESS_PERC                     # a
    
    throws = math.log(P_MIN_SUCCESS_PERC) / math.log(break_out_rate)
    return throws



def round_catch(prob):
    """
    Round and format the Probability to two decimal places
    """
    #return str(round(prob * 100, 2)) + ' %'
    return str(round(prob * 100)) + ' %'



def round_avg(average):
    """
    Round and format the Average
    """
    return str(round(average)) + " Av."



def main():
    """
    Caculates the catch rate for each galarian bird, then prints a table displaying 
    the rate for Excelent, Great, Nice, and regular throws at several levels. Use of
    Ulra Balls and Golden Raspberry is assumed for all throws.
    """
    #pokemon = input("Enter choice?"                    # < - for future aditions, 
    #                 + "\n * A - G!Articuno"           # uncomment to allow modification
    #                 + "\n * M - G!Moltres"
    #                 + "\n * Z - G!Zapdos\n")
    # If the input isn't in the list of avalable pokemon:
    #if ((pokemon != 'A') & (pokemon != 'M') & (pokemon != 'Z')):
    #    print("\ninvalid choice")
    #    exit(-1)

    # Header info:
    print("--------------------------\n"
          + "Catching: " + "Galarian Bird" + "\n"
          + "Galarian Bird" + " has a base catch rate of: " + str(BASE_RATE) + "\n" +
          "Each cell indicates both the percentage chance and the average number of throws for a successful catch.\n")
    
    # Column headers:
    print("\t\tNONE\t\t\tNICE\t\t\tGREAT\t\t\tEXCELENT\t\tFor a " + str(round(SUCCESS_PERC * 100)) + "%" + " catch chance:\n" +
          "\t    __________________________________________________________________________________________________________________________________________________________________")

    # For each level, calculate and print the catch rate, average throws, and tot. num for 99 success rate:
    levels = ['1', '10', '20', '30']
    for level in levels:
        if (level == '1'):
            print("level " + level + "    |"  , end='')          # end='' prevents newline char
        else:
            print("level " + level + "   |"    , end='')

        # Calculate the chance of a successful throw with a NONE, NICE, GREAT, and EXCELENT throw:
        catch_none, catch_nice, catch_great, catch_excelent = calc_catch(CPM[level])

        # Caculate the average number of throws for a success with NONE, NICE, GREAT, and EXCELENT throws:
        avg_none, avg_nice, avg_great, avg_excelent = calc_avg(catch_none, catch_nice, catch_great, catch_excelent)

        # Calculate the number of throws to acheive aSUCCESS_PERC % chance of a catch:
        e_throws = calc_throws(catch_excelent)
        n_throws = calc_throws(catch_none)
        
        #print("\t __%__\t\t __%__\t\t __%__\t\t __%__")
        # Output data in a table:
        print("\t" +  round_catch(catch_none)       + " | " + round_avg(avg_none) +
              "\t\t" + round_catch(catch_nice)      + " | " + round_avg(avg_nice) +
              "\t\t"+ round_catch(catch_great)      + " | " + round_avg(avg_great) +
              "\t\t" + round_catch(catch_excelent)  + " | " + round_avg(avg_excelent) +
              "\t\t" +
              str(round(e_throws)) + " EXCELENT throws / " + 
              str(round(n_throws)) + " NORMAL throws")
    

    # Disclaimer
    print('\nThis calculation assumes:\n' + 
          ' * Golden RazzBerry\n'
          ' * Curveball Throw\n'
          ' * Ultra Ball\n'
          + ' * Platinum Catch Medal(s)')


main()      # run everything lol
print()     # newline