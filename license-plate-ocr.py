import sys
import cv2
import numpy as np

import darknet.python.darknet as dn

from os.path 				import splitext, basename
from glob					import glob
from darknet.python.darknet import detect


if __name__ == '__main__':

	input_dir  = sys.argv[1]
	output_dir = input_dir

	ocr_threshold = .4

	ocr_weights = 'data/ocr/ocr-net.weights'
	ocr_netcfg  = 'data/ocr/ocr-net.cfg'
	ocr_dataset = 'data/ocr/ocr-net.data'

	ocr_net  = dn.load_net(ocr_netcfg.encode('utf-8'), ocr_weights.encode('utf-8'), 0)
	ocr_meta = dn.load_meta(ocr_dataset.encode('utf-8'))

	imgs_paths = glob('%s/*lp.png' % output_dir)

	print('Performing OCR...')

	for i,img_path in enumerate(imgs_paths):

		print ('\tScanning %s' % img_path)

		bname = basename(splitext(img_path)[0])

		R = detect(ocr_net, ocr_meta, img_path.encode('utf-8'),thresh=ocr_threshold)

		if len(R):

			R.sort(key=lambda x: x[2][0])
			lp_str = b''.join([r[0] for r in R])

			with open('%s/%s_str.txt' % (output_dir,bname),'wb') as f:
				f.write(lp_str + b'\n')

			print ('\t\tLP: %s' % lp_str)

		else:

			print('No characters found')
