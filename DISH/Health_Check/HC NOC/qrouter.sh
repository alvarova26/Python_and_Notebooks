/radcom/omniq/qcmdln 4449 << eof | grep "cdrs dropped rate" | awk -F':' '{print $NF}'
MAINQ
pall
eof

