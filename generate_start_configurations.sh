#!/bin/bash
BLK_BND="${HOME}/Documents/Codes/git/copoly/block_boundaries.py"
GEN_SEQ="${HOME}/Documents/Codes/git/copoly/convert_chain_atomtypes.py"
GEN_DAT="${HOME}/Documents/Codes/git/mouse2/mouse2/tests/create_configuration.py"
PKL_DIR="${HOME}/q/Copoly/data/for_article"

BOX="1000"
DATA_NAME="0.data"

FVCLS="0.55"		#"0.55 0.7 0.85"
TAILS=""		#"0.5 0.375 0.25 0.125"

DATA_OPTIONS=""		#"--angles"

shopt -s nullglob

write_datafile () {

	local LNTRUNC="$1"
	local SIM_DIR="f_${FVCL}_chain_${NCH}_N_${LNTRUNC}"
	local TMPFILE="$(mktemp)"
	mkdir "${SIM_DIR}"
	echo "${GEN_SEQ} ${PKL} --nmol-offset ${OFF} --nmol 1 --truncate ${LNTRUNC}"
	${GEN_SEQ} ${PKL} --nmol-offset ${OFF} --nmol 1 --truncate ${LNTRUNC} > "${TMPFILE}"
	${GEN_DAT} "${SIM_DIR}/${DATA_NAME}" --type random --self-avoid --box ${BOX} --atomtypes "${TMPFILE}" ${DATA_OPTIONS}
	rm "${TMPFILE}"
	
}


for FVCL in ${FVCLS}
do
	PKL="${PKL_DIR}/chains_f_${FVCL}.pkl"
	for NCH in 81 41 51 60 63 #31 23 33 52 55
	do
		OFF=$((${NCH}-1))
		NCOP=`${BLK_BND} ${PKL} --nmol-offset ${OFF} --nmol 1 | grep 'Type 2 max' | sed s/'Type 2 max '//`
		NTOT=`${BLK_BND} ${PKL} --nmol-offset ${OFF} --nmol 1 | grep 'Length' | sed s/'Length '//`
		write_datafile ${NTOT}
		for TAIL in ${TAILS}
		do
			NTRUNC=$(python3 -c "print(int(round(${NCOP}/(1.-${TAIL}))))")
			if [ "$NTRUNC" -lt "$NTOT" ]
			then
				write_datafile ${NTRUNC}
			fi
		done
	done
done
