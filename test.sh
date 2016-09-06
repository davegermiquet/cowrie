PYTHONPATH=${TRAVIS_BUILD_DIR}:${TRAVIS_BUILD_DIR}/cowrie/core
export PYTHONPATH
python 
cd ${TRAVIS_BUILD_DIR}
python test.pl
python $VIRTUAL_ENV/bin/trial cowrie
