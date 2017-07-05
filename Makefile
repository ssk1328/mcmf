

default: map route

route: route-clean route-gen

map: map-clean map-result

map-result:
	@echo "Generating mapping results as text files"
	cd qap; python qap_script.py; cd ..;

map-clean:
	@echo "Cleaning mapping result and data files"
	cd qap; rm -rf data/; rm -rf result/; mkdir result; mkdir data/; cd ..;

route-gen:
	@echo "Generating blusespec files post routing in /bsv"
	gurobi.sh mcflow.py

route-clean: 
	@echo "Clean routing generated bluespec files from /bsv"
	rm -f bsv/Lookup*

help:
	
	@echo "    map-result"
	@echo "        Generate mapping results as text files"
	@echo "    map-clean"
	@echo "        Clean mapping result and data files"
	
	@echo "    route-gen"
	@echo "        Generate blusespec files post routing in /bsv"
	@echo "    route-clean"
	@echo "        Clean routing generated bluespec files from /bsv"
