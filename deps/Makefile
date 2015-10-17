.PHONY: clean

build: crlibm
	(cd $<; CFLAGS='-fPIC' ./configure --prefix=$(abspath $@))
	$(MAKE) -C $< install

crlibm: crlibm.tar.gz
	mkdir $@
	tar xzf $< -C $@ --strip-components=1

crlibm.tar.gz:
	curl -sSo $@ http://lipforge.ens-lyon.fr/frs/download.php/162/crlibm-1.0beta4.tar.gz

clean:
	-rm -rf build crlibm
