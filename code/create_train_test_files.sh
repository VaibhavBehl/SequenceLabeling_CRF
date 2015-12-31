rm -f swbdDAMSL.crfsuite.$1.$2
for file in ../data/$2/*.csv
do
    python3 create_$1_features.py $file >> swbdDAMSL.crfsuite.$1.$2
    echo $'\n' >> swbdDAMSL.crfsuite.$1.$2
done
