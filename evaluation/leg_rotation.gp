reset
set terminal wxt size 350,262 enhanced font 'Verdana,10' persist
set multiplot 

# png
#set terminal pngcairo size 350,262 enhanced font 'Verdana,10'
#set output 'circle.png'
# svg
#set terminal svg size 350,262 fname 'Verdana, Helvetica, Arial, sans-serif' \
#fsize '10'
#set output 'circle.svg'

# Style definitions
set border lw 1.5
set style line 1 lc rgb '#0060ad' lt 1 lw 4     # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 2     # --- red

set size ratio -1
set xrange [-220:220]
set yrange [-240:240]

unset key; unset tics; unset border

set lmargin 0
set rmargin 1
set tmargin 1
set bmargin 0
set parametric
set trange [0:2*pi]
xCorrection = [0,0,0,0,0,0]
yCorrection = [0,0,0,0,0,0]
#functions
do for [i = 0:5]{
	tmp(t) = (xCorrection[i]**2)*(((cos(t))**2)-1)+(yCorrection[i]**2)*(((sin(t))**2)-1)+xCorrection[i]*yCorrection[i]*sin(2*t)+ R**2
	Rleg(t) = -xCorrection[i]*cos(t) - yCorrection[i]*sin(t) + sqrt(tmp(t)) 

	R = 220
	do for [angle=0:2*pi]{
		hx = Rleg(angle)*cos(angle)+xCorrection
		hy = Rleg(angle)*sin(angle)+yCorrection
		set arrow from xCorrection[i],yCorrection[i] to hx,hy nohead ls 2
		set label 'r' at 0.28,0.45 textcolor ls 2
	}

	plot R*cos(t),R*sin(t) ls 1 
	plot Rleg(t)*cos(t) + xCorrection[i],Rleg(t)*sin(t) + yCorrection[i] ls 2
#plot Rleg(t)*cos(t)+xCorrection, Rleg(t)*sin(t) +yCorrection ls 1
	plot "<echo 'xCorrection[i] yCorrection[i]'"   with points ls 1,

unset multiplot