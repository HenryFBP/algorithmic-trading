# YOINK from https://medium.com/analytics-vidhya/implementing-a-simple-mean-reverting-pairs-trading-algorithm-in-the-quantconnect-platform-part-2-3595c35b5cff

from scipy.stats import linregress


class EMAMomentumUniverse(QCAlgorithm):
    
    def Initialize(self):
        # Define backtest window and portfolio cash
        self.SetStartDate(2012, 6, 10)
        self.SetEndDate(2021, 6, 9)
        self.SetCash(100000)


        # Add the assets to be fed into the algorithm and save the symbol objects (to be referred later)
        self.asset1 = self.AddEquity('EWA', Resolution.Daily).Symbol
        self.asset2 = self.AddEquity('EWC', Resolution.Daily).Symbol
        
        # We then create a bollinger band with 120 steps for lookback period
        self.bb = BollingerBands(220, 0.5, MovingAverageType.Simple)
        
        # Define the objectives when going long or going short (long=buy asset 2 and sell asset 1) (short=sell asset 1 and buy asset 2)
        self.long_targets = [PortfolioTarget(self.asset2, 0.9), PortfolioTarget(self.asset1, -0.9)]
        self.short_targets = [PortfolioTarget(self.asset2, -0.9), PortfolioTarget(self.asset1, 0.9)]

        self.is_invested = None         # set the starting flag as not invested

        self.lookback = 220             # set the look back period to calculate the linear regression and find the hedge ratio

    def OnData(self, data):

        # for daily bars data is delivered at 00:00 of the day containing the closing price of the previous day (23:59:59)
        if (not data.Bars.ContainsKey(self.asset1)) or (not data.Bars.ContainsKey(self.asset2)):
            return

        # As we need a dataframe, we will use the history function, as we did in the research notebook
        history = self.History([self.asset1, self.asset2], self.lookback, Resolution.Daily)
        history = history.unstack(level=0).dropna()

        asset1 = history['close', self.asset1.Value]
        asset2 = history['close', self.asset2.Value]
        
        reg = linregress(asset1, asset2)
        
        portfolio = data[self.asset2].Close - data[self.asset1].Close * reg.slope - reg.intercept
        
        self.bb.Update(self.Time, float(portfolio))
        
        # Plot the portfolio (to see if it is working, and the bb bands)
        self.Plot("Indicators", "Portfolio", float(portfolio))
        self.Plot("Indicators", "Middle", self.bb.MiddleBand.Current.Value)
        self.Plot("Indicators", "Upper", self.bb.UpperBand.Current.Value)
        self.Plot("Indicators", "Lower", self.bb.LowerBand.Current.Value)     
        self.Plot("Arguments", "Hedge", float(reg.slope))     
        self.Plot("Arguments", "Intercept", float(reg.intercept))     
        

        # check if the bolllinger band indicator is ready (filled with 120 steps)
        if not self.bb.IsReady:
            return
        
        upper_band = self.bb.UpperBand.Current.Value
        lower_band = self.bb.LowerBand.Current.Value
        middle_band = self.bb.MiddleBand.Current.Value
        
        # Now that we have all values that we need, and the indicator is ready, let's attach the trading mechanism
        # if it is not invested, see if there is an entry point
        if not self.is_invested:
            # if our portfolio is bellow the lower band, enter long
            if portfolio < lower_band:
                self.SetHoldings(self.long_targets)

                self.Debug('Entering Long')
                self.is_invested = 'long'
            
            # if our portfolio is above the upper band, go short
            if portfolio > upper_band:
                self.SetHoldings(self.short_targets)
                
                self.Debug('Entering Short')
                self.is_invested = 'short'
        
        # if it is invested in something, check the exiting signal (when it crosses the mean)   
        else:
            if self.is_invested == 'long' and portfolio > middle_band:
                self.Liquidate()
                self.Debug('Exiting Long')
                self.is_invested = None
            elif self.is_invested == 'short' and portfolio < middle_band:
                self.Liquidate()
                self.Debug('Exiting Short')
                self.is_invested = None
            
