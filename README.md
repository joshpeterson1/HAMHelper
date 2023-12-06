# HamHelper

HamHelper (FKA HamCalc) is a versatile tool designed for amateur radio enthusiasts. It provides a range of calculations and utilities to assist with various aspects of ham radio operations...

Note that this application is very early stages, and functionality will be continue to be added. While I have preformed basic tests, there will likely be bugs. Please feel free to submit a PR fix or drop a descriptive report in Issues otherwise.

## Features

- **Frequency to Wavelength Conversion**: Easily convert between frequency and wavelength.
- **Ohm's Law Calculator**: Calculate voltage, current, resistance, and power using Ohm's Law.
- **Power Calculations**: Perform calculations related to peak voltage, PEP, RMS, and peak-to-peak voltage.
- **R, C, L Calculations**: Perform calculations for Capacitors, Inductors, and / or Restistors in series or parallel.
- **Positioning**: Enter City & State, Zip, or Lat & Long to get your Maidenhead Grid square in 4 and 6 format. (more features coming soon)
- **Customizable Settings**: Adjust window size, opacity, and other preferences.
- **Live Calculation**: Real-time updates of calculations as you input values.

## Installation

To use HamHelper, download the `freq.exe` executable file in the zipped folder from the [releases page](https://github.com/joshpeterson1/HamCalc/releases). Extract and double-click the file to run the application. A config file is created in the directory where the application is run. Because of this, it's recommended to keep the .exe file in it's extracted folder, or place it in its own folder in your desired install location.

## Usage

Upon launching HamHelper, you'll be presented with a tabbed interface. Each tab contains fields for inputting values relevant to different calculations. Enter the required values, and the software will automatically calculate and display the results.

## Config

Here is an example config: 
```
[Settings]
always_on_top = True
opacity = 1.0
window_width = 249
window_height = 378
ohms_live_calc = True
moar_live_calc = True
moar_live_calc_delay = 1.0
```
- `always_on_top:` (True / False) Always on top setting for application. Available in settings and will be remembered upon application close.
- `opacity:` opacity value for application. Available in settings and will be remembered upon application close.
- `window_width:` Width of window. Will be respected at launch at saved when closing the program.
- `window_height:` Height of window. Will be respected at launch at saved when closing the program.
- `ohms_live_calc:` (True / False) Whether or not calculations on the Ohms tab are preformed automatically. Available via checkbox on Ohms tab, saved on exit.
- `moar_live_calc:` (True / False) Whether or not calculations on the Moar Pwr tab are preformed automatically. Available via checkbox on Moar Pwr tab, saved on exit.
- `moar_live_calc_delay:` Set the delay of auto calculations for Moar Pwr calcs. Since only 1 value is needed, if this is too low, you may not be able to finish inputting your value. 

## Contributing

Contributions to HamHelper are welcome! If you have coding skills and wish to contribute, please feel free to make a pull request. Here's how you can do it:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

Please be sure to specify any changes / added functionality and the intent behind it as it will help with merging.

## Feedback and Support

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
