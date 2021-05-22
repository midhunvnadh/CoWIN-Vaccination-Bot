PI=pyinstaller
BINARY_NAME=start
BINARY_LOC=dist/

SRC_APP_IMAGE=Co-WIN_bot.AppImage
DEST_COMPRESS=Co-WIN_bot-AppImage

binbot:
	$(PI) --onefile $(BINARY_NAME).py
clean:
	rm -rf build/ dist/ *.spec release/
install_deps:
	pip3 install requests PyQt5 pyinstaller
release:
	mkdir -p release/
	cp $(BINARY_LOC)$(BINARY_NAME) release/$(SRC_APP_IMAGE)
	cd release && \
	tar -czvf $(DEST_COMPRESS).tar.gz $(SRC_APP_IMAGE) && \
	zip $(DEST_COMPRESS).zip $(SRC_APP_IMAGE) && \
	mv $(SRC_APP_IMAGE) $(SRC_APP_IMAGE).exe  && \
	cd .. 