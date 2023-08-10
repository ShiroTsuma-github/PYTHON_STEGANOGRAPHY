# Python Steganography Project

This Python project aims to implement steganography techniques to hide encoded messages within images. Steganography is the art and science of concealing information 
within other non-secret data to avoid detection. In this case, we'll be hiding messages within image files.

## Table of Contests
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)
- [Installation](#installation)
- [Examples](#examples)
- [License](#license)

## Getting Started 

Our objective was to create interesting solution for hiding messages that noone is able to see it. What's interesting about this project it's a implementation, 
message you want to hide is coded 2 times. First app is coding your message as diffrent chars with, then it's coded in image.

## Usage

App that codes messages in images can be useful when you want exchange messages with your friend like in action films. We can use it in situations where we're not
sure about communicator we're using with friends and want test it if it's not stealing our data. We can also store our private notes without fear of someone seeing it.
Some may use the app to create artistic works where the message is hidden in the content of the image. This can be an interesting application for people who like
to combine art with technology. It is important to note that while such an app can be used for a variety of purposes, there is also potential for inappropriate or 
illegal use, such as concealing unethical or criminal activities. Always use technology responsibly and legally.

## Features
With this app you can: 
   - hide message which include all special characters you have on keyboard and all letters in polish language
   - hide message up to 1000 characters for image with 100 x 100 resolution
   - choosing image with .jpg, jpeg and .png (transparency not supported ) extensions
   - generate coding key which is 32 bit long and have hexadecimal numbers or try your own key ( minimum 10 bit lengh, less than that can produce errors ) 
   - all of options above are packed into one minimalistic window application which nice for your eye
   - one .exe file needed for application working as intended 

## Installation

To use this steganography tool, you will need to have Python 3 installed on your system. Clone this repository and install the required dependencies 
using the following commands:
   - git clone https://github.com/ShiroTsuma-github/PYTHON_STEGANOGRAPHY.git
   - cd PYTHON_STEGANOGRAPHY
   - pip install -r requirements.txt 

## Examples

Coding message "I love programming" in image with png extension with auto generated key 

![Example1]()

Decoding message "I love programming" from coded image with png extension with earlier generated key

![Example2]()

##License

