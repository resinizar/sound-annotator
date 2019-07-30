import logging
import yaml



logger = logging.getLogger('session.py')


def save(fp, datapath, savepath, min_dur, f_ind):
	d = {
		'audio data path': datapath,
		'csv file save path': savepath,
		'minimum clip duration': min_dur,
		'file index': f_ind
	}
	with open(fp, 'w') as file:
		yaml.dump(d, file)

	logger.info('saved session file to {}'.format(fp))


def load(fp):
	with open(fp, 'r') as file:
		d = yaml.load(file, Loader=yaml.BaseLoader)

	logger.info('loaded session from {}'.format(fp))
	
	return (
		d['audio data path'], 
		d['csv file save path'], 
		d['minimum clip duration'], 
		d['file index']
	)
