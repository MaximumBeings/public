def bondValuation(principal, coupon_rate, paymentFrequency, mkt_rate, years):
    coupon_payment = principal * (coupon_rate/100.0)/paymentFrequency
    n = paymentFrequency * years
    #declare intermediate variables
    y = mkt_rate/100.0
    total = 0.0
    coupon2 = 0.0
    principal2 = 0.0
    dPrin = 0.0
    subtotal = 0.0
    total = 0.0
    
    print ""
    print "BOND CASHFLOW/VALUATION TABLE"
    template = "{0:4}|{1:9}|{2:10}|{3:10}|{4:10}|{5:13}|{6:20}"
    print('_'*72)
    print template.format("NR#", "Coupon", "Disc_Coup","Principal","Disc_Princ", "DiscCoup&Prin","Total_PV") # header
    print('_'*72)
    for x in range(1,n+1,1):
        coupon2 = coupon_payment/(1+y/paymentFrequency)**x
        total += coupon2
        subtotal = dPrin + coupon2
        if x == n:
            total += principal/(1+y/paymentFrequency)**x
            principal2 = principal
            dPrin = principal/(1+y/paymentFrequency)**x
            subtotal = dPrin + coupon2
        template = "{0:4}|{1:9}|{2:10}|{3:10}|{4:10}|{5:13}|{6:20}"
        print template.format(x, "%.2f" % coupon_payment, "%.2f" % coupon2,"%.2f" % principal2, "%.2f" % dPrin,"%.2f" % subtotal,"%.2f" % total)
    print ""
    print "The Value of a $" +  "{:,.2f}".format(principal) + " Bond with a " +  str(coupon_rate) + "% coupon rate and a yield of " + str(mkt_rate) + "%"
    print "compounded " + str(paymentFrequency) + " time(s) per annum" + " for " + str(years) + " years is: $" + "{:,.2f}".format(total)
        
#Example call - no commas or Dollar sign in numbers (Principal = 2000, Coupon = 4.00, Payment Frequency = 1, Yield/Mkt Rate = 3.00, Years to Maturity = 12)
bondValuation(2000, 4.00, 2, 3.00, 12)