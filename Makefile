PYTHON=python3
TIMER=/usr/bin/time

examples = $(wildcard example*.py)
png = $(examples:.py=.png)

default: $(png)
	true

%.png : %.py
	${TIMER} ${PYTHON} $<

clean:
	rm *.png
