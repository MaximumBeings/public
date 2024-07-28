/******************************************************************************
Read loan file into the SAS system and create a new variable LTV which was not part
of the original loan data. LTV = Loan to Value Ratio is calculated as the ratio of 
loan balance over the appraisal value.
Data Source: www.wiley.com/go/vba
*******************************************************************************/


data file_list;

infile "C:\books\SAS\mbs_orig_2.csv" dlm='2C0D'x dsd missover
lrecl=10000 firstobs=2;

input 	
	OrigBankBal CurBankBal Coupon: Percent5. OrigTerm RemTerm Season 
	Fixed_Float Index	$ Spread: Percent3. ResetRate: 1. RestPmt LifeFloor: Percent5. 
	LifeCap	: Percent5. ResetCap : Percent5. ResetFloor : Percent5.	
	DayCount StatedPmt Appraisal OrigEquity Current_Equity 	State $ ZipCode	
	OrigYear OrigMonth	MatYear	MatMonth
	CalcPmt: comma10.2 
;
LTV=CurBankBal/Appraisal;
run;


/******************************************************************************
Set the format for certain variables that will be used for categorial analysis
to understand the key characteristics of the loan data
*******************************************************************************/

Proc Format;
	value CBfmt 0 - 50000 = '<$50,000'
				50001-250000 = 'Between $50,001 - $250,000'
				250001-500000 = 'Between $250,001 - $500,000'
				500001-750000 = 'Between $250,001 - $750,000'
				750001-1000000 = 'Between $750,001 - $1,000,000'
				1000001-1250000 = 'Between $1,000,001 - $1,250,000'
				1250001-1500000 = 'Between $1,250,001 - $1,500,000'
				1500001-1750000 = 'Between $1,500,001 - $1,750,000';

	value Couponfmt	0.000 - 0.0699 = 'Between 0-6.999%'
					0.070 - 0.0799 = 'Between 7.00-7.999%'
					0.080 - 0.0899 = 'Between 8-8.999%'
					0.090 - 0.0999 = 'Between 9-9.999%'
					0.10 - 0.10999 = 'Between 10-10.999%'
					0.11 - 0.11999 = 'Between 11-11.999%';

	Value $Statefmt	'MA','NH','VT','RI','CT','NY','PA','NJ','ME' = "NorthEast"
					'WI','MI','IL','IN','OH','ND','SD','NE','KS',
					'MN','IA','MO' = "MidWest"
					'DE','MD','DC','WV','NC','SC','GA','FL','KY','TN',
					'MS','AL','OK',
					'TX','AR','LA','VA' = "South"
					'ID','MT','WY','NV','UT','CO','AZ','NM','AK','WA',
					'OR','CA','HA' = "West"
					'VI' = "US Territory";

	run;

/******************************************************************************
To print entire loan file and inspect that the import operation was successful
*******************************************************************************/

Proc Print Data=file_list;
format OrigBankBal comma10.2
	   CurBankBal comma10.2
	   Coupon percentn10.2;
run;


/******************************************************************************
Perform categorical analysis on sample parameters
*******************************************************************************/

Proc Freq data=file_list;
	Title 'Categorical Analysis of MBS Loan Pool By Original Balance Versus Coupon';
	tables OrigBankBal*Coupon /norow nocol;
	format OrigBankBal CBfmt. Coupon Couponfmt.;
run;

*options linesize=84 pageno=1 nodate;

Proc tabulate data=file_list;
	Title 'Categorical Analysis of Key Loan Balance By Coupon';
		Class Coupon;
		var CurBankBal OrigBankBal Current_Equity;
		tables Coupon all,
	 CurBankBal*(n*f=comma10. colpctsum='% CurBankBal' (sum)*f=dollar16.2 ) 
		OrigBankBal*(sum)*f=dollar16.2 Current_Equity*(sum)*f=dollar16.  ;
	format CurBankBal CBfmt. Coupon Couponfmt.;
run;

Proc tabulate data=file_list;
	Title 'Categorical Analysis of MBS Loan Pool By Region';
		Label State = "Region";
		Class State;
		var CurBankBal OrigBankBal Current_Equity;
		tables State all,
		OrigBankBal*(n*f=comma10. colpctsum='Percentage (%)' (sum)*f=dollar16.2 ) ;
		format CurBankBal CBfmt. Coupon Couponfmt. State $Statefmt. ;
run;


Proc Means Data = file_list maxdec=2 N MEAN MIN MAX RANGE SUM;
	Title3 " Categorical Analysis: Key Summary Statistics";

	var OrigBankBal CurBankBal Coupon OrigTerm RemTerm Season 
	Fixed_Float  Spread ResetRate RestPmt LifeFloor
	LifeCap ResetCap ResetFloor DayCount StatedPmt Appraisal 
	OrigEquity Current_Equity OrigYear OrigMonth MatYear MatMonth CalcPmt;

	format OrigBankBal comma10. ;

Run;


/******************************************************************************
Collateral Ineligibility Reports - Sample Only - Can Be Extended for Further
Criteria.  Other ineligibility conditions that can be generated (not included
in the sample below) include (i) Minimum/Maximum Remaining Term (ii) Minimum/
Maximum Original Term (iii) Minimum/Maximum Original Balance (iv) Minimum/Maximum
Current Balance (iv) Unacceptable Floater Indices/Spread (v) Inconsistent Original
versus Remaining Term (vi) Inconsistenet Original versus Remaining Balance (vii)
Unacceptable Gross Coupon.
*******************************************************************************/


/******************************************************************************
Collateral Ineligibility Reports - Exceeds Maximum LTV 7.8% (Based on assumption)
*******************************************************************************/
data total_LTV;
	set file_list;
	where LTV > 0.78;
	Total + CurBankBal;
	run;

Proc Print data=total_LTV;
	Title 'Exceeds Maximum LTV Ratio';
	var LTV CurBankBal Total;
	format CurBankBal dollar10. Total dollar10. ;
run;


/******************************************************************************
Collateral Ineligibility Reports - Excluded State or Geographic Region
*******************************************************************************/

data total_LTV;
	set file_list;
	where State = 'VI';
	Total + CurBankBal;
	run;
Proc Print data=total_LTV;
	Title 'Excluded State or Georgaphic Region';
	where State  = 'VI';
	var State CurBankBal Total;
	format CurBankBal dollar10. Total dollar10. ;
run;

/******************************************************************************
Collateral Ineligibility Report - Stated Payment Versus Calculated Payment
*******************************************************************************/
options nodate;
Proc Print data=file_list ;
Title 'Stated Payment Not Equal Calculated Payment';

	where StatedPmt  <> CalcPmt;
	var StatedPmt CalcPmt CurBankBal;
	format CurBankBal dollar10. ;
run;


/******************************************************************************
To generate the final loan list of qualified/eligible loans only i.e. excluding
ineligible collaterals.
*******************************************************************************/

Data finalList;
	Set file_list;
		where (LTV < 0.78 and State <>'VI' and StatedPmt eq CalcPmt);
	Run;

Proc Print Data=finalList;
var CurBankBal;
	run;

/******************************************************************************
Finally, a random sample of 30 items is selected for further substantive testing
namely verification, validation and confirmation by the underwriting and risk control
teams.
*******************************************************************************/

	Proc Surveyselect Data=finallist method = SRS rep=1
		sampsize=5 seed = 12345 out = randomsample;	
		id State Appraisal CurBankBal Coupon;
	run;

	Proc Print data = randomsample;
	Title 'Random Samples';
	format Appraisal dollar10. CurBankBal dollar10. ;
	run;
