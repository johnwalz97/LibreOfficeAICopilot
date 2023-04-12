package:
	mkdir -p build
	rm -f build/libre_copilot.oxt
	cd libre_copilot && zip -r ../build/libre_copilot.oxt .
	cp build/libre_copilot.oxt /Users/jwalz/
