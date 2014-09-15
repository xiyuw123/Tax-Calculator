'''
It has become apparent that the initial implementation of conditionals using
numpy.where and numpy.logical_and/or functions yields in our case some 
hard to read code (see below).

We are thinking of ways to fix these issues and will be adding mockups shortly.

'''


##
# Np.Where gruesome example
def SSBenefits():
    #Social Security Benefit Taxation
    global c02500   
    c02500 = np.where(np.logical_or(SSIND != 0, np.logical_or(MARS == 3, MARS == 6)), e02500, 
        np.where(_ymod < _ssb50[MARS-1], 0, 
            np.where(np.logical_and(_ymod >= _ssb50[MARS-1], _ymod < _ssb85[MARS-1]), 0.5 * np.minimum(_ymod - _ssb50[MARS-1], e02400),
                np.minimum(0.85 * (_ymod - _ssb85[MARS-1]) + 0.50 * np.minimum(e02400, _ssb85[MARS-1] - _ssb50[MARS-1]), 0.85 * e02400
                    ))))

    outputs = (c02500, e02500)
    output = np.column_stack(outputs)
    np.savetxt('SSBenefits.csv', output, delimiter=',', 
        header = ('c02500, e02500') 
        , fmt = '%1.3f')

