
default: map-clean map-result

map-result:
	cd qap; python qap_script.py; cd ..;
	@echo "Generated mapping results as text files"

map-clean:
	cd qap; rm -rf data/; rm -rf result/; mkdir result; mkdir data/; cd ..;
	@echo "Cleaned mapping result and data files"



help:
	@echo "    map-result"
	@echo "        Generate mapping results as text files"
	@echo "    map-clean"
	@echo "        Clean mapping result and data files"

