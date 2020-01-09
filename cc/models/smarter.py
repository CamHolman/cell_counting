import numpy as np
import skimage as sk
import cc.models.train_model as cc.train

def strain(ranges, ):
    for minS in [ranges('min_sigma_low'), ranges('min_sigma_high')]:
        pearson = run_pears

    """
    test the min max and average of each condition beofre iterating
    through all. Find those that create a dramatic difference

        for now: delta(pearson) >= 0.5

    then, ignore all the parameters that dont lead to a sigdif

    iterate specifically through all those that cause sigdif

        1) try default params get pearson
        2) min / max rage of each param find those that cause the largest diff
        3) set all those that didnt make a sigdif to defaults(? - maybe better the end that was
            slightly higher
        4) iterate through affecting parameters, collect pearsons
        5) ???
        6) profit

    * is pearson the correct correlation measure?

    what does random tree use? Fairly unrelated

    """