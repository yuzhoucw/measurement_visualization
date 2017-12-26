#!/usr/bin/env python

"""
Plot the C-V curve.

Example Usage:
	python plot_cv_curve.py --input './FeRAM/CV/2017-12-13_CV/C-V_1213_MFIS_SK3_140cyc_cell05_run*'
"""

import argparse
import csv
import glob
import os.path
import matplotlib.pyplot as plt


def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--input',
		dest='input',
		type=str,
		default='.',
		help='Path pattern of the input file.',
		required=True)

	args = parser.parse_args()

	return args


def read_data(filename):
	num_data_points = 0

	with open(filename, 'r') as f:
		reader = csv.reader(f)
		v_bias = []
		c = []
		r = []
		for row in reader:
			if row[0] == 'DataValue':
				v_bias.append(float(row[1]))
				c.append(float(row[2]))
				r.append(float(row[3]))

				num_data_points += 1

	data = {
			'VBias': v_bias,
			'C': c,
			'R': r,
			}

	print('Read %d data points.' % (num_data_points))

	dirname = os.path.dirname(filename)
	basename = os.path.basename(filename)
	basename_without_ext, _ = os.path.splitext(basename)
	output_path = os.path.join(dirname, 'plot_%s.png' % (basename_without_ext))
	print('Saving the plot to %s...' % (output_path))
	plt.savefig(output_path)

	return data


def plot_data(data):
	plt.figure(figsize=(10, 10))
	plt.plot(data['VBias'], data['C'])
	plt.title('Yuzhou\' drawing.')
	plt.xlabel('VBias')
	plt.ylabel('C')
	# plt.savefig('my_fig.png')			


def main():
	args = parse_args()

	input_pattern = os.path.abspath(args.input)
	filenames = glob.glob(input_pattern)

	for filename in filenames:
		print('Reading file %s...' % (filename))
		data = read_data(filename)
		print('Ploting the data...')
		plot_data(data)

	plt.show()


if __name__ == '__main__':
	main()