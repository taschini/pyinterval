.PHONY: clean msys2

build: crlibm
	(cd $<; CFLAGS='-fPIC' ./configure --prefix=$(abspath $@))
	$(MAKE) -C $< install

msys2: crlibm
	# Download most recent config support scripts, which know of msys:
	curl -Sso crlibm/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
	curl -Sso crlibm/config.sub   'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
	# Pretend that msys is a BSD-type OS.
	perl -plwe 's/netbsd/netbsd*|msys/' -i.bak $</configure
	# Configure needs a working stdin, which is normally hijacked by appevyor:
	(cd $<; exec 0</dev/null; ./configure --prefix=$(abspath build))
	# cat $</config.log  # Uncomment for extra diagnostics.
	# SUBDIRS="scs_lib ." signifies that the tests subdirectory is to be skipped:
	$(MAKE) -C $< SUBDIRS="scs_lib ." install

crlibm: crlibm.tar.gz
	mkdir $@
	tar xzf $< -C $@ --strip-components=1

crlibm.tar.gz:
	curl -sSo $@ http://lipforge.ens-lyon.fr/frs/download.php/162/crlibm-1.0beta4.tar.gz

clean:
	-rm -rf build crlibm
