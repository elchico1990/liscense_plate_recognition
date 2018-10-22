import sys
import cv2
import numpy as np

import darknet.python.darknet as dn

from src.label 				import Label, lwrite
from os.path 				import splitext, basename, isdir
from os 					import makedirs
from src.utils 				import crop_region, image_files_from_folder
from darknet.python.darknet import detect


if __name__ == '__main__':

	input_dir  = sys.argv[1]+'/images_from_video'
	output_dir = sys.argv[1]

	vehicle_threshold = .5

	vehicle_weights = 'data/vehicle-detector/yolo-voc.weights'
	vehicle_netcfg  = 'data/vehicle-detector/yolo-voc.cfg'
	vehicle_dataset = 'data/vehicle-detector/voc.data'

	vehicle_net  = dn.load_net(vehicle_netcfg.encode('utf-8'), vehicle_weights.encode('utf-8'), 0)
	vehicle_meta = dn.load_meta(vehicle_dataset.encode('utf-8'))

	imgs_paths = image_files_from_folder(input_dir)
	imgs_paths.sort()

	if not isdir(output_dir):
		makedirs(output_dir)

	#print('Searching for vehicles using YOLO...')
	print(imgs_paths)
	for i,img_path in enumerate(imgs_paths):

		#print('\tScanning %s' % img_path)

		bname = basename(splitext(img_path)[0])

		R = detect(vehicle_net, vehicle_meta, img_path.encode('utf-8') ,thresh=vehicle_threshold)

		#print ('\t\t%d cars found' % len(R))

		if len(R):

			Iorig = cv2.imread(img_path)
			WH = np.array(Iorig.shape[1::-1],dtype=float)
			Lcars = []

			for i,r in enumerate(R):

				cx,cy,w,h = (np.array(r[2])/np.concatenate( (WH,WH) )).tolist()
				tl = np.array([cx - w/2., cy - h/2.])
				print(tl.shape)
				br = np.array([cx + w/2., cy + h/2.])
				label = Label(0,tl,br)
				Icar = crop_region(Iorig,label)
				Lcars.append(label)


				I = Iorig
				wh = np.array(I.shape[1::-1])
				ch = I.shape[2] if len(I.shape) == 3 else 1
				tl = np.floor(label.tl()*wh).astype(int)
				br = np.ceil (label.br()*wh).astype(int)
				outwh = br-tl

				# if np.prod(outwh) == 0.:
				# 	return None

				outsize = (outwh[1],outwh[0],ch) if ch > 1 else (outwh[1],outwh[0])
				if (np.array(outsize) < 0).any():
					pause()
				Iout  = np.zeros(outsize,dtype=I.dtype) + 0.5

				offset 	= np.minimum(tl,0)*(-1)
				tl 		= np.maximum(tl,0)
				br 		= np.minimum(br,wh)
				wh 		= br - tl

				cv2.imwrite('%s/%s_%dcar.png' % (output_dir,bname,i),Icar)

			lwrite('%s/%s_cars.txt' % (output_dir,bname),Lcars)
