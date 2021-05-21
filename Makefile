PI=pyinstaller
BINARY_NAME=start
BINARY_LOC=dist/

binbot:
	$(PI) --onefile $(BINARY_NAME).py
	mv $(BINARY_LOC)$(BINARY_NAME) $(BINARY_LOC)$(BINARY_NAME).AppImage
clean:
	rm -rf build/ dist/ *.spec