PYTHONPATH=${TRAVIS_BUILD_DIR}
export PYTHONPATH
cd ${TRAVIS_BUILD_DIR}
python test.pl
python $VIRTUAL_ENV/bin/trial cowrie
env
