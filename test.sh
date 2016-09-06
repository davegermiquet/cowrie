PYTHONPATH=${TRAVIS_BUILD_DIR}
export PYTHONPATH
cd ${TRAVIS_BUILD_DIR}
cd ..
python $VIRTUAL_ENV/bin/trial cowrie.test
