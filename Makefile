
DESTDIR=/
PREFIX=/usr/local

all:
	@

install:
	env python2 setup.py install --root $(DESTDIR) --prefix $(PREFIX) --exec-prefix $(PREFIX)

clean:
	rm -rf build
	rm -rf jno.egg-info