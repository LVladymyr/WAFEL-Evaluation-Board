HARDWARE:

* 30A WORKING
	60A MAX

* 6 - 16 Li-ion / Li-Fe
	* it means 21 - 67V
	* Vgs is 67 x 2.5 redundancy = 167V or more
	
* Will use BQ769x2
* Size : 245 x 64 x 16
	Width and deep depends on bataries (245 x 64)
	Hight calculation:
	MAX HIGHT - 55
	CELLS HEIGHT (X2) - 39

protection to wrong + / -
protection to reverse connection electricity
protection to reverse impulses
pre-charge/pre-discharge
regular charging 5A but recuperation could generate up to ?15A everything above should somehow dumps  
CAN protection
in 

based on STM32L431
Should cover needs of consumption Go-Foc S100 at the most.

While be compartible with 300W and 500W in spike electrical engine.

SOFTWARE:


RUST based
