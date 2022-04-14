import pandas as pd

column_name = ["ticker","date","time","open","high","low","close","buy","sell"]
df = pd.read_csv("BANKNIFTY.csv",names=column_name)

totalProfit = 0
breakout_high = 0
breakout_low = 0
current_stop_loss = 0
current_traded = False
bought = 0
sold = 0
breakout_session = True
for index, row in df.iterrows():
    # We are at new date
    if row["time"] == "9:16":
        breakout_high = row["high"]
        breakout_low = row["low"]
        current_stop_loss = 0
        current_traded = False
        bought = 0
        sold = 0
        breakout_session = True
    elif row["time"] == "9:30":
        breakout_high = max(breakout_high,row["high"])
        breakout_low = min(breakout_low,row["low"])
        print(f'Date-> {row["date"]} breakout high-> {breakout_high} | breakout Low -> {breakout_low}')
        breakout_session = False
        
    # If we have traded now we need to move to the next day
    elif(current_traded == True):
        continue  
    
    # Now the time is to settle the trade 
    elif row["time"] == "15:15":
        if(current_traded == False):
            # Breakout occured at High's and we bought so the profit = Current Price - bought 
            if(bought != 0):
                print(f'(bought) Date-> {row["date"]}  bought At -> {bought} Sold at -> {row["close"]}')
                totalProfit += row["close"] - bought
                current_traded = True
                continue
            # Breakout occured at low's and we sold at the start so the profit = sold - Current Price
            elif(sold != 0):
                print(f'(sold) Date-> {row["date"]} Sold at -> {sold} bought At -> {row["close"]} ')
                totalProfit += sold - row["close"] 
                current_traded = True
                continue
            else:
                current_traded = True
                continue
        else:
            continue
        
    else :
        # Time between 9.15 - 9.30 That means we need to get the breakout high And breakout low
        if(current_traded == True):
            continue 
        
        if(breakout_session):
            breakout_high = max(breakout_high,row["high"])
            breakout_low = min(breakout_low,row["low"])
        # Trading session 9.30 - 3.15
        
        else:
            # Now we check wether if we have already bought or sold any share or not 

            # If we haven't we will check if it meets our condition
            if(sold == 0 and bought == 0):
                #  we meet the criteria to buy that is stock price is at breakout session high or greater
                if(row["close"] >= breakout_high):
                    bought = row["close"]
                    current_stop_loss = bought - bought * 0.005
                elif(row["close"]<= breakout_low):
                    sold = row["close"]
                    current_stop_loss = sold + sold * 0.005
                else:
                    continue
            # If we have sold the stock so to settle this trade we'll need to buy it(which we will do if stop loss hit)
            elif(sold != 0):
                if(row["open"] >= current_stop_loss):
                    print(f'(sold) Date-> {row["date"]} Sold at -> {sold} bought At -> {row["close"]} ')
                    totalProfit += sold - row["close"] 
                    current_traded = True
                else :
                    current_stop_loss = min(current_stop_loss,row["open"] + row["open"]*0.005)
            
            else:
                if(row["open"]<=current_stop_loss):
                    print(f'(bought) Date-> {row["date"]}  bought At -> {bought} Sold at -> {row["close"]}')
                    totalProfit += row["close"] - bought
                    current_traded = True
                else:
                    current_stop_loss = max(current_stop_loss,row["open"]-row["open"]*0.005)
                    
                
    # So the time is between 9:30 
print(f'Final Profit -> {totalProfit}')