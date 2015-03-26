import pandas as pd
from pandas import DataFrame
import math
import numpy as np
from .utils import *
from .functions import *
from .parameters import Parameters
from .records import Records


all_cols = set()
def add_df(alldfs, df):
    for col in df.columns:
        if col not in all_cols:
            all_cols.add(col)
            alldfs.append(df[col])
        else:
            dup_index = [i for i,series in enumerate(alldfs) if series.name == col][0]
            alldfs[dup_index] = df[col]


def calculator(parameters, records, mods="", **kwargs):
    update_mods = {}
    if mods:
        if isinstance(mods, str):
            import json
            dd = json.loads(mods)
            dd = {k:np.array(v) for k,v in dd.items() if type(v) == list}
            update_mods.update(dd)
        else:
            update_mods.update(mods)

    update_mods.update(kwargs)
    parameters.update(update_mods)
    calc = Calculator(parameters, records)

    return calc

class Calculator(object):

    @classmethod
    def from_files(cls, pfname, rfname, **kwargs):
        """
        Create a Calculator object from a Parameters JSON file and a
        Records file

        Parameters
        ----------
        pfname: filename for Parameters

        rfname: filename for Records
        """
        params = Parameters.from_file(pfname, **kwargs)
        recs = Records.from_file(rfname, **kwargs)
        return cls(params, recs)


    def __init__(self, parameters=None, records=None, sync_years=True, **kwargs):

        if isinstance(parameters, Parameters):
            self._parameters = parameters
        else:
            self._parameters = Parameters.from_file(parameters, **kwargs)

        if records is None:
            raise ValueError("Must supply tax records path or Records object")

        self._records = (records if not isinstance(records, str) else
                         Records.from_file(records, **kwargs))

        if sync_years and self._records.current_year==2008:
            print("You loaded data for "+str(self._records.current_year)+'.')

            while self._records.current_year < self._parameters.current_year:
                self._records.increment_year()

            print("Your data have beeen extrapolated to "+str(self._records.current_year)+".")

        assert self._parameters.current_year == self._records.current_year

    def __deepcopy__(self, memo):
        import copy
        params = copy.deepcopy(self._parameters)
        recs = copy.deepcopy(self._records)
        return Calculator(params, recs)

    @property
    def parameters(self):
        return self._parameters

    @property
    def records(self):
        return self._records

    def __getattr__(self, name):
        """
        Only allowed attributes on a Calculator are 'parameters' and 'records'
        """

        if hasattr(self.parameters, name):
            return getattr(self.parameters, name)
        elif hasattr(self.records, name):
            return getattr(self.records, name)
        else:
            try:
                self.__dict__[name]
            except KeyError:
                raise AttributeError(name + " not found")

    def __setattr__(self, name, val):
        """
        Only allowed attributes on a Calculator are 'parameters' and 'records'
        """

        if name == "_parameters" or name == "_records":
            self.__dict__[name] = val
            return

        if hasattr(self.parameters, name):
            return setattr(self.parameters, name, val)
        elif hasattr(self.records, name):
            return setattr(self.records, name, val)
        else:
            self.__dict__[name] = val

    def __getitem__(self, val):

        if val in self.__dict__:
            return self.__dict__[val]
        else:
            try:
                return getattr(self.parameters, val)
            except AttributeError:
                try:
                    return getattr(self.records, val)
                except AttributeError:
                    raise




    def calc_all(self):
        FilingStatus(self.parameters, self.records)
        Adj(self.parameters, self.records)
        CapGains(self.parameters, self.records)
        SSBenefits(self.parameters, self.records)
        AGI(self.parameters, self.records)
        ItemDed(self.parameters, self.records)
        EI_FICA(self.parameters, self.records)
        AMED(self.parameters, self.records)
        StdDed(self.parameters, self.records)
        XYZD(self.parameters, self.records)
        NonGain(self.parameters, self.records)
        TaxGains(self.parameters, self.records)
        MUI(self.parameters, self.records)
        AMTI(self.parameters, self.records)
        F2441(self.parameters, self.records)
        DepCareBen(self.parameters, self.records)
        ExpEarnedInc(self.parameters, self.records)
        RateRed(self.parameters, self.records)
        NumDep(self.parameters, self.records)
        ChildTaxCredit(self.parameters, self.records)
        AmOppCr(self.parameters, self.records)
        LLC(self.parameters, self.records)
        RefAmOpp(self.parameters, self.records)
        NonEdCr(self.parameters, self.records)
        AddCTC(self.parameters, self.records)
        F5405(self.parameters, self.records)
        C1040(self.parameters, self.records)
        DEITC(self.parameters, self.records)
        OSPC_TAX(self.parameters, self.records)

    def calc_all_test(self):
        all_dfs = []
        add_df(all_dfs, FilingStatus(self.parameters, self.records))
        add_df(all_dfs, Adj(self.parameters, self.records))
        add_df(all_dfs, CapGains(self.parameters, self.records))
        add_df(all_dfs, SSBenefits(self.parameters, self.records))
        add_df(all_dfs, AGI(self.parameters, self.records))
        add_df(all_dfs, ItemDed(self.parameters, self.records))
        add_df(all_dfs, EI_FICA(self.parameters, self.records))
        add_df(all_dfs, AMED(self.parameters, self.records))
        add_df(all_dfs, StdDed(self.parameters, self.records))
        add_df(all_dfs, XYZD(self.parameters, self.records))
        add_df(all_dfs, NonGain(self.parameters, self.records))
        add_df(all_dfs, TaxGains(self.parameters, self.records))
        add_df(all_dfs, MUI(self.parameters, self.records))
        add_df(all_dfs, AMTI(self.parameters, self.records))
        add_df(all_dfs, F2441(self.parameters, self.records))
        add_df(all_dfs, DepCareBen(self.parameters, self.records))
        add_df(all_dfs, ExpEarnedInc(self.parameters, self.records))
        add_df(all_dfs, RateRed(self.parameters, self.records))
        add_df(all_dfs, NumDep(self.parameters, self.records))
        add_df(all_dfs, ChildTaxCredit(self.parameters, self.records))
        add_df(all_dfs, AmOppCr(self.parameters, self.records))
        add_df(all_dfs, LLC(self.parameters, self.records))
        add_df(all_dfs, RefAmOpp(self.parameters, self.records))
        add_df(all_dfs, NonEdCr(self.parameters, self.records))
        add_df(all_dfs, AddCTC(self.parameters, self.records))
        add_df(all_dfs, F5405(self.parameters, self.records))
        add_df(all_dfs, C1040(self.parameters, self.records))
        add_df(all_dfs, DEITC(self.parameters, self.records))
        add_df(all_dfs, OSPC_TAX(self.parameters, self.records))
        totaldf = pd.concat(all_dfs, axis=1)
        return totaldf

    def increment_year(self):
        self.records.increment_year()
        self.parameters.increment_year()

    @property
    def current_year(self):
        return self.parameters.current_year


    def mtr(self, income_type_string, diff = 100):
        """
        This method calculates the marginal tax rate for every record. 
        In order to avoid kinks, we find the marginal rates associated with 
        both a tax increase and a tax decrease and use the more modest of 
        the two. 
        """

        income_type = getattr(self, income_type_string)
        
        # Calculate the base level of taxes. 
        self.calc_all()
        taxes_base = np.copy(self._ospctax)

        # Calculate the tax change with a marginal increase in income.
        setattr(self, income_type_string, income_type + diff)
        self.calc_all()
        delta_taxes_up = self._ospctax - taxes_base

        # Calculate the tax change with a marginal decrease in income.
        setattr(self, income_type_string, income_type - diff)
        self.calc_all()
        delta_taxes_down = taxes_base - self._ospctax

        # Reset the income_type to its starting point to avoid 
        # unintended consequences. 
        setattr(self, income_type_string, income_type)
        self.calc_all()

        # Choose the more modest effect of either adding or subtracting income.
        delta_taxes = np.where( np.absolute(delta_taxes_up) <= 
                            np.absolute(delta_taxes_down), 
                            delta_taxes_up , delta_taxes_down)

        # Calculate the marginal tax rate
        mtr = delta_taxes / diff

        return mtr
    
    def baseline_table(self, num_years = 5):
        table = []
        row_years = []
        for i in range(0,num_years):
            self.calc_all()
            row_years.append(self.current_year)
            #totoal number of records
            returns = self.s006.sum()
            
            #AGI
            agi = (self.c00100*self.s006).sum()
            
            #number of itemizers
            ID1= self.c04470 * self.s006
            STD1 = self._standard * self.s006
            NumItemizer1 = self.s006[ID1>STD1].sum()
            
            #itemized deduction
            ID = ID1[STD1<ID1].sum()
            
            #number of standardizers
            NumSTD = self.s006[self._standard > self.c04470].sum()
            
            #standard deduction
            STD = (self._standard * self.s006).sum()
            
            #personal exemption
            PE = (self.c04600*self.s006).sum()
            
            #taxable income
            taxinc = (self.c04800*self.s006).sum()
            
            #regular tax
            regular_tax = (self.c05200*self.s006).sum()
            
            #AMT income
            AMTI = (self.c62100 * self.s006).sum()
            
            #total AMTs
            AMT = (self.c09600*self.s006).sum()
            
            #number of people paying AMT
            NumAMT1 = self.s006[self.c09600>0].sum()
            
            
            #tax before nonrefundable credits 09200
            tax_bf_credits = (self.c05800 * self.s006).sum()
            
            #refundable credits
            refundable = (self._refund * self.s006).sum()
            
            #nonrefuncable credits
            nonrefundable = (self.c07100 * self.s006).sum()
            
            #ospc_tax
            revenue1 = (self._ospctax * self.s006).sum()
            
            
            table.append([returns/math.pow(10,6),agi/math.pow(10,9),NumItemizer1/math.pow(10,6), 
                          ID/math.pow(10,9), NumSTD/math.pow(10,6), STD/math.pow(10,9),  
                          PE/math.pow(10,9), taxinc/math.pow(10,9), 
                          regular_tax/math.pow(10,9), AMTI/math.pow(10,9), AMT/math.pow(10,9), NumAMT1/math.pow(10,6), 
                          tax_bf_credits/math.pow(10,9),refundable/math.pow(10,9), 
                          nonrefundable/math.pow(10,9), revenue1/math.pow(10,9)])
            
            self.increment_year()
          
        df = DataFrame(table, row_years, 
               ["Returns (#m)", "AGI ($b)", "Itemizers (#m)", "Itemized Deduction ($b)", "Standard Deduction Filers (#m)", 
                "Standard Deduction ($b)", "Personal Exemption ($b)", "Taxable income ($b)", 
                "Regular Tax ($b)", "AMTI ($b)", "AMT amount ($b)", "AMT number (#m)", "Tax before credits ($b)", 
                "refundable credits ($b)", "nonrefundable credits ($b)",
                "ospctax ($b)"])
        df = df.transpose()
        pd.options.display.float_format = '{:8,.1f}'.format
        df.to_csv('baseline.csv')
        return df

    def baseline_table(self, num_years = 5):
        table = []
        row_years = []
        for i in range(0,num_years):
            self.calc_all()
            row_years.append(self.current_year)
            #totoal number of records
            returns = self.s006.sum()
            
            #AGI
            agi = (self.c00100*self.s006).sum()
            
            #number of itemizers
            ID1= self.c04470 * self.s006
            STD1 = self._standard * self.s006
            NumItemizer1 = self.s006[ID1>STD1].sum()
            
            #itemized deduction
            ID = ID1[STD1<ID1].sum()
            
            #number of standardizers
            NumSTD = self.s006[self._standard > self.c04470].sum()
            
            #standard deduction
            STD = (self._standard * self.s006).sum()
            
            #personal exemption
            PE = (self.c04600*self.s006).sum()
            
            #taxable income
            taxinc = (self.c04800*self.s006).sum()
            
            #regular tax
            regular_tax = (self.c05200*self.s006).sum()
            
            #AMT income
            AMTI = (self.c62100 * self.s006).sum()
            
            #total AMTs
            AMT = (self.c09600*self.s006).sum()
            
            #number of people paying AMT
            NumAMT1 = self.s006[self.c09600>0].sum()
            
            
            #tax before nonrefundable credits 09200
            tax_bf_credits = (self.c05800 * self.s006).sum()
            
            #refundable credits
            refundable = (self._refund * self.s006).sum()
            
            #nonrefuncable credits
            nonrefundable = (self.c07100 * self.s006).sum()
            
            #ospc_tax
            revenue1 = (self._ospctax * self.s006).sum()
            
            
            table.append([returns/math.pow(10,6),agi/math.pow(10,9),NumItemizer1/math.pow(10,6), 
                          ID/math.pow(10,9), NumSTD/math.pow(10,6), STD/math.pow(10,9),  
                          PE/math.pow(10,9), taxinc/math.pow(10,9), 
                          regular_tax/math.pow(10,9), AMTI/math.pow(10,9), AMT/math.pow(10,9), NumAMT1/math.pow(10,6), 
                          tax_bf_credits/math.pow(10,9),refundable/math.pow(10,9), 
                          nonrefundable/math.pow(10,9), revenue1/math.pow(10,9)])
            
            self.increment_year()
          
        df = DataFrame(table, row_years, 
               ["Returns (#m)", "AGI ($b)", "Itemizers (#m)", "Itemized Deduction ($b)", "Standard Deduction Filers (#m)", 
                "Standard Deduction ($b)", "Personal Exemption ($b)", "Taxable income ($b)", 
                "Regular Tax ($b)", "AMTI ($b)", "AMT amount ($b)", "AMT number (#m)", "Tax before credits ($b)", 
                "refundable credits ($b)", "nonrefundable credits ($b)",
                "ospctax ($b)"])
        df = df.transpose()
        pd.options.display.float_format = '{:8,.1f}'.format
        df.to_csv('baseline.csv')
        return df
