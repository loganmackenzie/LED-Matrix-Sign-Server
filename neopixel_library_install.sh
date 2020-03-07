# Download the library
git clone https://github.com/jgarff/rpi_ws281x

# Compile the necessary C files
cd rpi_ws281x/
sudo scons

# Install the Python package
cd python
sudo python3 setup.py build
sudo python3 setup.py install
