pyfile = christofides.py
cfile = christofides.c
outfile = christofides

christofides:
	cython3 -3 --embed -o $(cfile) $(pyfile)
	gcc -Os -I /usr/include/python3.6m -o $(outfile) $(cfile) -lpython3.6m -lpthread -lm -lutil -ldl

clean:
	rm $(cfile) $(outfile)